#!/usr/bin/env python2

from flask import Flask, render_template, request, redirect, url_for, flash
from flask import jsonify

from sqlalchemy import create_engine, desc
from sqlalchemy.sql import exists
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, User, Item

from flask import session as login_session
import random
import string

from datetime import datetime

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

engine = create_engine(
    'sqlite:///catalog.db',
    connect_args={'check_same_thread': False},
)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Decorator for functions that require login
def login_required(func):
    def wrapped(*args, **kwargs):
        if 'username' not in login_session:
            return redirect('/login')
        return func(*args, **kwargs)
    wrapped.func_name = func.func_name
    return wrapped


# Show the login page
@app.route('/login')
def showLogin():
    state = ''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for x in xrange(32)
        )
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# Handle the POST request from client with the token from Google
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the acess token is not saved and user hasn't logged in yet
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'),
            200
            )
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    # Save user info in the session for later use
    login_session['username'] = data['name']
    login_session['email'] = data['email']

    # Create user object in database if it doesn't already exist
    email = login_session["email"]
    result = session.query(exists().where(User.email == email)).scalar()
    if not result:
        new_user = User(
            name=login_session["username"],
            email=login_session["email"],
        )
        session.add(new_user)
        session.commit()

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    flash("you are now logged in as %s" % login_session['username'])
    return output


@app.route('/gdisconnect')
def gdisconnect():
    # Verify the user is not already logged out
    access_token = login_session['access_token']
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'),
            401
            )
        response.headers['Content-Type'] = 'application/json'
        return response

    # Revoke the token at Google side
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % \
        login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    # Delete data saved in login_session
    del login_session['access_token']
    del login_session['gplus_id']
    del login_session['username']
    del login_session['email']

    # Check if revoking token from Google is successful or not.
    if result['status'] == '200':
        return redirect('/')
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400)
            )
        response.headers['Content-Type'] = 'application/json'
        return response


# Show the page for all categories
@app.route('/', methods=['GET'])
def show_all_categories():
    categories = session.query(Category).all()
    latest_items = session \
        .query(Item) \
        .order_by(desc(Item.time_added)) \
        .limit(9) \
        .all()
    return render_template(
        "show_all_categories.html",
        categories=categories,
        latest_items=latest_items
        )


# Add new item (Create)
@app.route('/catalog/add', methods=['GET', 'POST'])
@login_required
def add_item():
    categories = session.query(Category).all()
    # Handle the POST request to add item
    if request.method == 'POST':
        if request.form["item_name"] and request.form["category"]:
            user_id = session \
                .query(User) \
                .filter_by(email=login_session["email"]) \
                .one() \
                .id
            item = Item(
                name=request.form["item_name"],
                category_name=request.form["category"],
                description=request.form["description"],
                time_added=datetime.now(),
                user_id=user_id,
            )
            session.add(item)
            session.commit()
        return redirect(url_for('show_all_categories'))
    # Handle the GET request
    else:
        return render_template(
            'add_item.html',
            categories=categories,
        )


# Show all the items of a category
@app.route('/catalog/<string:category_name>/items', methods=['GET'])
def show_items(category_name):
    categories = session.query(Category).all()
    category_items = session.query(Item) \
        .filter_by(category_name=category_name) \
        .all()
    count = len(category_items)
    return render_template(
        "show_category_items.html",
        categories=categories,
        count=count,
        category_name=category_name,
        category_items=category_items,
    )


# Show the description page of an item
@app.route(
    '/catalog/<string:category_name>/<string:item_name>',
    methods=['GET']
    )
def show_item_description(category_name, item_name):
    item = session.query(Item).filter_by(name=item_name).one()
    logged_in = "username" in login_session
    return render_template(
        "show_item_description.html",
        item_name=item_name,
        item=item,
        logged_in=logged_in,
    )


# Edit an item
@app.route('/catalog/<string:item_name>/edit', methods=['GET', 'POST'])
@login_required
def edit_item(item_name):
    # Find the user that created this item
    item = session.query(Item).filter_by(name=item_name).one()
    categories = session.query(Category).all()
    # Verify the user is the one creating the item to be edited
    user = session.query(User).filter_by(id=item.user_id).one()
    if user.email != login_session['email']:
        script_to_return = (
            "<script>function myFunction() "
            "{alert('You are not authorized to edit this item. "
            "Please create your own item in order to edit.');}"
            "</script><body onload='myFunction()'>"
            )
        return script_to_return
    if request.method == 'POST':
        if request.form.get("new_item_name") and request.form.get("category"):
            item.name = request.form.get("new_item_name")
            item.category_name = request.form.get("category")
            item.description = request.form.get("new_description")
            item.time_added = datetime.now()
            session.add(item)
            session.commit()
        return redirect(url_for('show_all_categories'))
    else:
        return render_template(
            'edit_item.html',
            item_name=item_name,
            item=item,
            categories=categories,
        )


@app.route('/catalog/<string:item_name>/delete', methods=['GET', 'POST'])
@login_required
def delete_item(item_name):
    # Find the user that created this item
    item = session.query(Item).filter_by(name=item_name).one()
    user = session.query(User).filter_by(id=item.user_id).one()
    # Verify the user is the one creating the item to be edited
    if user.email != login_session['email']:
        script_to_return = (
            "<script>function myFunction() "
            "{alert('You are not authorized to delete this item. "
            "Please create your own item in order to delete.');}"
            "</script><body onload='myFunction()'>"
            )
        return script_to_return
    if request.method == "POST":
        session.delete(item)
        session.commit()
        return redirect(url_for('show_all_categories'))
    else:
        return render_template(
            "delete_item.html",
            item_name=item_name,
        )


@app.route('/catalog.json')
def category_json():
    categories = session.query(Category).all()
    return jsonify(Category=[i.serialize for i in categories])


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
