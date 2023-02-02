import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="",
  password="",
  database="eventos"
)


def insert_user(data):
    mycursor = mydb.cursor()
    sql = "INSERT INTO usuarios (user, name, password_hash) VALUES (%s, %s, %s)"
    mycursor.execute(sql, data)
    mydb.commit()
    return mycursor.rowcount

def select_user(user):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM usuarios WHERE user = %(user)s", {'user': user})
    return mycursor.fetchall()

def inser_event(data):
    mycursor = mydb.cursor()
    sql = "INSERT INTO eventos (id, user, nombre_evento, categoria_evento, lugar_evento, direccion_evento, fecha_inicio_evento, fecha_fin_evento, modo_evento) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    mycursor.execute(sql, data)
    mydb.commit()
    return mycursor.rowcount

def select_events(user):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM eventos WHERE user = %(user)s ORDER BY fecha_inicio_evento DESC", {'user': user})
    return mycursor.fetchall()

def select_event(user, id):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM eventos WHERE user = %(user)s AND id=%(id)s", {'user': user, 'id': id})
    return mycursor.fetchall()

def delete_event(user, id):
    mycursor = mydb.cursor()
    mycursor.execute("DELETE from eventos WHERE user=%(user)s AND id=%(id)s", {'user': user, 'id': id})
    mydb.commit()
    return mycursor.rowcount

def update_event(data):
    mycursor = mydb.cursor()
    mycursor.execute("UPDATE eventos SET id=%s, user=%s, nombre_evento=%s, categoria_evento=%s, lugar_evento=%s, direccion_evento=%s, fecha_inicio_evento=%s, fecha_fin_evento=%s, modo_evento=%s WHERE user=%s AND id=%s", data)
    mydb.commit()
    return mycursor.rowcount
