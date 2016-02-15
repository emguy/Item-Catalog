# flask
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask import make_response

# get the login session from flask
from flask import session as login_session

# orm
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Catalog, User,Item

# oauth
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

# some standard python modules
import httplib2
import json
import random
import string
import requests

# name of this web application
APPLICATION_NAME = "Item Catalog"

# required by Flask
app = Flask(__name__)

# connect to database and create database session through sqlalchemy
engine = create_engine("sqlite:///items.db") # here, we specifies the sqlite db file
Base.metadata.bind = engine # used only once
DBSession = sessionmaker(bind=engine) # used only once
db_session = DBSession() # we only need this handler for all database interactions

# load the client id (generated by google)
CLIENT_ID = json.loads(open("client_secrets.json", 'r').read())["web"]["client_id"]

# create anti-forgry state tocken
@app.route("/login")
def show_login():
  # generate a random text with length=32
  login_session["state"] = "".join(
       random.choice(string.ascii_uppercase + string.digits) for x in range(32))
  cats = db_session.query(Catalog).order_by(Catalog.name).all()
  return render_template("main.html", task="show_login", cats=cats, STATE=login_session["state"])

@app.route("/gconnect", methods=["POST"])
def gconnect():
  """ 
  this method handles user authentication.
  
  Returns:
    a JSON object with proper error message if the authentication is
    unsuccessful.
  """
  # step 1 - validate state token (here 'state' is passed as a url argument)
  if request.args.get("state") != login_session["state"]:
    response = make_response(json.dumps("Invalid state parameter."), 401)
    response.headers["Content-Type"] = "application/json"
    return response

  # step 2 - obtain authorization code, now compatible with Python3 
  request.get_data()
  code = request.data.decode("utf-8")

  # step 3 - upgrade the authorization code into a credentials object
  # which contains the access-token
  try:
    oauth_flow = flow_from_clientsecrets("client_secrets.json", scope="")
    oauth_flow.redirect_uri = "postmessage"
    credentials = oauth_flow.step2_exchange(code)
  except FlowExchangeError:
    response = make_response(
      json.dumps("Failed to upgrade the authorization code."), 401)
    response.headers["Content-Type"] = "application/json"
    return response

  # step 4 - check that the access token is valid.
  access_token = credentials.access_token
  url = ("https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s"
     % access_token)
  # submit request, parse response - Python3 compatible
  h = httplib2.Http()
  h_response = h.request(url, "GET")[1]
  str_h_response = h_response.decode("utf-8")
  result = json.loads(str_h_response) # this is the parsed response
  # if there was an error in the access token info, abort.
  if result.get("error") is not None:
    response = make_response(json.dumps(result.get("error")), 500)
    response.headers["Content-Type"] = "application/json"
    return response
  # verify that the access token is used for the intended user.
  gplus_id = credentials.id_token["sub"]
  if result["user_id"] != gplus_id:
    response = make_response(
      json.dumps("Token's user ID doesn't match given user ID."), 401)
    response.headers["Content-Type"] = "application/json"
    return response
  # verify that the access token is valid for this app.
  if result["issued_to"] != CLIENT_ID:
    response = make_response(
      json.dumps("Token's client ID does not match app's."), 401)
    response.headers["Content-Type"] = "application/json"
    return response

  # step 5 - check that if the user is already logged in
  stored_access_token = login_session.get("access_token")
  stored_gplus_id = login_session.get("gplus_id")
  if stored_access_token is not None and gplus_id == stored_gplus_id:
    response = make_response(json.dumps("Current user is already connected."), 200)
    response.headers["Content-Type"] = "application/json"
    return response
  # if not logged in, we store the access token in the session for later use.
  login_session["access_token"] = access_token
  login_session["gplus_id"] = gplus_id

  # step 6 - post-processing
  # Get user info and parse it
  userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
  params = {"access_token": access_token, "alt": "json"}
  answer = requests.get(userinfo_url, params=params)
  data = answer.json()
  # Add user info to login_session
  login_session["username"] = data["name"]
  login_session["email"] = data["email"]
  # see if user exists, if it doesn't make a new one
  user_id = get_user_id(login_session["email"])
  if not user_id:
    user_id = create_user(login_session)
  login_session["user_id"] = user_id
  # display confirmation
  output = "Welcome, " + login_session["email"] + "!</h3>"
  return output

@app.route("/gdisconnect")
def gdisconnect():
  """
  This method handle the user logout event.

  Returns:
    a JSON object with proper error message if this process is
    unsuccessful.
  """
  # only disconnect a connected user
  print(login_session)
  credentials = login_session.get("access_token")
  if credentials is None:
    response = make_response(json.dumps("Current user not connected."), 401)
    response.headers["Content-Type"] = "application/json"
    return response
  # send request to google
  access_token = login_session["access_token"]
  url = "https://accounts.google.com/o/oauth2/revoke?token=%s" % access_token
  h = httplib2.Http()
  result = h.request(url, "GET")[0]
  if result["status"] == "200":
    # Reset the user's sesson.
    del login_session["access_token"]
    del login_session["gplus_id"]
    del login_session["username"]
    del login_session["email"]
    return redirect(url_for("show_login"))
  else:
    # For whatever reason, the given token was invalid.
    response = make_response(
        json.dumps('Failed to revoke token for given user.', 400))
    response.headers['Content-Type'] = 'application/json'
    return response

