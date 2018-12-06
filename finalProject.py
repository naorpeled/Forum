from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Posts, Categories, Users, Comments
import datetime

app = Flask(__name__)

engine = create_engine('sqlite:///forum_database.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)


@app.route('/')
@app.route('/categories')
def showCategories():
    session = DBSession()
    categories = session.query(Categories).all()
    session.close()
    return render_template('categories.html', categories=categories)


@app.route('/categories/new', methods=['GET', 'POST'])
def createCategory():
    if request.method == 'POST':
        session = DBSession()
        newCategory = Categories(name=request.form['title'])
        if (session.query(Categories).
            filter_by(name=request.form['title']).first()) == None:
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


@app.route('/categories/<int:category_id>')
def showCategoryPosts(category_id):
    session = DBSession()
    category = session.query(Categories).filter_by(id=category_id).one()
    posts = session.query(Posts).filter_by(category_id=category_id)
    session.close()
    return render_template('posts.html', category = category, posts = posts)


@app.route('/categories/<int:category_id>/edit')
def editCategory(category_id):
  output = ""
  output += "Editing category #"
  output += str(category_id)
  return output


@app.route('/categories/<int:category_id>/delete')
def deleteCategory(category_id):
  output = ""
  output += "Deleting category #"
  output += str(category_id)
  return output


@app.route('/categories/<int:category_id>/<int:post_id>', methods=['GET', 'POST'])
def showPost(category_id, post_id):
    if request.method == 'POST':
        session = DBSession()
        newComment = Comments(content=request.form['content'], post_id=post_id, time=datetime.datetime.now())
        session.add(newComment)
        session.commit()
        session.close()
        return redirect(url_for('showPost', category_id=category_id, post_id=post_id))
    session = DBSession()
    category = session.query(Categories).filter_by(id=category_id).one()
    post = session.query(Posts).filter_by(id=post_id).one()
    comments = session.query(Comments).filter_by(post_id=post_id).all()
    users = session.query(Users).all()  
    session.close()
    return render_template('post.html', category = category, post = post, users=users ,comments = comments)


@app.route('/categories/<int:category_id>/add', methods=['GET', 'POST'])
def addPost(category_id):
    if request.method == 'POST':
            session = DBSession()
            newPost = Posts(title=request.form['title'], content=request.form[
                               'content'], category_id=category_id, time=datetime.datetime.now())
            session.add(newPost)
            session.commit()
            session.close()
            return redirect(url_for('showCategoryPosts', category_id=category_id))
    else:
            return render_template('newPost.html', category_id=category_id)

@app.route('/categories/<int:category_id>/edit/<int:post_id>')
def editPost(category_id, post_id):
  output = ""
  output += "Editing Post #"
  output += str(post_id)
  output += "in category #"
  output += str(category_id)
  return output  


@app.route('/categories/<int:category_id>/delete/<int:post_id>')
def deletePost(category_id, post_id):
  output = ""
  output += "Deleting Post #"
  output += str(post_id)
  output += "in category #"
  output += str(category_id)
  return output


@app.route('/login')
def login():
  return 'Log in here'


@app.route('/logout')
def logout():
  return 'Log out here'

@app.route('/register')
def registerUser():
  return 'Register here'


@app.route('/admin')
def showAdminPanel():
    return 'Admin panel here'


@app.route('/profiles/<int:user_id>/')
def showUserProfile(user_id):
    return 'Showing user details here'


def searchUserPhotoURL(user_id):
    session = DBSession()
    url = session.query(Users).filter_by(id=user_id).one().photoURL
    session.close()
    return url


if __name__ == '__main__':
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000)