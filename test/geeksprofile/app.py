#LL: I'm using the code found here [https://www.geeksforgeeks.org/profile-application-using-python-flask-and-mysql/] as a foundation for my project
#http://localhost:5000/
# Store this code in 'app.py' file
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from MySQLdb import _mysql
import MySQLdb.cursors
import re

from mysql.connector import (connection)
import webbrowser


app = Flask(__name__)


app.secret_key = 'your secret key'


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = "DBHW2_2"
app.config['MYSQL_PASSWORD'] = "0Ct18Rs3n&q&"
app.config['MYSQL_DB'] = 'Books'

password= "0Ct18Rs3n&q&"
user= "DBHW2_2"


mysql = MySQL(app)


@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM readers WHERE username = % s AND password = % s', (username, password, ))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['username'] = account['username']
			msg = 'Logged in successfully !'
			return render_template('index.html', msg = msg)
		else:
			msg = 'Incorrect username / password !'
	return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        #print(request.form)
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        fBT= request.form["favoriteBookTitle"].strip()
        fBA= request.form["favoriteBookAuthor"].strip()
        fA= request.form["favoriteAuthor"].strip()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM readers WHERE username = % s', (username, ))
        #cursor.close()
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
# 		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
# 			msg = 'Invalid email address !'
# 		elif not re.match(r'[A-Za-z0-9]+', username):
# 			msg = 'name must contain only characters and numbers !'
          
            
        else:          
            if fA == "":
                fA= "None"
            if fBT =="":
                fBT= "None"
            if fBA =="":
                fBA= "None"
            if "password" =="":
                msg= "You need to enter a value for your password"
            #TODO
            
            cursor.execute("SELECT DISTINCT name FROM Authors")
            val= cursor.fetchall()
            authorList= []
            for i in val:
                authorList.append(list(i.values())[0])
            
            cursor.execute("SELECT DISTINCT authorName FROM books")
            fAuthorList= []
            val= cursor.fetchall()
            # print("val", val)
            # print()
            for i in val:
                fAuthorList.append(list(i.values())[0])
            
            cursor.execute("SELECT DISTINCT title FROM books")
            fBookList= list()
            val= cursor.fetchall()
            for i in val:
                fBookList.append(list(i.values())[0])
            
            #cursor.execute('SELECT authorName FROM Books WHERE title= %s', (fBT,))
            #cursor.execute('SELECT authorName FROM Books WHERE title= %s', [fBT])
            
            #('SELECT * FROM readers WHERE username = % s', (username, ))
            
            # print([username, password, fBT, fBA, fA])
            if (fA != "None") and (fA not in list(authorList)):
                msg= "The author you entered is not in our database."
                return render_template('register.html', msg = msg)
            
            if (fBA != "None") and (fBT != "None"):
                cursor.execute('SELECT authorName FROM Books WHERE title = % s', (fBT, ))
                rAN= list(cursor.fetchall())
                # print(rAN)
                
                if (fBA != "None") and (fBA not in fAuthorList):
                    msg= "The author you entered has not written a book in our database."
                    return render_template('register.html', msg = msg)
                
                if (fBT != "None") and (fBT not in fBookList):
                    msg= "The book you entered is not in our database"
                    return render_template('register.html', msg = msg)
                
                if len(rAN) > 0:
                    if fBA != rAN[0]:
                        msg= "The author of your favorite book and the title of your favorite book do not match."                    
                        return render_template('register.html', msg = msg)
            
            else:
                # print([username, password, fBT, fBA, fA])
                #cursor.execute("UPDATE readers SET password= %s, favoriteBookTitle= %s, favoriteBookAuthor= %s, favoriteAuthor= %s WHERE username= %s"), (password, fBT, fBA, fA, username)
                cursor.execute('INSERT INTO readers VALUES (% s, % s, %s, % s, % s)', (username, password, fBT, fBA, fA))
                mysql.connection.commit()
                msg = 'You have successfully registered!'
    
    elif request.method == 'POST':
        msg = 'Please fill out the form !'   
        
    #return render_template('register.html', msg = msg)
    return render_template('register.html', msg = msg)


@app.route("/index")
def index():
	if 'loggedin' in session:
		return render_template("index.html")
	return redirect(url_for('login'))


