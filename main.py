import cs50 as cs
import flask
import functions as f
#Conexion con la base de datos
db = cs.SQL("sqlite:///users.db")

#iniciamos la app
app = flask.Flask(__name__)

@app.route("/")
def index():
    users = f.Get_data() 
    indexes = f.Get_index()
    return flask.render_template("index.html", data = zip(users,indexes))

@app.route("/Table")
def Table():
    users = f.Get_data() 
    indexes = f.Get_index()
    return flask.render_template("table.html", data = zip(users,indexes))


@app.route("/Register", methods = ["GET","POST"])
def register():
    id       = 1
    username = flask.request.form.get("username")
    password = flask.request.form.get("password") 
    
    if f.Valid_id(id) and f.Valid_username(username) and f.Valid_password(password):
        f.Register(id,username,password)
        return flask.redirect("/")
    
    return flask.render_template("register.html")

@app.route("/Delete", methods = ["GET","POST"])
def delete():
    id = flask.request.form.get("id")
    f.Delete(id)
    return flask.redirect("/")    

@app.route("/Edit", methods = ["GET","POST"])
def edit():

    id = flask.request.form.get("id")
    new_username = flask.request.form.get("new_username")
    new_password = flask.request.form.get("new_password")

    user_data = f.Get_user_info(id)[0]
    if user_data["name"] == new_username:
        if f.Valid_password(new_password):
            f.Edit(id,new_username,new_password)
            return flask.redirect("/")
        else:
            return flask.render_template("edit.html", data = user_data)
    
    else:
        if f.Valid_username(new_username) and f.Valid_password(new_password):         
            f.Edit(id,new_username,new_password)
            return flask.redirect("/")
        else:
            return flask.render_template("edit.html", data = user_data)
 
app.run(debug = True, port= 8080)