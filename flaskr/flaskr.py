# all the imports

from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from flask.ext.sqlalchemy import SQLAlchemy
import datetime

#Configuration
DEBUG = True

# create our little application :)
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Tracker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(80))
    report_user = db.Column(db.String(120))
    timestamp = db.Column(db.DateTime)

    def __init__(self, location, report_user):
        self.location = location
        self.report_user = report_user
        self.timestamp = datetime.datetime.now()

    def __repr__(self):
        return '<User %r>' % self.report_user

@app.route('/')
def homepage():
    #trackings = Tracker.query.all()
    trackings = Tracker.query.order_by(Tracker.timestamp.desc()).limit(5)
    return render_template('homepage.html', trackings=trackings)
        
@app.route('/tracking', methods=['POST'])
def createtrack():
    location = request.form['location']
    user = request.form['user']
    print location
    print user
    
    if location == "writein":
        location = request.form['writein']
        
    new_tracking = Tracker(location, user)
    db.session.add(new_tracking)
    db.session.commit()
    return redirect(url_for('homepage'))

#@app.route('/tracking', methods=['DELETE'])
#def deletetrack():
    
    
    
if __name__ == '__main__':
    app.run(host='0.0.0.0')