@app.route("/display")
def display():
	if 'loggedin' in session:
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM readers WHERE username = % s', (session['username'], ))
		account = cursor.fetchone()
		return render_template("display.html", account = account)
	return redirect(url_for('login'))

@app.route("/displayBooks", methods =['GET', 'POST'])
def displayBooks(): #Ll: taken from here [https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-select.html]
#LL: also from [https://www.quora.com/How-can-I-display-a-table-from-a-database-in-a-web-application-using-Flask]
    conn= MySQLdb.connect("localhost", user, password, "Books")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM Books")
    data = cursor.fetchall() #data from database 
    return render_template("displayBooks.html", value=data)

@app.route("/viewAuthors", methods =['GET', 'POST'])
def viewAuthors():
    conn= MySQLdb.connect("localhost", user, password, "Books")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM Authors")
    data = cursor.fetchall() #data from database 
    return render_template("viewAuthors.html", value=data)

@app.route("/viewPublishers", methods =['GET', 'POST'])
def viewPublishers():
    conn= MySQLdb.connect("localhost", user, password, "Books")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM Publishers")
    data = cursor.fetchall() #data from database 
    return render_template("viewPublishers.html", value=data)

@app.route("/viewPublishes", methods =['GET', 'POST'])
def viewPublishes():
    conn= MySQLdb.connect("localhost", user, password, "Books")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM Publishes")
    data = cursor.fetchall() #data from database 
    return render_template("viewPublishes.html", value=data)

@app.route("/deleteAccount", methods =['GET', 'POST'])
def deleteAccount():
    while "loggedin" in session:
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM readers WHERE username = % s', (session['username'], ))
        mysql.connection.commit()
        msg = 'You have successfully deleted your account!'
        
        session.pop('loggedin', None)
        session.pop('username', None)
        
        return render_template("deleteAccount.html")
     
    return redirect(url_for('login'))
    
@app.route("/searchBooks", methods =['GET', 'POST'])
def searchBooks():
    msg = ''
    if request.method == 'POST':
        #print("hi")
        bA = request.form['bA'].strip()
        bAD = request.form['bAD']
        
        bT= request.form["bT"].strip()
        bTD= request.form["bTD"]
        
        bL= request.form["bL"].strip()
        bLD= request.form["bLD"]
        
        print([bA, bAD, bL])
        if bA== "" or bAD== "":
            p1= ""
        if bT== "" or bTD=="":
            p2= ""
        if bL== "" or bLD=="":
            p4= ""
        # cursor.execute("UPDATE readers SET password='"+ password+ "', favoriteBookTitle='"+ fBT+ "',favoriteBookAuthor='"+fBA+ "',favoriteAuthor='"+ fA + "' WHERE username='"+username+"'")
        if bA !="" and bAD !="":
            p1= "authorName"+ bAD+ "'"+bA+ "'"+","
        if bT != "" and bTD != "":
            p2= "title"+ bTD+ "'"+bT+"'"+","
        if bL != "" and bLD != "":
            p4= "link"+ bLD+ "'"+ bL+ "'"
            
        if p1 == "" and p2 == "" and p4 == "":
            msg= "You did not correctly enter enough information for a search"
            return render_template('searchBooks.html', msg = msg)
        
        s= ("SELECT * FROM books WHERE "+p1 + p2 +p4).strip(",")
        
        conn= MySQLdb.connect("localhost", user, password, "Books")
        cursor = conn.cursor()
        #cursor.execute('SELECT * FROM books WHERE username =  s', (session['username'], ))
        #cursor.execute("SELECT * FROM books WHERE authorName %s %s, title %s %s, averageRating %s %s, link %s %s"), (bAD, bA, bTD, bT, bRD, bR, bLD, bL)
        cursor.execute(s)
        data = cursor.fetchall() #data from database 
        return render_template("searchBooks.html", value=data)
        #s= ("UPDATE Students2.records SET ssn='"+ ssnVal+ "', firstName='"+ fNameVal+ "',lastName='"+lNameVal+ "',address='"+ addrVal + "',state='"+ stateVal+ "', zipcode= '"+ zipcodeVal+ "' WHERE id='"+keyVal+"'")  
    return render_template('searchBooks.html', msg = msg)

