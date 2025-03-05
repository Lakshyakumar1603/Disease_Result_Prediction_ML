from flask import Flask,render_template,request,url_for
import joblib 
import numpy as np

model=joblib.load("Disease_Pridiction_Model_lgr.lb")


#Connect to mysql Data Base 
import mysql.connector as con

app=Flask(__name__)
@app.run("/")
def home():
    return render_template("form.html")

@app.route("/user_data",methods=["GET","POST"])
def user_data():
    if request.method=="POST":
        age=int(request.form["age"])
        g=int(request.form["g"])
        d=int(request.form["d"])
        f=int(request.form["f"])
        c=int(request.form["c"])
        fa=int(request.form["fa"])
        db=int(request.form["db"])
        bp=int(request.form["bp"])
        cl=int(request.form["cl"])
    data=[[age,d,f,c,fa,db,g,bp,cl]]
    
    output=model.predict(data)
    output=output.ravel()
    output=output[0]
    #return output
    if output==1:
        msg="Positive"
    else:
        msg="Negtive"
    

    #mysql connection work 
    conn=con.connect(
        host="localhost",
        user="root",
        password="",
        database="Disease"
    )
    
    main_data=(age,d,f,c,fa,db,g,bp,cl,int(output))
    
    #create the cursor object 
    cursor = conn.cursor()
    
    Qurey="insert into prediction(age,d,f,c,fa,db,g,bp,cl,p) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(Qurey,main_data)
    
    # Commit the transaction
    conn.commit()

    # Close the cursor and connection
    cursor.close()
    conn.close()
    return msg


if(__name__== "__main__"):
    app.run(debug=True,host='0.0.0.0',port=5000)