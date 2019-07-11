from flask import Flask, render_template, redirect, request, session, flash
from connect5000 import connectToMySQL
import re
from flask_bcrypt import Bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "ft67uhgf"

########## SHOWS MAIN PAGE #########################
@app.route("/")
def index():
    mysql = connectToMySQL('wishdb')
    # friends = mysql.query_db('SELECT * FROM usertbl;')
    return render_template("main.html")
################## END OF SHOW PAGE ################################

############## ADD USER _ INPUT VALIDATION ######################
@app.route("/add", methods=["POST", "GET"])
def input():
    is_valid = True
    if len(request.form['reg_name']) < 3:
        flash("Name should be at least 3 characters")
    if len(request.form['reg_username']) < 3:
        flash("User Name should be at least 3 characters")
    if len(request.form['reg_date']) < 2:
        flash("Please enter a valid hired date")
    if len(request.form['reg_pass']) < 8:
        flash("Password should be at least 8 characters")
    if request.form['reg_pass'] != request.form['con_pass']:
        flash("Password do not match- Please try again")

    # if not EMAIL_REGEX.match(request.form['reg_email']):    
    #     flash("Invalid email address!")
    #-------CONNECTS AND CHECKS FOR EMAIL VALIDATION  ---------
    database = connectToMySQL('wishdb')
    query = "SELECT * FROM usertbl WHERE username= %(usn)s;"
    data = {
            'usn' : request.form['reg_username'],
        }
    result = database.query_db(query, data)
    if len(result)>0:  #IF A USER THAT ALREADY EXIST THEN FLASH MSG **** DO NOT ENTER ******
        flash("Username already in use - Please try again!")
    if not '_flashes' in session.keys(): #IF THERE ARE NO FLASH MSG THEN PROCESS TO PUT INFO INTO DB
        flash("Successfully Added",)
        database = connectToMySQL('wishdb')
        pw_hash = bcrypt.generate_password_hash(request.form['reg_pass'])
        print(pw_hash)
        query = "INSERT INTO usertbl(name, username, date_hired, password)VALUES(%(n)s,%(un)s,%(day)s,%(pass)s);"
        qwerty = {
                'n' : request.form['reg_name'],
                'un' : request.form['reg_username'],
                'day' : request.form['reg_date'],
                'pass': pw_hash,
        }
        info=database.query_db(query,qwerty)
        queryDB = "SELECT * FROM usertbl WHERE username = %(un)s;" #ROADMAP INTO THE EMAIL IN THE DB

        dataDB = {
            "un" : request.form['reg_username'],
        }
        db = connectToMySQL('wishdb') # linking db 
        show = db.query_db(queryDB,dataDB)
        session['userid'] = show[0]['id']
        session['fn'] = show[0]['name']


        return redirect("/dashboard")
    else:
        return redirect("/")
################# END OF ADD USER W/ VALIDATION #########################

####################### MESSAGE ###############################

## EVEYRONE BUT CURRENT USER ---------------------
@app.route("/dashboard")
def msg():
    mysql = connectToMySQL("wishdb")
    qwerty = "SELECT id, name, username, created_at FROM usertbl WHERE id != %(id)s;"
    data={
        "id" : session['userid']
    }
    result = mysql.query_db(qwerty,data)
    ##----   -  - - - ALL BUT CURRENT USER WISH LIST  - -- - - - 
    mysql = connectToMySQL("wishdb")
    qwerty3 ="SELECT wishtbl.idnum, wishtbl.wishing, wishtbl.wcreated_at, wishtbl.wish_user_id, usertbl.id, usertbl.name FROM wishtbl JOIN usertbl ON usertbl.id = wishtbl.wish_user_id WHERE usertbl.id != %(id)s; "
    data3={
        "id" : session['userid'],
    }
    result2 = mysql.query_db(qwerty3,data3)
