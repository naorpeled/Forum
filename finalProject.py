from flask import Flask
app = Flask(__name__)

@app.route('/')
@app.route('/categories')
def showCategories():
    return 'Show all categories here'

@app.route('/categories/new')
def createCategory():
  return 'Create a new category here'

@app.route('/categories/<int:category_id>')
def showCategoryPosts(category_id):
  output = ""
  output += "Showing category #"
  output += str(category_id)
  return output

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

@app.route('/categories/<int:category_id>/add')
def addPost(category_id):
  output = ""
  output += "Adding Post "
  output += "in category #"
  output += str(category_id)
  return output

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

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)