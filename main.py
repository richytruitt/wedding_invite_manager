from flask import Flask, request, render_template, jsonify, redirect
import psycopg2
import pyqrcode
import configparser

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('config/dbconfig.ini')

@app.route('/')
def index():

    users_list = []
    try:
        conn = psycopg2.connect(dbname=str(config['dbcreds']['dbname']), user=str(config['dbcreds']['username']), host=str(config['dbcreds']['dbhost']), password=str(config['dbcreds']['password']))
        print("connected")
    except:
        print("Cannot connect to the DB")
    
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM invites where status = 'Attending';")
    except:
        print("Database query failed")
    
    _all = cursor.fetchall()
    for i in _all:
        each_item = dict(user_id = i[0], first_name = i[1], last_name = i[2], status = i[3])
        users_list.append(each_item)

    return render_template("attending.html", userlist=users_list)

@app.route("/<userID>")
def rsvp(userID):
    try:
        conn = psycopg2.connect(dbname=str(config['dbcreds']['dbname']), user=str(config['dbcreds']['username']), host=str(config['dbcreds']['dbhost']), password=str(config['dbcreds']['password']))
        print("connected")
    except:
        print("Cannot connect to the DB")
    
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM invites WHERE id ='"+userID+"';")
    except:
        print("Database query failed")
    

    user = cursor.fetchall()

    first_name = user[0][1]
    last_name = user[0][2]

    return render_template("wedding_form.html", id=userID, firstname=first_name, lastname=last_name)


@app.route("/generate_codes")
def codes():
    try:
        conn = psycopg2.connect(dbname=str(config['dbcreds']['dbname']), user=str(config['dbcreds']['username']), host=str(config['dbcreds']['dbhost']), password=str(config['dbcreds']['password']))
        print("connected")
    except:
        print("Cannot connect to the DB")

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM invites;")
    except:
        print("I did not get anything from the database")
    
    users = cursor.fetchall()
    for row in users:
        print(row[0])
        # code = pyqrcode.create("http://{}:5555/{}".format(config['dbcreds']['webhost'], row[0]))
        code = pyqrcode.create("http://{}:80/{}".format(config['dbcreds']['webhost'], row[0]))
        code.png('labels/{}.png'.format(row[1]+" "+row[2]), scale=5)

    return "test"


@app.route("/checkin", methods=['POST'])
def checkin():

    user_id = request.form['userid']
    status = request.form['status']
    entree = request.form['entree']

    try:
        conn = psycopg2.connect(dbname=str(config['dbcreds']['dbname']), user=str(config['dbcreds']['username']), host=str(config['dbcreds']['dbhost']), password=str(config['dbcreds']['password']))
        print("connected")
    except:
        print("Cannot connect to the DB")

    cursor = conn.cursor()

    try:
        cursor.execute("UPDATE invites SET status=%s, meal_option=%s WHERE id=%s;" , (status, entree, user_id))
        print("Update Successful")
        conn.commit()
    except:
        print("Database is unable to be updated")
    
    return redirect("localhost:80/", code=302)



if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port="5555")