# this is the JSON endpoint
@app.route("/catalog.json")
def get_json():
  """
  This is the required json endpoint.

  Returns:
    a JSON object containing all item information.
  """
  cats = db_session.query(Catalog).order_by(Catalog.name).all()
  out = [cat.serialize for cat in cats]
  for entry in out:
    id = entry["id"]
    items = db_session.query(Item).filter_by(catalog_id=id).all()
    entry["items"] = [i.serialize for i in items]
  return jsonify(Catalog=out)

@app.route("/")
def show_main():
  """
  This is the home page. It lists recently added items.
  """
  cats = db_session.query(Catalog).order_by(Catalog.name).all()
  items = db_session.query(Item).order_by(desc(Item.time_stamp)).limit(12)
  items_with_catagory = [get_item_info(item) for item in items]
  heading = "Latest Items" 
  is_loggedin = "username" in login_session
  return render_template("main.html", task="show_items", cats=cats, 
      items=items_with_catagory, heading=heading, is_loggedin=is_loggedin)

@app.route("/catalog/<catalog_name>/items")
def show_items_by_catalog(catalog_name):
  """
  This page displays all items of the specified catalory.

  Returns:
    a JSON object with proper error message if the url contains
    bad data.
  """
  cats = db_session.query(Catalog).order_by(Catalog.name).all() 
  # check if the specified catalog_name is valid
  try:
    cat = db_session.query(Catalog).filter_by(name = catalog_name).one()
  except:
    response = make_response(
      json.dumps("Invalid catalog name %s." % catalog_name), 401)
    response.headers["Content-Type"] = "application/json"
    return response
  items = db_session.query(Item).filter_by(catalog_id=cat.id).order_by(Item.name).all()
  items_with_catagory = [get_item_info(item) for item in items]
  heading = cat.name + "  (%d items)" % len(items)
  is_loggedin = "username" in login_session
  return render_template("main.html", task="show_items", cats=cats, 
      items=items_with_catagory, heading=heading, is_loggedin=is_loggedin)

@app.route("/item/catalog/<catalog_name>/<item_name>")
def show_iteminfo(catalog_name, item_name):
  """
  This page shows the description of the specified item.

  Returns:
    a JSON object with proper error message if the url contains
    bad data.
  """
  cats = db_session.query(Catalog).order_by(Catalog.name).all() 
  # check if the specified catalog_name is valid
  try:
    cat = db_session.query(Catalog).filter_by(name = catalog_name).one()
  except:
    response = make_response(
      json.dumps("Invalid catalog name."), 401)
    response.headers["Content-Type"] = "application/json"
    return response
  # check if the specified item_name is in the catalog
  try:
    item = db_session.query(Item).filter_by(catalog_id=cat.id).filter_by(name=item_name).one()
  except:
    response = make_response(
      json.dumps("The item %s is not in the catalog %s." % (item_name, catalog_name)), 401)
    response.headers["Content-Type"] = "application/json"
    return response
  heading = item.name
  is_loggedin = "username" in login_session
  is_owner = is_loggedin and login_session["email"] == get_item_owner(item).email
  return render_template("main.html", task="show_info", cats=cats, item=item, 
      heading=heading, is_loggedin=is_loggedin, is_owner=is_owner)

@app.route("/new", methods=["GET", "POST"])
def add_item():
  """
  This page shows input forms which allow registered users to add new items.

  Returns:
    a JSON object with proper error message if this process does not go through.
  """
  is_loggedin = "email" in login_session
  if not is_loggedin:
    return redirect(url_for("show_login"))
  if request.method == "POST":
    name = request.form["title"].strip(" ")
    # check if it is a valid item name
    if name == "":
      response = make_response(
        json.dumps("Invalid item name %s." % item_name), 401)
      response.headers["Content-Type"] = "application/json"
      return response
    # insert a new record into the database:w
    description = request.form["description"].strip(" ")
    author = request.form["author"].strip(" ")
    catalog_id = request.form["catalog"].strip(" ")
    picture = request.form["picture"].strip(" ")
    user_id = get_user_id(login_session["email"])
    new_item = Item(name=name, description=description, author=author, 
                        catalog_id=catalog_id, picture=picture, user_id=user_id)
    db_session.add(new_item)
    db_session.commit()
    return redirect(url_for("show_main"))
  else:
    cats = db_session.query(Catalog).order_by(Catalog.name).all() 
    heading="Add a new item"
    return render_template("main.html", cats=cats, task="show_new", heading=heading, 
        is_loggedin=is_loggedin)

