from flask import Flask, jsonify, abort, request, redirect, render_template, session, g, url_for
import fileinput
import json 
from votedao import voteDAO
 # to get server up and running
app = Flask(__name__, static_url_path='', static_folder ='static')



clubs = [
    {'clubName':'Shannon Gaels'},
    {'clubName':'Maghera'},
    {'clubName':'Cavan Gaels'},
    {'clubName':'Courlough'},
    {'clubName':'St.Kilda'}
    ]


#########################################################################################
# Get logged in 


class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'

users = []
users.append(User(id=1, username='Conor', password='Blacklion1.'))
users.append(User(id=2, username='admin', password='admin'))
users.append(User(id=3, username='Andrew', password='Castlebar'))



#########################################
#Flask & login requirements

app = Flask(__name__, static_url_path='', static_folder='static')
app.secret_key = 'GMIT'

#Check for User
@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user

#Login page to verify credentials and start session
@app.route('/login', methods=['GET', 'POST'])
def login():
    while True:
        try:
            if request.method == 'POST':
                session.pop('user_id', None)

                username = request.form['username']
                password = request.form['password']
                
                user = [x for x in users if x.username == username][0]
                if user and user.password == password:
                    session['user_id'] = user.id
                    return redirect(url_for('profile'))

                return redirect(url_for('login'))
        except:
                return '<h1>Unknown User</h1> '+\
        '<button>'+\
            '<a href="'+url_for('login')+'">' +\
                'Try Again' +\
            '</a>' +\
        '</button>'
        
        return render_template('login.html')

        

#Session Logout page
@app.route('/logout')
def logout():
    session.clear()
    return redirect('login.html')

#Redirect if not looged in
@app.route('/notlogged')
def notlogged():

    return redirect('login.html')

#Logged in User Home page
@app.route('/profile')
def profile():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('profile.html')

#Redirect to Landing Page
@app.route('/')
def index():
    return redirect('login.html')



###################################################################
# Viewing Tables
@app.route('/clubs', methods=['GET'])
def getallClubs():
    data = voteDAO.getallClubs()
    return jsonify(data)


@app.route('/sportsground', methods=['GET'])
def getallGrounds():
    data = voteDAO.getallGrounds()
    return jsonify(data)

@app.route('/clubs/<int:ID>')
def locateClub(ID):
    return jsonify(voteDAO.locateClub(ID))

@app.route('/sportsground/<int:ID>')
def locateGround(ID):
    return jsonify(voteDAO.locateGround(ID))

#########################################################################################
#delete and add to dbs (while viewing also)

@app.route('/clubs/<int:ID>', methods=['DELETE'])
def deleteclub(ID):
    voteDAO.deleteclub(ID)
    return jsonify({'done':True})

@app.route('/sportsground/<int:ID>', methods=['DELETE'])
def deletesportsground(ID):
    voteDAO.deletesportsground(ID)
    return jsonify({'done':True})


# Voting functionality
@app.route('/clubs/vote/<clubName>', methods=['POST'])
def voteForClub(clubName):
    sender = 'Online'
    data = (clubName,sender)
    newid =voteDAO.createVote(data)

    return jsonify({'id':newid})

# Get count of votes
@app.route('/clubs/vote/<clubName>', methods=['GET'])
def getCountForBand(clubName):
    count = voteDAO.countvotes(clubName)
    return jsonify({clubName:count})

# delete all votes
@app.route('/clubs/vote/all', methods=['DELETE'])
def deleteAllVote():
    return jsonify({'done':True})

# Get count of all votes
@app.route('/clubs/vote', methods=['GET'])
def getAllCount():
    allcounts = []
    for club in clubs:
        clubName = club['clubName'] 
        count = voteDAO.countvotes(clubName)
        allcounts.append({clubName:count})
    return jsonify(allcounts)
#########################################################################################


if (__name__) == "__main__":
    app.run(debug=True)