@app.route("/searchAuthors", methods =['GET', 'POST'])
def searchAuthors():
    msg = ''
    if request.method == 'POST':
        aN = request.form['aN'].strip()
        aND = request.form['aND']
        
        aB= request.form["aB"].strip()
        aBD= request.form["aBD"]
        
        aD= request.form["aD"].strip()
        aDD= request.form["aDD"]
        
        #print([bA, bAD, bL])
        if aN== "" or aND== "":
            p1= ""
        if aB== "" or aBD=="":
            p2= ""
        if aD== "" or aDD=="":
            p3= ""
        
        if aN !="" and aND !="":
            p1= "name"+ aND+ "'"+aN+ "'"+","
        if aB != "" and aBD != "":
            p2= "yearOfBirth"+ aBD+ "'"+aB+"'"+","
        if aD != "" and aDD != "":
            p3= "yearOfDeath"+ aDD+ "'" + aD+ "'" +","
        
        if p1 == "" and p2 == "" and p3 == "":
            msg= "You did not correctly enter enough information for a search"
            return render_template('searchAuthors.html', msg = msg)
        
        s= ("SELECT * FROM authors WHERE "+p1+ p2+ p3).strip(",")
        print(s)
        
        conn= MySQLdb.connect("localhost", user, password, "Books")
        cursor = conn.cursor()
        cursor.execute(s)
        data = cursor.fetchall() #data from database 
        return render_template("searchAuthors.html", value=data)
    return render_template('searchAuthors.html', msg = msg)

@app.route("/searchPublishers", methods =['GET', 'POST'])
def searchPublishers():
    msg = ''
    if request.method == 'POST':
        #print(request.method)
        #print("hi")
        pN = request.form['pN'].strip()
        pND = request.form['pND']
        
        pO= request.form["pO"].strip()
        pOD= "="
        
        #print([bA, bAD, bL])
        if pN== "" or pND== "":
            p1= ""
        if pO== "" or pOD=="":
            p2= ""

        
        # cursor.execute("UPDATE readers SET password='"+ password+ "', favoriteBookTitle='"+ fBT+ "',favoriteBookAuthor='"+fBA+ "',favoriteAuthor='"+ fA + "' WHERE username='"+username+"'")
        if pN !="" and pND !="":
            p1= "name"+ pND+ "'"+pN+ "'"+","
        if pO != "" and pOD != "":
            p2= "stillAround = "+ "'"+pO+"'"
            
        if p1 == "" and p2 == "":
            msg= "You did not correctly enter enough information for a search"
            return render_template('searchPublishers.html', msg = msg)

        
        s= ("SELECT * FROM publishers WHERE "+p1+ p2).strip(",")
        print(s)
        
        conn= MySQLdb.connect("localhost", user, password, "Books")
        cursor = conn.cursor()
        cursor.execute(s)
        data = cursor.fetchall() #data from database 
        return render_template("searchPublishers.html", value=data)
    return render_template('searchPublishers.html', msg = msg)

@app.route("/searchPublishes", methods =['GET', 'POST'])
def searchPublishes():
    msg = ''
    if request.method == 'POST':
        print(request.form)
        #print("hi")
        aN = request.form['aN'].strip()
        aND = request.form['aND']
        
        bT= request.form["bT"].strip()
        bTD= request.form["bTD"]
        
        pN= request.form["pN"].strip()
        pND= request.form["pND"]
        
        y= request.form["y"].strip()
        yD= request.form["yD"]
        
        l= request.form["l"].strip()
        lD= request.form["lD"]
        

        if aN== "" or aND== "":
            p1= ""
        if bT== "" or bTD=="":
            p2= ""
        if pN== "" or pND=="":
            p3= ""
        if y== "" or yD=="":
            p4= ""
        if l== "" or lD== "":
            p5= ""
            
            
        if aN !="" and aND !="":
            p1= "authorName"+ aND+ "'"+aN+ "'"+","
        if bT != "" and bTD != "":
            p2= "title"+ bTD+ "'"+bT+"'"+","
        if pN != "" and pND != "":
            p3= "publisherName"+ pND+ "'" + pN+ "'" +","
        if y != "" and yD != "":
            p4= "yearOfPublication"+ yD+ "'"+ y+ "'" + ","
        if l != "" and lD != "":
            p5= "location"+ lD+ "'"+ l+ "'"
            
        if p1 == "" and p2 == "" and p3 == "" and p4 == "" and p5 == "":
            msg= "You did not correctly enter enough information for a search"
            return render_template('searchPublishes.html', msg = msg)
            
            
        s= ("SELECT * FROM publishes WHERE "+p1 + p2 + p3 + p4 + p5).strip(",")
        print(s)
        
        conn= MySQLdb.connect("localhost", user, password, "Books")
        cursor = conn.cursor()
        cursor.execute(s)
        data = cursor.fetchall() #data from database 
        return render_template("searchPublishes.html", value=data)
        #s= ("UPDATE Students2.records SET ssn='"+ ssnVal+ "', firstName='"+ fNameVal+ "',lastName='"+lNameVal+ "',address='"+ addrVal + "',state='"+ stateVal+ "', zipcode= '"+ zipcodeVal+ "' WHERE id='"+keyVal+"'")  
    return render_template('searchPublishes.html', msg = msg)

