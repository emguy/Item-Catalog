from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Catalog, User,Item

# required by Flask
app = Flask(__name__)

# required by sqlalchemy
engine = create_engine('sqlite:///items.db') # here, we specifies the sqlite db file
Base.metadata.bind = engine # used only once
DBSession = sessionmaker(bind=engine) # used only once
db_session = DBSession() # we only need this handler for all database interactions

def parse_item(item):
  """
  Add two fields---"catalog_name" and "name_no_space" to the item. It repaces
  spaces in the generated URL with "\%20".

  """
  out = {}
  cat = db_session.query(Catalog).filter_by(id=item.catalog_id).one()
  out['name'] = item.name
  out['name_no_space'] = item.name.replace(" ", "%20")
  out['catalog_name'] = cat.name
  return out

# this is the only JSON endpoint
@app.route('/catalog.json')
def get_json():
  cats = db_session.query(Catalog).all() 
  out = [cat.serialize for cat in cats]
  for entry in out:
    id = entry['id']
    items = db_session.query(Item).filter_by(catalog_id=id).all()
    entry['items'] = [i.serialize for i in items]
  return jsonify(Catalog=out)

# this is the endpoint for the root URL
@app.route('/')
def show_main():
  cats = db_session.query(Catalog).all()
  items = db_session.query(Item).order_by(desc(Item.time_stamp)).limit(10)
  items_ = [parse_item(item) for item in items]
  heading = "Latest Items"
  return render_template('main.html', cats=cats, items=items_, heading=heading)

@app.route('/catalog/<catalog_name>/items')
def show_items(catalog_name):
  cats  = db_session.query(Catalog).all() 
  cat = db_session.query(Catalog).filter_by(name = catalog_name).one()
  items = db_session.query(Item).filter_by(catalog_id = cat.id).all()
  items_ = [parse_item(item) for item in items]
  heading = cat.name + "  (%d items)" % len(items)
  return render_template('catalog.html', cats=cats, items=items_, heading=heading)

@app.route('/item/catalog/<catalog_name>/<item_name>')
def show_iteminfo(catalog_name, item_name):
  item_name = item_name.replace("%20", u" ")
  cats  = db_session.query(Catalog).all() 
  cat = db_session.query(Catalog).filter_by(name = catalog_name).one()
  item = db_session.query(Item).filter_by(name=item_name).one()
  item_ = parse_item(item) # this is for replaciing spaces in urls with %20
  return render_template('item_info.html', cats=cats, item=item, item_=item_)

@app.route('/new', methods=['GET', 'POST'])
def new_item():
  if request.method == 'POST':
    name = request.form['title'].strip(' ')
    description = request.form['description'].strip(' ')
    author = request.form['author'].strip(' ')
    catalog_id = request.form['catalog'].strip(' ')
    picture = request.form['picture'].strip(' ')
    user_id = 1
    new_item = Item(name=name, description=description, author=author, 
                        catalog_id=catalog_id, picture=picture, user_id=user_id)
    db_session.add(new_item)
    db_session.commit()
    return redirect(url_for('show_main'))
  else:
    cats  = db_session.query(Catalog).all() 
    return render_template('new_item.html', cats=cats)

@app.route('/item/catalog/catalog/<item_name>/edit', methods=['GET', 'POST'])
def edit_item(item_name):
  item_name = item_name.replace("%20", " ")
  item = db_session.query(Item).filter_by(name=item_name).one()
  if request.method == 'POST':
    name = request.form['title'].strip(' ')
    description = request.form['description'].strip(' ')
    author = request.form['author'].strip(' ')
    catalog_id = request.form['catalog'].strip(' ')
    picture = request.form['picture'].strip(' ')
    item.name = name
    item.description = description
    item.author = author
    item.catalog_id = int(catalog_id)
    item.picture = picture
    user_id = 1
    db_session.add(item)
    db_session.commit()
    return redirect(url_for('show_main'))
  else:
    name = item.name
    description = item.description
    author = item.author
    catalog_id = item.catalog_id
    picture = item.picture
    cats  = db_session.query(Catalog).all() 
    return render_template('edit_item.html', cats=cats, name=name, catalog_id=catalog_id,
            description=description, author=author, picture=picture)

#@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete',
#           methods=['GET', 'POST'])
#def deleteMenuItem(restaurant_id, menu_id):
#    itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
#    if request.method == 'POST':
#        session.delete(itemToDelete)
#        session.commit()
#        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
#    else:
#        return render_template('deleteconfirmation.html', item=itemToDelete)

if __name__ == '__main__':
    #app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
