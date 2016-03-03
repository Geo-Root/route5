#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 03.03.2016
#@author: Alex Ferechin
#@contact: alex.ferechin@gmail.com

from flaskext.auth import permission_required
from flask import render_template, url_for, redirect, g, Response
from route5 import auth, google
from route5 import app, roles


@app.route('/login')
def login():
    callback=url_for('authorized', _external=True)
    return google.authorize(callback=callback)

@app.route('/logout')
def logout():
    session.clear()
    return render_template("error.html", error="You can login back")

@google.tokengetter
def get_access_token():
    return session.get('access_token')

@app.route('/authorized')
@google.authorized_handler
def authorized(resp):
    ''' Controller for handling google auth response.
    '''
    if 'access_token' in resp:
        access_token = resp['access_token']
        session['access_token'] = access_token, ''

        access_token = session.get('access_token')
        if access_token is None:
            return redirect("http://google.com") 
            # return render_template("error.html", error="Empty access token")

        access_token = access_token[0]
        headers = {'Authorization': 'OAuth '+access_token}
        req = Request('https://www.googleapis.com/oauth2/v1/userinfo',
                      None, headers)
        try:
            res = urlopen(req)
        except URLError, e:
            if e.code == 401:
                # Unauthorized - bad token
                session.pop('access_token', None)
                return redirect("http://google.com") 
                # return render_template("error.html", error="Error 401 from Google Auth")
            return redirect("http://google.com") 
            # return render_template("error.html", error="Something wrong %s" % str(e))
        data = res.read()
        data = simplejson.loads(data)
        username = data["email"]

        if username in g.users:
            if g.users[username].authenticate(username):
                flash("Welcome %s" % username)
                return redirect('/')
        flash("Wrong login or password")
        return redirect("http://google.com") 
        # return render_template("error.html", error="Wrong inner user auth")
    else:
        return redirect("http://google.com") 
        # return render_template("error.html", error="No access token in response %s" % str(resp))


def get_context():
	context = {}
	return context


### Main controllers
# @permission_required(resource='all', action='view')
def index():
    ''' Index page.
    '''
    d = get_context()
    return render_template('index.html', d=d)


app.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])
app.add_url_rule('/logout', 'logout', logout, methods=['GET', 'POST'])
app.add_url_rule('/authorized', 'authorized', authorized)
app.add_url_rule('/', 'index', index, methods=['GET'])