@app.route("/viewRatings", methods =['GET', 'POST'])
def viewRatings():
    conn= MySQLdb.connect("localhost", user, password, "Books")
    cursor = conn.cursor()
    
    cursor.execute("SELECT authorName, title, AVG(rating) FROM rate GROUP BY authorName, title")
    data = cursor.fetchall() #data from database 
    return render_template("viewRatings.html", value=data)


@app.route("/rateBooks", methods =['GET', 'POST'])
def rateBooks():
    msg = ''
    print(request.form)
    if request.method == 'POST' and 'authorName' in request.form and "title" in request.form and "rating" in request.form:
        username = session['username']
        aN= request.form["authorName"].strip()
        t= request.form["title"].strip()
        r= request.form["rating"].strip()
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute("SELECT DISTINCT name FROM Authors")
        val= cursor.fetchall()
        authorList= []
        for i in val:
            authorList.append(list(i.values())[0])
            
        cursor.execute("SELECT DISTINCT title FROM books")
        fBookList= list()
        val= cursor.fetchall()
        for i in val:
            fBookList.append(list(i.values())[0])
            
        if (t == "") and (t not in list(fBookList)):
            msg= "The book you entered is not in our database."
            return render_template('rateBooks.html', msg = msg)
        
        if (aN == "") and (aN not in list(fBookList)):
            msg= "The author you entered is not in our database."
            return render_template('rateBooks.html', msg = msg)
        
        cursor.execute('SELECT authorName FROM Books WHERE title = % s', (t, ))
        rAN= list(cursor.fetchall())
        
        if aN != rAN:
            msg= "The author you entered did not write the book you entered."
            return render_template('rateBooks.html', msg = msg)
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # cursor.execute("INSERT INTO readers(username, password) VALUES (%s, %s)", (username, password))
        cursor.execute('INSERT INTO rate VALUES (%s, %s, %s, %s)', (username, aN, t, r))
        mysql.connection.commit()
        msg = 'You have successfully submited your rating!'
    
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    
    return render_template('rateBooks.html', msg = msg)
         
@app.route("/update", methods =['GET', 'POST'])
def update():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # print("request form favebooktitle")
        # print(request.form["favoriteBookTitle"])
        # print("empty string??")
        # print(request.form["favoriteBookTitle"]== "")
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        fBT= request.form["favoriteBookTitle"].strip()
        fBA= request.form["favoriteBookAuthor"].strip()
        fA= request.form["favoriteAuthor"].strip()
        
# 		email = request.form['email']
# 		organisation = request.form['organisation']
# 		address = request.form['address']
# 		city = request.form['city']
# 		state = request.form['state']
# 		country = request.form['country']
# 		postalcode = request.form['postalcode']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM readers WHERE username = % s', (username, ))
        account = cursor.fetchone()
        # if account:
        #     msg = 'Account already exists !'
