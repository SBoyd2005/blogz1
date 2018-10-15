from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:Password@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

app_secret_key = "build-a-blog"

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    body = db.Column(db.String(800))

    def __init__(self, title, body):
        self.title = title
        self.body = body

def get_blog_post(id):
    return Blog.query.get(id)

@app.route("/")
def index():
    return redirect('/blogs')

@app.route("/newpost", methods=['POST', 'GET'])
def newpost(): 
    if request.method == 'POST':
        new_post_title = request.form['title']
        new_post_body = request.form['body']
        new_post = Blog(new_post_title, new_post_body)

        if new_post_title == "" or new_post_body == "":
            flash("This field cannot be empty. Please fill in both fields.", 'error')
            return render_template('newpost.html', title="Build A Blog", new_post_body=new_post_body)
        else:
        
            db.session.add(new_post)
            db.session.commit()
            url = '/blogs?id=' + str(new_post.id)
            return redirect(url)

    return render_template('newpost.html', title="Build A Blog")

@app.route('/blogs', methods=['POST', 'GET'])
def blogs():
    ind_id =request.args.get('id')
    if ind_id:
        # post = Blog.query.get(ind_id)
        return render_template('individual.html', title='Build A Blog', post=get_blog_post(ind_id))
        
    else:
        all_posts = Blog.query.all()
        return render_template('blogs.html', title='Build A Blog', posts=all_posts)
        
    
if __name__ == '__main__':
    app.run()