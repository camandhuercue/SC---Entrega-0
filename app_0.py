from flask import Flask, render_template, request, redirect, session
import hash_passwd
import db

app = Flask(__name__)

app.secret_key = 'ds4%%4rfdsf&&$34/.__$/((dsdsada"'

@app.route("/")
@app.route("/index")
def index():
    if session.get("user"):
        return redirect('/eventos')
    if request.path == "/index":
        return redirect('/')
    return render_template('index.html')

@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return redirect('/')
    elif request.method == 'POST':
        usuario = request.form['user']
        contrasena = request.form['passwd']
        resultado = db.select_user(usuario)
        if len(resultado) == 0:
            return "<p>usuario no existe</p>"
        for r in resultado:
            user, name, hash = r
            flag = hash_passwd.check_passwd(bytes(contrasena, 'utf-8'), bytes(hash, 'utf-8'))
            if flag:
                session['user'] = usuario
                return redirect('/eventos')
            else:
                return "<p>usuario o contraseña erronea</p>"

@app.route("/logout")
def logout():
    session["user"] = None
    return redirect('/')

@app.route("/eventos")
def eventos():
    eventos_html = ""
    eventos_template = """
                      <div class="row align-items-start">
                        <div class="col">
                          {n_evento}
                        </div>
                        <div class="col">
                          {f_inicio}
                        </div>
                        <div class="col">
                          {f_fin}
                      </div>
                        <div class="col">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-eye" viewBox="0 0 16 16" type="submit" onclick="location.href = 'evento/{id}';">
                                <path d="M16 8s-3-5.5-8-5.5S0 8 0 8s3 5.5 8 5.5S16 8 16 8zM1.173 8a13.133 13.133 0 0 1 1.66-2.043C4.12 4.668 5.88 3.5 8 3.5c2.12 0 3.879 1.168 5.168 2.457A13.133 13.133 0 0 1 14.828 8c-.058.087-.122.183-.195.288-.335.48-.83 1.12-1.465 1.755C11.879 11.332 10.119 12.5 8 12.5c-2.12 0-3.879-1.168-5.168-2.457A13.134 13.134 0 0 1 1.172 8z"/>
                                <path d="M8 5.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5zM4.5 8a3.5 3.5 0 1 1 7 0 3.5 3.5 0 0 1-7 0z"/>
                            </svg>
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil" viewBox="0 0 16 16" type="submit" onclick="location.href = 'modificar_evento/{id}';">
                                <path d="M12.146.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1 0 .708l-10 10a.5.5 0 0 1-.168.11l-5 2a.5.5 0 0 1-.65-.65l2-5a.5.5 0 0 1 .11-.168l10-10zM11.207 2.5 13.5 4.793 14.793 3.5 12.5 1.207 11.207 2.5zm1.586 3L10.5 3.207 4 9.707V10h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.293l6.5-6.5zm-9.761 5.175-.106.106-1.528 3.821 3.821-1.528.106-.106A.5.5 0 0 1 5 12.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.468-.325z"/>
                            </svg>
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16" type="submit" onclick="location.href = 'eliminar_evento/{id}';">
                                <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"/>
                                <path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"/>
                            </svg>
                          </div>
</div>
"""
    if not session.get("user"):
        return redirect('/')
    usuario = session.get("user")
    resultado = db.select_user(usuario)
    for r in resultado:
        user, name, hash = r
    eventos = db.select_events(usuario)
    for e in eventos:
        id, user, nombre_evento, categoria_evento, lugar_evento, directorio_evento, fecha_inicio, fecha_fin, modo_evento = e
        eventos_html = eventos_html + eventos_template.format(n_evento=nombre_evento, f_inicio=fecha_inicio, f_fin=fecha_fin, id=id)
    return render_template('eventos.html',nombre_usuario=name, template=eventos_html)

@app.route("/nuevo_evento", methods=['POST', 'GET'])
def nuevo_evento():
    if request.method == 'GET':
        if not session.get("user"):
            return redirect('/')
        usuario = session.get("user")
        resultado = db.select_user(usuario)
        for r in resultado:
            user, name, hash = r
        return render_template('nuevo_evento.html', nombre_usuario=name)

    if request.method == 'POST':
        if not session.get("user"):
            return redirect('/')
        usuario = session.get("user")
        resultado = db.select_user(usuario)
        for r in resultado:
            user, name, hash = r
        nombre_evento = request.form['nombre_evento']
        tipo_evento = request.form['tipo_evento']
        lugar_evento = request.form['lugar_evento']
        direccion_evento = request.form['direccion_evento']
        fechai_evento = request.form['fechai_evento']
        fechaf_evento = request.form['fechaf_evento']
        modo_evento = request.form['modo_evento']
        data = (None, user, nombre_evento, tipo_evento, lugar_evento, direccion_evento, fechai_evento, fechaf_evento, modo_evento)
        db.inser_event(data)
        return redirect('/eventos')

