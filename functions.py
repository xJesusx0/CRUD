import cs50 as cs

#Conexion con la base de datos
db = cs.SQL("sqlite:///users.db")

def Get_user_info(id):
    return db.execute("SELECT * FROM database WHERE id = ?", id)

def Get_data():
    return db.execute("SELECT * FROM database;")

def  Get_last_id():
    packed_last_id = db.execute("SELECT id FROM database ORDER BY id DESC LIMIT 1;")
    unpacked_last_id = packed_last_id[0]
    return unpacked_last_id["id"]

def Valid_username(username):
    if username == None:
        return False
    else:
        request = db.execute("SELECT name FROM database WHERE ? IN (SELECT name FROM database) LIMIT 1;",username)
        if len(request) == 0 and len(username.strip().lower()) != 0:
            return True
        else:
            return False
    
def Alert(username):
    if username == None:
        return False
    else:
        if len(username.strip()) == 0:
            return False
        else:
            request = db.execute("SELECT name FROM database WHERE ? IN (SELECT name FROM database) LIMIT 1;",username)
            if len(request) == 0:
                return True

def Valid_password(password):
    if password == None:
        return False
    if len(password.strip()) <= 8 and len(password.strip()) != 0:
        return True
    else:
        return False

def Register(username,password):  
    last_id = Get_last_id()
    new_id = last_id + 1
    db.execute("INSERT INTO database (id,name,password) VALUES (?,?,?);",new_id,username.lower(),password)

def Reorganize_id(id):
    data_to_reorganize = db.execute("SELECT * FROM database WHERE id > ?;",id)
    for data in data_to_reorganize:
        new_id = data["id"] - 1
        db.execute("UPDATE database SET id = ? WHERE id = ?;",new_id,data["id"])
    
def Delete(id):
    db.execute(f"DELETE FROM database WHERE id= ?;",id)
    Reorganize_id(id)

def Edit(id,new_username,new_password):
    db.execute("UPDATE database SET name = ?,password = ? WHERE id = ?;",new_username,new_password,id)