###_-------------- CURRENT USER WISH LIST --------------------
    mysql = connectToMySQL("wishdb")
    qwertys ="SELECT wishtbl.idnum, wishtbl.wishing, wishtbl.wcreated_at, wishtbl.wish_user_id, usertbl.id, usertbl.name FROM wishtbl JOIN usertbl ON usertbl.id = wishtbl.wish_user_id WHERE usertbl.id = %(id)s; "
    data1={
        "id" : session['userid'],
    }
    main = mysql.query_db(qwertys,data1)

##----GET SESSION USER FIRST NAME TO BE DISPLAYED -------------
    mysql = connectToMySQL("wishdb")
    qwerty2 ="SELECT name FROM usertbl WHERE id = %(fn)s;"
    data2={
        "fn": session['userid']
    }
    resultz = mysql.query_db(qwerty2,data2)
    #-------------------------
    # mysql = connectToMySQL("wishdb")
    # query='SELECT COUNT(wishings.recipient_id) FROM wishings WHERE wishings.recipient_id=users_users_id;'

    return render_template("read.html", show=resultz, showing=result, appearing= result2, hero=main)
#################### END OF MESSAGE ###########################



############## REMOVE FROM DB ###################################
@app.route("/delete/<id>")
def help_me_code_gods(id):
    mysql = connectToMySQL("wishdb")
    qwerty = "DELETE FROM wishtbl WHERE idnum = %(num)s; "
    data = {
        "num" : id,
    }
    dust = mysql.query_db(qwerty,data)
    print("************77")
    print(dust)
    print("************77")
    return redirect("/dashboard")
############### END OF PROCESS #######################

####### SHOW SINGLE WISH LIST ITEM ##############################
@app.route("/wish_items/<id>")
def view(id):
    mysql = connectToMySQL("wishdb")
    qwerty="SELECT * FROM wishtbl WHERE idnum = %(num)s;"
    data = {
    "num" : id,
    }
    product = mysql.query_db(qwerty,data)
    return render_template("show.html", item=product)
#### END OF DELETE #########################




######## ADD ITEM TO WISH LIST ###############
@app.route("/wish_items/create")
def wlitem():
    return render_template("create.html")
########## END OF ADD ITEMT TO WISH LIST #########


######### CREATE A NEW WISH LIST ITEM #################
@app.route("/wishlist", methods=["POST"] )
def createwish():
    is_valid = True
    if len(request.form['wish_item']) < 3:
        flash("Wish Item should be at least 3 characters")
    if not '_flashes' in session.keys(): 
        database = connectToMySQL("wishdb")
        qwerty = "INSERT INTO wishtbl(wishing,wish_user_id) VALUES (%(wh)s,%(use)s); "
        data = {
            "wh" : request.form["wish_item"],
            "use" : session['userid']
            }
        display = database.query_db(qwerty,data)

        return redirect("/dashboard")
    else:
        return redirect('/wish_items/create')
########## END OF  CREATE A NEW WISH LIST ITEM #######################



#########  LOG IN ###############################
@app.route('/WelcomeBack', methods=['POST'])
def login():   # see if the username provided exists in the database
    mysql = connectToMySQL("wishdb")
    query = "SELECT * FROM usertbl WHERE username= %(un)s;"
    data = {
        "un" : request.form["log_username"],
        }
    result = mysql.query_db(query, data)

    if len(result) > 0:
        if not request.form["log_pass"] =="":
            pw_hash = bcrypt.generate_password_hash(request.form['log_pass'])
            print (pw_hash)
            if bcrypt.check_password_hash(result[0]['password'], request.form['log_pass']):
                # if we get True after checking the password, we may put the user id in session
                session['userid'] = result[0]['id']
                # never render on a post, always redirect!
                return redirect('/dashboard')
    flash("You could not be logged in - Try Again!")
    return redirect("/")
################# END OF LOG-IN  ##########################




# LOGOUT USER /// CLEAR SESSION #############################
@app.route('/logout',methods=['GET'])
def logout(): 
    session.clear()
    flash("You have been logged out - Please return soon!")
    return redirect('/')
###################### END OF LOG OUT #####################

if __name__ == "__main__":
    app.run(debug=True)