@app.route("/registro", methods=['POST', 'GET'])
def registro():
    error_correo = ""
    error_nombre = ""
    error_passwd1 = ""
    error_passwd2 = ""
    mensaje_correo = ""
    mensaje_nombre = ""
    mensaje_passwd1 = ""
    mensaje_passwd2 = ""
    if request.method == 'GET':
        return render_template('registro.html', error_correo=error_correo, error_nombre=error_nombre, error_passwd1=error_passwd1, mensaje_correo=mensaje_correo, mensaje_nombre=mensaje_nombre, mensaje_passwd1=mensaje_passwd1, error_passwd2=error_passwd2, mensaje_passwd2=mensaje_passwd2)
    elif request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        passwd1 = request.form['passwd1']
        passwd2 = request.form['passwd2']
        if (nombre == "" or nombre is None) and not nombre.isspace():
            error_nombre = "is-invalid"
            mensaje_nombre = '<small class="text-muted">Este campo es Necesario</small>'
        if (correo == "" or correo is None) and not correo.isspace():
            error_correo = "is-invalid"
            mensaje_correo = '<small class="text-muted">Este campo es Necesario</small>'
        if len(passwd1) == 0:
            error_passwd1 = "is-invalid"
            mensaje_passwd1 = '<small class="text-muted">Este campo es Necesario</small>'
        if len(passwd2) == 0:
            error_passwd2 = "is-invalid"
            mensaje_passwd2 = '<small class="text-muted">Este campo es Necesario</small>'
        if (passwd1 == passwd2) and (len(passwd1) != 0):
            if len(db.select_user(correo)) > 0:
                return "<p>El usuario ya existe</p>"
            hash_pw = hash_passwd.hash_passwd(bytes(passwd1, 'utf-8')).decode("utf-8")
            data = (correo, nombre, hash_pw)
            try:
                db.insert_user(data)
                return "<p>exitoso</p>"
            except:
                return "<p>error</p>"
        else:
            if error_passwd2 == "":
                error_passwd2 = "is-invalid"
                mensaje_passwd2 = '<small class="text-muted">Las contraseñas no coinciden</small>'
            return render_template('registro.html', error_correo=error_correo, error_nombre=error_nombre, error_passwd1=error_passwd1, mensaje_correo=mensaje_correo, mensaje_nombre=mensaje_nombre, mensaje_passwd1=mensaje_passwd1, error_passwd2=error_passwd2, mensaje_passwd2=mensaje_passwd2)

@app.route("/evento/<int:id>")
def mod_evento(id):
    print(id)
    if request.method == "GET":
        if not session.get("user"):
            return redirect('/')
        usuario = session.get("user")
        evento = db.select_event(usuario, id)
        print(len(evento))
        if len(evento) == 0:
            return redirect('/eventos')
        for e in evento:
            id, user, nombre_evento, categoria_evento, lugar_evento, directorio_evento, fecha_inicio, fecha_fin, modo_evento = e
        return render_template('ver_evento.html', id=id, user=user, nombre_evento=nombre_evento, categoria_evento=categoria_evento, lugar_evento=lugar_evento, directorio_evento=directorio_evento, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, modo_evento=modo_evento)

@app.route("/eliminar_evento/<int:id>", methods=["GET", "POST"])
def eliminar_evento(id):
    if request.method == "GET":
        if not session.get("user"):
            return redirect('/')
        usuario = session.get("user")
        evento = db.select_event(usuario, id)
        if len(evento) == 0:
            return redirect('/eventos')
        for e in evento:
            id, user, nombre_evento, categoria_evento, lugar_evento, directorio_evento, fecha_inicio, fecha_fin, modo_evento = e
        return render_template('eliminar_evento.html', id=id, user=user, nombre_evento=nombre_evento, categoria_evento=categoria_evento, lugar_evento=lugar_evento, directorio_evento=directorio_evento, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, modo_evento=modo_evento)
    if request.method == "POST":
        if not session.get("user"):
            return redirect('/')
        usuario = session.get("user")
        evento = db.select_event(usuario, id)
        if len(evento) == 0:
            return redirect('/eventos')
        cantidad = db.delete_event(usuario, id)
        if cantidad == 0:
            return redirect('/')
        return redirect('/eventos')

@app.route("/modificar_evento/<int:id>", methods=["GET", "POST"])
def modificar_evento(id):
    if request.method == "GET":
        if not session.get("user"):
            return redirect('/')
        usuario = session.get("user")
        evento = db.select_event(usuario, id)
        if len(evento) == 0:
            return redirect('/eventos')
        for e in evento:
            id, user, nombre_evento, categoria_evento, lugar_evento, directorio_evento, fecha_inicio, fecha_fin, modo_evento = e
        return render_template('editar_evento.html', id=id, nombre_user=usuario, nombre_evento=nombre_evento, tipo_evento=categoria_evento, lugar_evento=lugar_evento, direccion_evento=directorio_evento, fechai_evento=fecha_inicio, fechaf_evento=fecha_fin, modo_evento=modo_evento)
    if request.method == "POST":
        if not session.get("user"):
            return redirect('/')
        usuario = session.get("user")
        resultado = db.select_user(usuario)
        for r in resultado:
            user, name, hash = r
        nombre_evento = request.form['nombre_evento']
        tipo_evento = request.form['tipo_evento']
        lugar_evento = request.form['lugar_evento']
        direccion_evento = request.form['direccion_evento']
        fechai_evento = request.form['fechai_evento']
        fechaf_evento = request.form['fechaf_evento']
        modo_evento = request.form['modo_evento']
        data = (id, user, nombre_evento, tipo_evento, lugar_evento, direccion_evento, fechai_evento, fechaf_evento, modo_evento, user, id)
        db.update_event(data)
        return redirect('/eventos')
