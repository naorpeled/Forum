from flask import Flask, render_template, request
from flask import redirect, url_for, jsonify, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Posts, Categories, Users, Comments
import datetime
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
from flask import session as login_session

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Forum Project"

app = Flask(__name__)

engine = create_engine('sqlite:///forum_database.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)


@app.route('/')
@app.route('/categories', methods=['GET', 'POST'])
def showCategories():
    session = DBSession()
    categories = session.query(Categories).all()
    if request.method == 'POST':
        searchKeyword = '%'
        searchKeyword += request.form['keyword']
        searchKeyword += '%'
        filtered = session.query(Categories).filter(
                                    Categories.name.like(searchKeyword)).all()
        return render_template('categories.html', categories=filtered)
    session.close()
    return render_template('categories.html', categories=categories)


@app.route('/JSON')
@app.route('/categories/JSON')
def showCategoriesJSON():
    session = DBSession()
    categories = session.query(Categories).all()
    session.close()
    return jsonify(categories=[r.serialize for r in categories])


@app.route('/categories/new', methods=['GET', 'POST'])
def createCategory():
    if not login_session['user_id']:
        flash("Please login first")
        return redirect(url_for('login'))
    elif str(login_session['user_rank']) == str(0):
        flash("In order to create a category you must be an admin.")
        return redirect(url_for('showCategories'))
    elif str(login_session['user_rank']) == str(1):
        if request.method == 'POST':
            session = DBSession()
            newCategory = Categories(name=request.form['title'])
            cond = session.query(Categories).filter_by(
                                             name=request.form['title'])
            if cond.first() is None:
                session.add(newCategory)
                session.commit()
                flash('Category added!')
                session.close()
                return redirect(url_for('showCategories'))
            else:
                flash('Category with that name already exists')
                return redirect(url_for('createCategory'))
        else:
            return render_template('newCategory.html')


@app.route('/categories/<int:category_id>', methods=['GET', 'POST'])
def showCategoryPosts(category_id):
    session = DBSession()
    category = session.query(Categories).filter_by(id=category_id).one()
    users = session.query(Users).all()
    posts = session.query(Posts).filter_by(category_id=category_id)
    if request.method == 'POST':
        searchKeyword = '%'
        searchKeyword += request.form['keyword']
        searchKeyword += '%'
        filtered_posts = session.query(Posts).filter(
                                Posts.title.like(searchKeyword)).all()
        session.close()
        return render_template('posts.html',
                               category_id=category.id,
                               category=category,
                               posts=filtered_posts,
                               users=users)
    session.close()
    return render_template('posts.html',
                           category_id=category.id,
                           category=category,
                           posts=posts,
                           users=users)


@app.route('/categories/<int:category_id>/JSON')
def showCategoryPostsJSON(category_id):
    session = DBSession()
    category = session.query(Categories).filter_by(id=category_id).one()
    posts = session.query(Posts).filter_by(
        category_id=category_id).all()
    return jsonify(posts=[i.serialize for i in posts])


@app.route('/categories/<int:category_id>/edit', methods=['GET', 'POST'])
def editCategory(category_id):
    session = DBSession()
    oldCategory = session.query(Categories).filter_by(
                                           id=category_id).first()
    if not login_session:
        flash("Please login first")
        return redirect(url_for('login'))
    if str(login_session['user_rank']) == str(0):
        flash("In order to edit a category you must be an admin")
        return redirect(url_for('showCategories'))
    elif str(login_session['user_rank']) == str(1):
        if request.method == 'POST':
            cond = session.query(Categories).filter_by(
                                             name=request.form['title'])
            if cond.first() is None:
                oldCategory.name = request.form['title']
                session.add(oldCategory)
                session.commit()
                flash('Category name changed!')
                session.close()
                return redirect(url_for('showCategories'))
            else:
                flash('Category with that name already exists')
                return redirect(url_for('editCategory',
                                        category_id=category_id))
        else:
            session.close()
            return render_template('editCategory.html', category=oldCategory)


@app.route('/categories/<int:category_id>/delete', methods=['GET', 'POST'])
def deleteCategory(category_id):
    session = DBSession()
    category = session.query(Categories).filter_by(
                                           id=category_id).first()
    if not login_session:
        flash("Please login first")
        return redirect(url_for('login'))
    if str(login_session['user_rank']) == str(0):
        flash("In order to edit a category you must be an admin")
        return redirect(url_for('showCategories'))
    elif str(login_session['user_rank']) == str(1):
        if request.method == 'POST':
                session.delete(category)
                session.commit()
                message = 'Category \''
                message += str(category.name)
                message += '\' was successfully deleted!'
                flash(message)
                session.close()
                return redirect(url_for('showCategories'))
        else:
            session.close()
            return render_template('deleteCategory.html', category=category)


@app.route('/categories/<int:category_id>/<int:post_id>',
           methods=['GET', 'POST'])
def showPost(category_id, post_id):
    if request.method == 'POST':
        if login_session['user_id']:
            session = DBSession()
            newComment = Comments(content=request.form['content'],
                                  post_id=post_id,
                                  author_id=login_session['user_id'],
                                  time=datetime.datetime.now())
            session.add(newComment)
            session.commit()
            session.close()
            return redirect(url_for('showPost', category_id=category_id,
                                    post_id=post_id))
        else:
            flash("You aren't logged in.")
            flash("Please log in in roder to write a comment")
            return redirect(url_for('login'))
    session = DBSession()
    category = session.query(Categories).filter_by(id=category_id).one()
    post = session.query(Posts).filter_by(id=post_id).one()
    comments = session.query(Comments).filter_by(post_id=post_id).all()
    users = session.query(Users).all()
    session.close()
    return render_template('post.html',
                           category=category,
                           post=post,
                           users=users,
                           comments=comments)


@app.route('/categories/<int:category_id>/<int:post_id>/JSON')
def showPostJSON(category_id, post_id):
    session = DBSession()
    post = session.query(Posts).filter_by(id=post_id).one()
    session.close()
    return jsonify(post=post.serialize)


@app.route('/categories/<int:category_id>/add', methods=['GET', 'POST'])
def addPost(category_id):
    session = DBSession()
    if request.method == 'POST':
        if login_session:
            newPost = Posts(title=request.form['title'],
                            content=request.form[
                            'content'],
                            category_id=category_id,
                            time=datetime.datetime.now(),
                            author_id=login_session['user_id'])
            session.add(newPost)
            session.commit()
            session.close()
            return redirect(url_for('showCategoryPosts',
                                    category_id=category_id))
        else:
            flash("Please login in order to create a new post")
            return redirect(url_for('login'))
    else:
            categoryName = session.query(Categories).filter_by(
                                                        id=category_id)
            session.close()
            return render_template('newPost.html',
                                   category_id=category_id,
                                   categoryName=categoryName.one().name)


@app.route('/categories/<int:category_id>/edit/<int:post_id>',
           methods=['GET', 'POST'])
def editPost(category_id, post_id):
    session = DBSession()
    oldPost = session.query(Posts).filter_by(
                                id=post_id,
                                category_id=category_id).first()
    if oldPost.author_id != login_session['user_id']:
        flash("You cannot edit posts that aren't yours")
        return redirect(url_for('showCategoryPosts', category_id=category_id))
    if request.method == 'POST':
            oldPost.title = request.form['title']
            oldPost.content = request.form['content']
            session.add(oldPost)
            session.commit()
            flash('The post was successfully edited!')
            session.close()
            return redirect(url_for('showCategoryPosts',
                                    category_id=category_id))
    else:
        session.close()
        return render_template('editPost.html', post=oldPost)


editCommentURL = ''
editCommentURL += '/categories/<int:category_id>/'
editCommentURL += '<int:post_id>/editComment/<int:comment_id>'


@app.route(editCommentURL,
           methods=['GET', 'POST'])
def editComment(category_id, post_id, comment_id):
    session = DBSession()
    currentCategory = session.query(Categories).filter_by(
                                                id=category_id).first()
    allComments = session.query(Comments).filter_by(post_id=post_id).all()
    currentPost = session.query(Posts).filter_by(id=post_id).first()
    users = session.query(Users).all()
    oldComment = session.query(Comments).filter_by(
                                     id=comment_id).first()
    if oldComment.author_id != login_session['user_id']:
        flash("You cannot edit comments that aren't yours")
        return redirect(url_for('showPost',
                                category_id=category_id,
                                post_id=post_id))
    if request.method == 'POST':
            oldComment.content = request.form['content']
            session.add(oldComment)
            session.commit()
            flash('The comment was successfully edited!')
            session.close()
            return redirect(url_for('showPost',
                                    post_id=post_id,
                                    category_id=category_id))
    else:
        session.close()
        return render_template('editComment.html',
                               category=currentCategory,
                               users=users,
                               post=currentPost,
                               comments=allComments,
                               comment_id=comment_id)


@app.route('/categories/<int:category_id>/delete/<int:post_id>',
           methods=['GET', 'POST'])
def deletePost(category_id, post_id):
    session = DBSession()
    category = session.query(Categories).filter_by(
                                           id=category_id).first()
    post = session.query(Posts).filter_by(
                                  id=post_id).first()
    if post.author_id != login_session['user_id']:
        flash("You cannot delete posts that aren't yours")
        return redirect(url_for('showCategoryPosts', category_id=category_id))
    if request.method == 'POST':
            session.delete(post)
            session.commit()
            message = 'The post titled \''
            message += str(post.title)
            message += '\' was successfully deleted!'
            flash(message)
            session.close()
            return redirect(url_for('showCategoryPosts',
                                    category_id=category_id))
    else:
        session.close()
        return render_template('deletePost.html', category=category, post=post)


deleteCommentURL = ''
deleteCommentURL += '/categories/<int:category_id>/<int:post_id>'
deleteCommentURL += '/deleteComment/<int:comment_id>'


@app.route(deleteCommentURL,
           methods=['GET', 'POST'])
def deleteComment(category_id, post_id, comment_id):
    session = DBSession()
    comment = session.query(Comments).filter_by(
                                           id=comment_id).first()
    if comment.author_id != login_session['user_id']:
        if str(login_session['user_rank']) != str(1):
            flash("You cannot delete comments that aren't yours")
            return redirect(url_for('showPost',
                                    category_id=category_id,
                                    post_id=post_id))
    if request.method == 'POST':
            session.delete(comment)
            session.commit()
            message = 'The comment was successfully deleted!'
            flash(message)
            session.close()
            return redirect(url_for('showPost',
                                    post_id=post_id,
                                    category_id=category_id))
    else:
        session.close()
        return render_template('deleteComment.html',
                               category_id=category_id,
                               post_id=post_id,
                               comment_id=comment_id)


@app.route('/login', methods=['GET'])
def login():
        state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                        for x in xrange(32))
        login_session['state'] = state
        return render_template('login.html', STATE=state)


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?'
    url += 'grant_type=fb_exchange_token&client_id='
    url += app_id
    url += '&client_secret='
    url += app_secret
    url += '&fb_exchange_token='
    url += access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"

    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = 'https://graph.facebook.com/v2.8/me?access_token='
    url += token
    url += '&fields=name,id,email'
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # Get user picture
    url = 'https://graph.facebook.com/v2.8/me/picture?access_token='
    url += token
    url += '&redirect=0&height=200&width=200'
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    login_session['user_rank'] = getUserRank(user_id)
    output = '-'
    flash("Now logged in as %s" % login_session['username'])
    return output


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
    url = 'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token='
    url += access_token
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
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
                        json.dumps('Current user is already connected.'),
                        200)
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

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    login_session['user_rank'] = getUserRank(user_id)

    output = '-'
    flash("You are now logged in as %s" % login_session['username'])
    return output


