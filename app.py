from datetime import datetime, date
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'

# creating a database object here

db = SQLAlchemy(app)

class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    detail = db.Column(db.String(180), nullable=True)
    due = db.Column(db.DateTime, nullable=False)
    priority = db.Column(db.Integer, nullable=False)

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'GET':
        posts = Post.query.order_by(Post.due).all()
        return render_template('index.html', posts=posts, today=date.today())
    else:
        t = request.form.get('title')
        detail = request.form.get('detail')
        due = request.form.get('due')
        priority = request.form.get('priority')

        d = datetime.strptime(due, '%Y-%m-%d')
        print(t)
        print(detail)
        
        detail_str = detail.split('\r\n')
       

        print(detail_str)
        new_post = Post(title=t, detail=detail, due=d, priority=priority)
        db.session.add(new_post)
        db.session.commit()

        return redirect('/')


@app.route('/create')
def create():
    return render_template('create.html')


@app.route('/detail/<int:id>')
def read(id):

    post = Post.query.get(id)
    return render_template('detail.html', post=post)



@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):

    post = Post.query.get(id)

    if request.method == 'GET':
        return render_template('update.html', post=post)
    else:
        post.title = request.form.get('title')
        post.detail = request.form.get('detail')
        post.due = datetime.strptime(request.form.get('due'), '%Y-%m-%d')
        post.priority = request.form.get('priority')

        db.session.commit()
        return redirect('/')


# deleting the event
@app.route('/delete/<int:id>')
def delete(id):

    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()

    return redirect('/')

if __name__ == "__main__":
    app.run()
    