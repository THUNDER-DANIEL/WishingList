def dashboard():
    if "user_id" not in session:
        flash("you need to be logged in to view this page!")
        return redirect("/")
    else:
        db = connectToMySQL("dash")
        query = "SELECT quotes.id, quotes.person, quotes.words, quotes.created_at, quotes.updated_at, quotes.users_id, users.first_name, users.last_name FROM quotes JOIN users ON quotes.users_id = users.id;"
        results = db.query_db(query)
        db = connectToMySQL("dash")
        query = "SELECT * FROM users WHERE id = %(id)s;"
        data = {
            "id": session["user_id"],
        }
        users = db.query_db(query, data)
        return render_template("dashboard_1.html", gibberish = results, info = users)

#  {% for one in gibberish %}
#         <p>{{one['person']}}: "{{one['words']}}"</p>
#         <br>
#         <p>Posted by <a href="/view/quotes/{{one['users_id']}}">{{one['first_name']}} {{one['last_name']}}</a></p>
#         <br>
#         {% endfor %}

@app.route("/view/quotes/<id>")
def view(id):
    db = connectToMySQL("dash")
    query = "SELECT quotes.person, quotes.words, quotes.users_id, users.first_name, users.last_name FROM quotes JOIN users ON quotes.users_id = users.id WHERE users.id = %(id)s;"
    data = {
        "id": id,
    }
    result = db.query_db(query, data)
    db = connectToMySQL("dash")
    query = "SELECT users.first_name, users.last_name FROM users WHERE id = %(id)s;"
    data = {
        "id": id,
    }
    users = db.query_db(query, data)
    return render_template("view_1.html", quotes = result, information = users)

{% for x in information %}
        <h1> {{x['first_name']}} {{x['last_name']}}'s Quotes</h1>
        {% endfor %}



            SELECT quote_table.author, quote_table.quote_content, quote_table.id_trax, user_table.first_name, user_table.last_name FROM quote_table JOIN user_table ON quote_table.id_trax = user_table.id_track WHERE user_table.id_track = 1 ;


SELECT wishtbl.wishing, wishtbl.idnum, usertbl.name, usertbl.username 
FROM wishtbl JOIN usertbl
ON wishtbl.idnum = wish_user_id WHERE usertbl.id = 3 ;



SELECT wishtbl.wishing, wishtbl.wish_user_id FROM wishtbl JOIN usertbl ON usertbl.id, usertbl.name WHERE usertbl.id == wishtbl.wish_user_id = 1;





SELECT wishtbl.wishing, wishtbl.wish_user_id, usertbl.id, usertbl.name FROM wishtbl JOIN usertbl ON usertbl.id = wishtbl.wish_user_id WHERE usertbl.id =2; 



######### HTML SHOW PAGE WITH DB INFORMATION #################
@app.route("/wish_items/create", methods=["GET"] )
def so1o():
    if  not "userid" in session:
        return redirect("/logout")
    return render_template('show.html')
########## END OF SHOW PAGE #######################