# User Helper Functions


def createUser(login_session):
    session = DBSession()
    newUser = Users(name=login_session['username'], email=login_session[
                   'email'], photoURL=login_session['picture'], rank=0)
    session.add(newUser)
    session.commit()
    user = session.query(Users).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    session = DBSession()
    user = session.query(Users).filter_by(id=user_id).one()
    return user


def getUserRank(user_id):
    session = DBSession()
    user = session.query(Users).filter_by(id=user_id).one()
    return user.rank


def getUserID(email):
    session = DBSession()
    try:
        user = session.query(Users).filter_by(email=email).one()
        return user.id
    except LookupError:
        return None

# DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/disconnect')
def disconnect():
    if not login_session['provider']:
        return redirect(url_for('showCategories'))
    if login_session['provider'] == 'facebook':
        facebook_id = login_session['facebook_id']
        # The access token must me included to successfully logout
        access_token = login_session['access_token']
        url = 'https://graph.facebook.com/'
        url += facebook_id
        url += '/permissions?access_token='
        url += access_token
        h = httplib2.Http()
        result = h.request(url, 'DELETE')[1]
        login_session.clear()
        flash("You have been logged out")
        return redirect(url_for('showCategories'))
    elif login_session['provider'] == 'google':
        access_token = login_session.get('access_token')
        if access_token is None:
            response = make_response(
                                    json.dumps(
                                            'Current user not connected'), 401)
            response.headers['Content-Type'] = 'application/json'
            flash("Current user not connected")
            return redirect(url_for('showCategories'))
        url = 'https://accounts.google.com/o/oauth2/revoke?token='
        url += access_token
        print(access_token)
        h = httplib2.Http()
        result = h.request(url, 'GET')[0]
        if result['status'] == '200':
            login_session.clear()
            response = make_response(json.dumps(
                        'Successfully disconnected.'), 200)
            response.headers['Content-Type'] = 'application/json'
            flash("You have been logged out")
            return redirect(url_for('showCategories'))
        else:
            response = make_response(json.dumps(
                            'Failed to revoke token for given user.', 400))
            response.headers['Content-Type'] = 'application/json'
            flash("Failed to revoke token")
            login_session.clear()
            return redirect(url_for('showCategories'))


@app.route('/profiles/<int:user_id>/',
           methods=["GET", "POST"])
def showUserProfile(user_id):
    session = DBSession()
    user = session.query(Users).filter_by(id=user_id).one_or_none()
    if user is None:
        session.close()
        flash("User not found")
        return redirect(url_for('showCategories'))
    user_posts = session.query(Posts).filter_by(author_id=user_id).all()
    if request.method == "POST":
        newUser = session.query(Users).filter_by(id=user_id).first()
        newBio = request.form['bio']
        newUser.bio = str(newBio)
        session.add(user)
        session.commit()
    return render_template('profile.html', user=user, user_posts=user_posts)


if __name__ == '__main__':
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
