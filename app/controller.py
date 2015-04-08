from flask import render_template, request,flash, redirect, url_for, abort
from app import app, db
from app.models import Post,Comment,Users, Terms
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import LoginManager, login_user,UserMixin, logout_user, login_required


#Main
@app.route('/' )
def index():
  post = Post.query.all()
  return render_template('index.html', post=post)


#End Main Content
#Posts
@app.route('/post/' )
@login_required
def post_index():
  post = Post.query.all()
  terms =Terms.query.all()
  return render_template('/post/index.html', post=post, terms=terms)

@app.route('/post/add' , methods=['POST', 'GET'])
@login_required
def post_add():
    terms=Terms.query.all()
    if request.method == 'POST':
        post=Post(request.form['author'],request.form['title'],request.form['content'], request.form['published'],request.form['category'])
        post_add=post.add(post)
        if not post_add:
                   flash("Add was successful")
                   return redirect(url_for('post_index'))
        else:
                   flash("Oops something went wrong")

    return render_template('/post/add.html', terms=terms)

@app.route('/post/update/<id>' , methods=['POST', 'GET'])
@login_required
def post_update (id):
    #Getting user by primary key:
    post = Post.query.get(id)
    error=query_error(post, post_index)
    if not error:
        terms=Terms.query.all()
        if request.method == 'POST':
            post.author=request.form['author']
            post.title = request.form['title']
            post.content =  request.form['content']
            post.published=request.form['published']
            post.category=request.form['category']
            post_update=post.update()
            if not post_update:
                   flash("Update was successful")
                   return redirect(url_for('post_index'))

            else:
                   flash("Oops something went wrong")

        return render_template('post/update.html', post=post, terms=terms)
    else:
          return error


@app.route('/delete/<id>' , methods=['POST', 'GET'])
@login_required
def post_delete (id):
     post = Post.query.get(id)
     error = query_error(post, post_index)
     if not error:
            post.delete(post)
            flash("Post was deleted successfully")
            return redirect(url_for('post_index'))
     else:
          return error




 #Comments
@app.route('/comment/' )
@login_required
def comment_index():
  comments = Comment.query.all()
  return render_template('/comment/index.html', comments=comments)

@app.route('/comment/add/<post_id>', methods=['POST', 'GET'])
@login_required
def comment_add(post_id):
    post = Post.query.get(post_id)
    error = query_error(post,comment_index)
    if not error:
        if request.method == 'POST':
           comment=Comment(request.form['author'], request.form['website'], request.form['content'],post_id,request.form['approved'])
           comment_add=comment.add(comment)
           if not comment_add:
               flash("Add was successful")
               return redirect(url_for('comment_index'))

           else:
               flash("Oops something went wrong")


        return render_template('comment/add.html', post_id=post_id)
    else:
        return error

@app.route('/comment/update/<id>', methods=['POST', 'GET'])
@login_required
def comment_update (id):
    comment = Comment.query.get(id)
    error = query_error(comment,comment_index)
    if not error:
        if request.method == 'POST':
            comment.author=request.form['author']
            comment.website=request.form['website']
            comment.content=request.form['content']
            comment.approved=request.form['approved']
            comment_update=comment.update()
            if comment_update == 'false':
               flash("Oops something went wrong")
            else:
               flash("Update was successful")
               return redirect(url_for('comment_index'))
        return render_template('comment/update.html', comment=comment)
    else:
        return error


@app.route('/comment/delete/<id>', methods=['POST', 'GET'])
@login_required
def comment_delete (id):
    comment = Comment.query.get(id)
    error = query_error(comment,comment_index)
    if not error:

            comment.delete(comment)
            flash("Comment was deleted successfully")
            return redirect(url_for('comment_index'))
    else:
          return error



#Users
@app.route('/user/' )
@login_required
def user_index():
  users = Users.query.all()
  return render_template('/user/index.html', users=users)

