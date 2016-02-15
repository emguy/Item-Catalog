# Item Catalog
This web application provides an interface for its end-users to make there own
catalogs with items inside them. It requires users' google plus account for the
authentication. All user data are stored in a SQLite database on the server
side.

# Requirements
You need SQLite library and a python 2.x interpretor with the following modules:

1. [sqlalchemy](http://www.sqlalchemy.org)
2. [Flask](http://flask.pocoo.org)
3. [oauth2client](https://github.com/google/oauth2client)
4. [requests](http://docs.python-requests.org)
5. [httplib2](https://github.com/jcgregorio/httplib2)

# File structures
```
  templates/              (Contains all raw html files.)
  static/style.css        (The css file for styling.)
  web_server.py           (The server side python code.)
  data_setup.py           (The python code for setting up the database.)
  lotsofitems.py          (This python code pre-loads the database with some initial items.)
  item.db                 (The sqlite3 database storing all user data)
```

# Database structures
```
  The table (user) contains a list of registered users.

     id   |  name  |  email
  --------------------------------------
     1    | user_1 |
     2    | user_2 |
     3    | user_3 |

  The table (catalog) contains a list of book catalogs.

     id   |  name
  --------------------------------------
     1    | classic
     2    | mystery
     3    | kids

  The table (item) contains a list of book catalogs.

     id   |  name   | author | description | picture | time_stamp | catalog_id | user_id
  ----------------------------------------------------------------------------------------
     1    | title 1 |        |             |         |            |    3       |  1
     2    | title 2 |        |             |         |            |    2       |  1
     3    | title 3 |        |             |         |            |    5       |  1

```

# Usage
To initiate the database, execute the following command
```
  python database_setup.py

```
To run the server side application, execute the following command
```
  python web_server.py

```
To preload the database with sample items, execute the following command
```
  python lotsofitems.py

```
On the client side, the web server is settled at
```
  http://localhost:5000
```

Report bugs to Yu Zhang (emguy2000@gmail.com).
