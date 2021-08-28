from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from werkzeug.utils import redirect

app = Flask(__name__) #this just references this file
#tells us where the DB is located
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
#above initalises the db with our app

class ToDo(db.Model):
    #setting up columns, first is int id
    id = db.Column(db.Integer, primary_key=True)
    #cloumn called content, what holds each task. 200 chars max. must have content
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = ToDo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    
    else:
        tasks = ToDo.query.order_by(ToDo.date_created).all()
        return render_template('index.html', tasks=tasks)
    # name = request.args.get("name", "World")
    # return f'Hello, {escape(name)}!'

# @app.route('/api/wings', methods = [ 'POST', 'GET' ])
# def wings():
#     if request.method == 'POST':
#         return 'lkdfl'
#     return 'sdfsd'

if __name__ == "__main__":
    app.run(debug=True)