@app.route("/item/catalog/<item_name>/edit", methods=["GET", "POST"])
def edit_item(item_name):
  """
  This page shows input forms which allow registered users to modify an item.

  Returns:
    a JSON object with proper error message if this process does not go through.
  """
  # check if the user is logged in
  is_loggedin = "email" in login_session
  if not is_loggedin:
    return redirect(url_for("show_login"))
  # check if the item is exist
  try:
    item = db_session.query(Item).filter_by(name=item_name).one()
  except:
    response = make_response(
      json.dumps("The item %s is unavailable." % (item_name)), 401)
    response.headers["Content-Type"] = "application/json"
    return response
  # check if the user is the owner of this item
  if login_session["email"] != get_item_owner(item).email:
    response = make_response(json.dumps("You are not authorized to modify this item."), 401)
    response.headers["Content-Type"] = "application/json"
    return response
  if request.method == "POST":
    name = request.form["title"].strip(" ")
    description = request.form["description"].strip(" ")
    author = request.form["author"].strip(" ")
    catalog_id = request.form["catalog"].strip(" ")
    picture = request.form["picture"].strip(" ")
    # check if it is a valid item name
    if name == "":
      response = make_response(
        json.dumps("Invalid item name %s." % item_name), 401)
      response.headers["Content-Type"] = "application/json"
      return response
    # update the record in the database with new values
    item.name = name
    item.description = description
    item.author = author
    item.catalog_id = int(catalog_id)
    item.picture = picture
    user_id = 1
    db_session.add(item)
    db_session.commit()
    return redirect(url_for("show_main"))
  else:
    # we initiate the input forms using the values in the database
    name = item.name
    description = item.description
    author = item.author
    catalog_id = item.catalog_id
    picture = item.picture
    cats  = db_session.query(Catalog).order_by(Catalog.name).all() 
    heading="Edit the title"
    is_loggedin = "username" in login_session
    return render_template("main.html", task="show_edit", cats=cats, name=name, 
        catalog_id=catalog_id, description=description, author=author, 
        picture=picture, heading=heading, is_loggedin=is_loggedin)

@app.route("/catalog/<item_name>/delete", methods=["GET", "POST"])
def delete_item(item_name):
  """
  This page shows deletion comfirmation about deleting an item from the database.

  Returns:
    a JSON object with proper error message if this process does not go through.
  """
  is_loggedin = "email" in login_session
  # check if the user is logged in
  if not is_loggedin:
    return redirect(url_for("show_login"))
  # check if the item is exist
  try:
    item = db_session.query(Item).filter_by(name=item_name).one()
  except:
    response = make_response(
      json.dumps("The item %s is unavailable." % (item_name)), 401)
    response.headers["Content-Type"] = "application/json"
    return response
  if login_session["email"] != get_item_owner(item).email:
  # check if the user is the owner of this item
    response = make_response(json.dumps("You are not authorized to modify this item."), 401)
    response.headers["Content-Type"] = "application/json"
    return response
  if request.method == "POST":
    # delete the respective record in the database
    db_session.delete(item)
    db_session.commit()
    return redirect(url_for("show_main"))
  else:
    cats  = db_session.query(Catalog).order_by(Catalog.name).all() 
    heading="Are you sure you want to delete \"%s\" ?" % item.name
    return render_template("main.html", task="show_delete", cats=cats, item=item, 
        heading=heading, is_loggedin=is_loggedin)

# Some Helper Functions
def create_user(login_session):
  """
  Insert a new user in the database

  Returns:
    The id of the new user.
  """
  new_user = User(name=login_session["username"], email=login_session["email"])
  db_session.add(new_user)
  db_session.commit()
  user = db_session.query(User).filter_by(email=login_session["email"]).one()
  return user.id

def get_user_info(user_id):
  """
    Get the user object.

    Args:
      user_id (int): the id of the user.

    Returns:
      The user object.
  """
  user = db_session.query(User).filter_by(id=user_id).one()
  return user

def get_user_id(email):
  """
    Get the user id.

    Args:
      email (string): the email address of the user.

    Returns:
      The user id if the user exsits.
  """
  try:
    user = db_session.query(User).filter_by(email=email).one()
    return user.id
  except:
    return None

def get_item_owner(item):
  """
    Get the owner of an item.

    Args:
      item (Item): the item object.

    Returns:
      The owner of the item.
  """
  owner = db_session.query(User).filter_by(id=item.user_id).one()
  return owner

def get_item_catalog(item):
  """
    Get the catalog of an item.

    Args:
      item (Item): the item object.

    Returns:
      The cotalog of the item.
  """
  cat = db_session.query(Catalog).filter_by(id=item.catalog_id).one()
  return cat

def get_item_info(item):
  """
    Get the information about the item.

    Args:
      item (Item): the item object.

    Returns:
      a dict contains the assciated infomation about the item including 
      its catalog.
  """
  out = {}
  cat = get_item_catalog(item)
  out["name"] = item.name
  out["catalog_name"] = cat.name
  out["picture"] = item.picture
  return out

if __name__ == "__main__":
  app.secret_key = "super_secret_key"
  app.debug = True
  app.run(host="0.0.0.0", port=8080)