# 		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
# 			msg = 'Invalid email address !'
# 		elif not re.match(r'[A-Za-z0-9]+', username):
# 			msg = 'name must contain only characters and numbers !'
#        else:
            #s= "INSERT INTO readers VALUES (%s, %s)", (username, password)
        if fA == "":
            fA= "None"
        if fBT =="":
            fBT= "None"
        if fBA =="":
            fBA= "None"
        if "password" =="":
            msg= "You need to enter a value for your password"
            return render_template('update.html', msg = msg)
         #       s= ("UPDATE Students2.records SET ssn='"+ ssnVal+ "', firstName='"+ fNameVal+ "',lastName='"+lNameVal+ "',address='"+ addrVal + "',state='"+ stateVal+ "', zipcode= '"+ zipcodeVal+ "' WHERE id='"+keyVal+"'")
         #cursor.execute('UPDATE accounts SET  username =% s, password =% s, email =% s, organisation =% s, address =% s, city =% s, state =% s, country =% s, postalcode =% s WHERE id =% s', (username, password, email, organisation, address, city, state, country, postalcode, (session['id'], ), ))
        print([username, password, fBT, fBA, fA])
        #cursor.execute("UPDATE readers SET password= %s, favoriteBookTitle= %s, favoriteBookAuthor= %s, favoriteAuthor= %s WHERE username= %s"), (password, fBT, fBA, fA, username)
        cursor.execute("UPDATE readers SET password='"+ password+ "', favoriteBookTitle='"+ fBT+ "',favoriteBookAuthor='"+fBA+ "',favoriteAuthor='"+ fA + "' WHERE username='"+username+"'")
        mysql.connection.commit()
        msg = 'You have successfully updated your profile!'
        
# =============================================================================
#         if "favoriteAuthor" != "" and ("favoriteBookTitle" == "" and "favoriteBookAuthor" == ""):
#             #cursor.execute('INSERT INTO readers(username, password, favoriteAuthor) VALUES (% s, % s, % s)', (username, password, fA))
#             print("1")
#             cursor.execute("UPDATE readers SET password= %s, favoriteAuthor= %s WHERE username= %s"), (password, fA, username)
#             mysql.connection.commit()
#             msg = 'You have successfully registered !'
#         
#         elif "favoriteAuthor" == "" and ("favoriteBookTitle" != "" and "favoriteBookAuthor" != ""):
#             #cursor.execute('INSERT INTO readers(username, password, favoriteBookTitle, favoriteBookAuthor) VALUES (% s, % s, %s, % s)', (username, password, fBT, fBA))
#             print("2")
#             cursor.execute("UPDATE readers SET password= %s, favoriteBookTitle= %s, favoriteBookAuthor= %s WHERE username= %s"), (password, fBT, fBA, username)
#             mysql.connection.commit()
#             msg = 'You have successfully registered !'
#         
#         elif ("favoriteBookTitle" != "" and "favoriteBookAuthor" == ""):
#             msg= "You have not fully entered your favorite book"
#         
#         elif ("favoriteBookTitle" == "" and "favoriteBookAuthor" != ""):
#             msg= "You have not fully entered your favorite book"
#         
#         elif "favoriteAuthor" == "" and ("favoriteBookTitle" == "" and "favoriteBookAuthor" == ""):
#             print("3")
#             #cursor.execute("INSERT INTO readers(username, password) VALUES (%s, %s)", (username, password))
#             cursor.execute("UPDATE readers SET password= %s WHERE username= %s"), (password, username)
#             mysql.connection.commit()
#             msg = 'You have successfully registered !'
#         
#         
#         else:
#             #        s= ("UPDATE Students2.records SET ssn='"+ ssnVal+ "', firstName='"+ fNameVal+ "',lastName='"+lNameVal+ "',address='"+ addrVal + "',state='"+ stateVal+ "', zipcode= '"+ zipcodeVal+ "' WHERE id='"+keyVal+"'")
#             #cursor.execute('INSERT INTO readers VALUES (% s, % s, %s, % s, % s)', (username, password, fBT, fBA, fA))
#             print("4")
#             cursor.execute("UPDATE readers SET password= '"+password+"',favoriteBookTitle= '"+ fBT+ "',favoriteBookAuthor= '"+ fBA+ "',favoriteAuthor= '"+ fA+ "' WHERE username= '"+ username+"'")
#             mysql.connection.commit()
#             msg = 'You have successfully registered !'
# =============================================================================
            
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('update.html', msg = msg)

if __name__ == "__main__":
	app.run(host ="localhost", port = int("5000"))