@app.route('/user/add' , methods=['POST', 'GET'])
@login_required
def user_add():
    if request.method == 'POST':
        name=request.form['name']
        email=request.form['email']
        password=generate_password_hash(request.form['password'])
        user=Users(email,password,name)
        return add(user, user_index, user_add)

    return render_template('/user/add.html')

@app.route('/user/update/<id>' , methods=['POST', 'GET'])
@login_required
def user_update (id):
    #Get user by primary key:
    user=Users.query.get(id)
    if user == None:
       return abort(404)
    if request.method == 'POST':
            user.email=request.form['email']
            user.password = request.form['password']
            user.name =  request.form['name']
            return update(user, user_index, user_update, id)

    return render_template('/user/update.html', user=user)



@app.route('/user/delete/<id>' , methods=['POST', 'GET'])
@login_required
def user_delete (id):
     user = Users.query.get(id)
     if user == None:
       return abort(404)
     return delete(user, user_index)




#START TERMS
@app.route('/terms/' )
@login_required
def term_index():
  terms = Terms.query.all()
  return render_template('/terms/index.html', terms=terms)

@app.route('/terms/add' , methods=['POST', 'GET'])
@login_required
def term_add():
     if request.method == 'POST':
        name=request.form['name']
        description=request.form['description']
        term=Terms(name,description)
        term_add=term.add(term)
        db_commit(term_add,term_index)

        return redirect(url_for('term_index'))


     return render_template('/terms/add.html')

@app.route('/terms/update/<id>' , methods=['POST', 'GET'])
@login_required
def term_update (id):
    #Getting user by primary key:
    term = Terms.query.get(id)
    error=query_error(term, term_index)
    if not error:
        if request.method == 'POST':
            term.name=request.form['name']
            term.description = request.form['description']
            term_update=term.update()
            db_commit(term_update, term_index)

        return render_template('terms/update.html', term=term)
    else:
          return error




@app.route('/terms/delete/<id>' , methods=['POST', 'GET'])
@login_required
def term_delete (id):
     term = Terms.query.get(id)
     error = query_error(term,term_index)
     if not error:
            term_delete=term.delete(term)
            #if does not return an error
            db_commit(term_delete, term_index)
            return redirect(url_for('term_index'))
     else:
          return error


#END TERMS

#Initialize the LoginManager from Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))

@app.route('/login', methods=['POST', 'GET'])
def login ():
  if request.method == 'POST':
    email=request.form['email']
    password=request.form['password']
    user=Users.query.filter_by(email=email).first()
    error=query_error(user,login)
    if not error:
        if check_password_hash(user.password,password):
          login_user(user)
          return redirect(url_for('post_index'))
        else:
         flash("invalid username/password")
    else:
        return error
  return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))



#End Login Manager

#CRUD FUNCTIONS
#Arguments  are data to add, function to redirect to if the add was successful and if not
def add (data, func1, func2):
    add = data.add(data)
    #if does not return any error
    if not add :
       flash("Add was successful")
       return redirect(url_for(str(func1.__name__)))
    else:
       message=add
       flash(message)
       return redirect(url_for(str(func2.__name__)))


def update (data, func1, func2, id):

            update=data.update()
            #if does not return any error
            if not update :
              flash("Update was successful")
              return redirect(url_for(str(func1.__name__)))
            else:
               message=update
               flash(message)
               return redirect(url_for(str(func2.__name__), id=id))



def delete (data, func1):
     delete=data.delete(data)
     if not delete :
              flash("Delete was successful")

     else:
          message=delete
          flash(message)
     return redirect(url_for(str(func1.__name__)))



#Errors
def db_commit(data,func):
    #if does not return an error
    if not data:
       flash("Great Success")
       return redirect(url_for(str(func.__name__)))
    else:
       message=data
       flash(message)

def query_error(var,func):
  if var == None:
      flash("This entry does not exist in the database")
      return redirect(url_for(str(func.__name__)))
