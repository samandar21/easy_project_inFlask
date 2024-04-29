import os
import hashlib
from slugify import slugify
from flask import (
    Flask, 
    render_template,
    request,
    make_response,
    session,
    redirect,
)
from articles import Article

app = Flask(__name__)
app.secret_key="thisisverysecret"

articles = Article.all()

users={
    "admin":"4f0239556a42e7efd4f8a34125608ae4daaeb3de247a61a8fc6589e344d5befa",
}


@app.route("/")
def blog():
    return render_template("blog.html", articles=articles)



@app.get("/admin")
def admin_page():
    if "user" in session:
        return "you are alredy authenticated"
    return render_template("login.html")

@app.get("/logout")
def logout():
    del session["user"]
    return "logged out"

@app.post("/admin")
def admin_login():
    username=request.form["username"]
    password=request.form['password']
    
    if username not in users:
        return render_template("login.html",error="username/password incorrect")
    
    hashed=hashlib.sha256(password.encode()).hexdigest()
    
    if users[username]!=hashed:
        return render_template("login.html",error="username/password incorrect")
    
    session["user"]=username
    return "you are now authenticated"



@app.route("/first-time")
def first_time():
    if "seen" not in request.cookies:
        response=make_response("you are new here") 
        response.set_cookie("seen","1")
        return response
    
    seen=int(request.cookies["seen"])
    response=make_response(f"I have seen you before {seen} times") 
    response.set_cookie("seen",str(seen+1))
    return response

@app.route('/publish')
def publish():
    if 'user' not in session:
        return redirect("/admin")
    
    return render_template('publish.html')

@app.post("/publish")
def new_articles():
    title=request.form["title"]
    content=request.form["content"]
    Article.create_article(title,content)
    return "Maqola yaratildi"
    


@app.route("/set-session")
def set_session():
    session["user_id"]=1
    return "session set"




@app.route("/get-session")
def get_session():
    return f"user_id= {session['user_id']}"
    



@app.route("/blog/<slug>")
def article(slug: str):
    article = articles[slug]
    return render_template("article.html", article=article)




if __name__ == "__main__":
    app.run(port=4200, debug=True)
    

