from flask import render_template, request,flash, redirect, url_for, abort
from app import app, db
from app.models import Posts,Comment,Users, Terms
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import LoginManager, login_user,UserMixin, logout_user, login_required
from slugify import slugify



##Main Content Begins##
#Main index page
@app.route('/' )
def index():
  post = Posts.query.all()
  return render_template('index.html', post=post)

#Single Post
@app.route('/post/<id>/<slug>' )
def single_post(id,slug):
  post = Posts.query.get_or_404(id)
  return render_template('single.html', post=post)

##End Main Content##


#Posts
@app.route('/post/' )
@login_required
def post_index():
  post = Posts.query.all()
  terms =Terms.query.all()
  return render_template('/post/index.html', post=post, terms=terms)

@app.route('/post/add' , methods=['POST', 'GET'])
@login_required
def post_add():
    terms=Terms.query.all()
    if request.method == 'POST':
        slug=slugify(request.form['slug'])
        post=Posts(request.form['author'], request.form['title'], slug, request.form['content'], request.form['status'], request.form['post_type'])
        term_ids=request.form.getlist('term_id')
        for id in term_ids:
           term=Terms.query.get(id)
           post.terms.append(term)


        return add(post, post_index, post_add)

    return render_template('/post/add.html', terms=terms)

@app.route('/post/update/<id>' , methods=['POST', 'GET'])
@login_required
def post_update (id):
    post = Posts.query.get_or_404(id)
    post_terms=[]
    for term in post.terms:
        post_terms.append(term.id)
    terms=Terms.query.all()
    if request.method == 'POST':
            post.author=request.form['author']
            post.title = request.form['title']
            post.slug = slugify(request.form['slug'])
            post.content =  request.form['content']
            post.status=request.form['status']
            post.post_type=request.form['post_type']
            new_post_terms=request.form.getlist('term_id')
            #Add new post terms
            for term_id in new_post_terms:
                if term_id not in post_terms:
                  term=Terms.query.get(term_id)
                  post.terms.append(term)
            #Remove old post terms which are not included in the update.
            for post_term_id in post_terms:
                if post_term_id not in new_post_terms:
                      term=Terms.query.get(post_term_id)
                      post.terms.remove(term)

            return update(post, post_index, post_update, id)

    return render_template('post/update.html', post=post, terms=terms, post_terms=post_terms)

@app.route('/post/delete/<id>' , methods=['POST', 'GET'])
@login_required
def post_delete (id):
     post = Posts.query.get_or_404(id)
     return delete(post, post_index)

#Comments
@app.route('/comment/' )
@login_required
def comment_index():
  comments = Comment.query.all()
  return render_template('/comment/index.html', comments=comments)


@app.route('/comment/add/<post_id>', methods=['POST'])
@login_required
def comment_add(post_id):
    post = Posts.query.get(post_id)
    if request.method == 'POST':
           comment=Comment(request.form['author'], request.form['website'], request.form['content'],post_id,request.form['approved'])
           comment_add=comment.add(comment)
           if not comment_add:
               flash("Add was successful")
           else:
               flash("Oops something went wrong")
           return redirect(url_for('single_post', id=post.id, slug=post.slug))


@app.route('/comment/update/<id>', methods=['POST', 'GET'])
@login_required
def comment_update (id):
    comment = Comment.query.get_or_404(id)
    if request.method == 'POST':
            comment.author=request.form['author']
            comment.website=request.form['website']
            comment.content=request.form['content']
            comment.approved=request.form['approved']
            return update(comment, comment_index, comment_update, id)


    return render_template('comment/update.html', comment=comment)


@app.route('/comment/delete/<id>', methods=['POST', 'GET'])
@login_required
def comment_delete (id):
    comment = Comment.query.get_or_404(id)
    return delete(comment, comment_index)

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
    user=Users.query.get_or_404(id)
    if request.method == 'POST':
            user.email = request.form['email']
            user.name =  request.form['name']
            if not request.form['password'] :
              return update(user, user_index, user_update, id)
            else:
              user.password = generate_password_hash(request.form['password'])
              return update(user, user_index, user_update, id)              

    return render_template('/user/update.html', user=user)



@app.route('/user/delete/<id>' , methods=['POST', 'GET'])
@login_required
def user_delete (id):
     user = Users.query.get_or_404(id)
     return delete(user, user_index)



#START TERMS
@app.route('/terms/' )
@login_required
def term_index():
  terms = Terms.query.order_by(Terms.taxonomy).all()
  return render_template('/terms/index.html', terms=terms)

@app.route('/terms/add' , methods=['POST', 'GET'])
@login_required
def term_add():
     if request.method == 'POST':
        slug=slugify(request.form['slug'])
        term=Terms(request.form['name'],slug,request.form['description'], request.form['taxonomy']
                      ,request.form['parent'])
        return add(term, term_index, term_add)

     return render_template('/terms/add.html')

@app.route('/terms/update/<id>' , methods=['POST', 'GET'])
@login_required
def term_update (id):
    #Getting user by primary key:
    term = Terms.query.get_or_404(id)
    if request.method == 'POST':
            term.name = request.form['name']
            term.slug = slugify(request.form['slug'])
            term.description = request.form['description']
            term.taxonomy = request.form['taxonomy']
            term.parent = request.form['parent']
            return update(term, term_index, term_update, id)

    return render_template('terms/update.html', term=term)


@app.route('/terms/delete/<id>' , methods=['POST', 'GET'])
@login_required
def term_delete (id):
     term = Terms.query.get_or_404(id)
     return delete(term, term_index)


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
        if user == None:
           flash("invalid username/password")
           return render_template('login.html')
        if check_password_hash(user.password,password):
              login_user(user)
              return redirect(url_for('post_index'))
        else:
             flash("invalid username/password")
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
