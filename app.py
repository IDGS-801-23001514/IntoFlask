from flask import Flask, render_template, request
from flask import flash
from flask_wtf.csrf import CSRFProtect

import forms

app = Flask(__name__)
app.secret_key='clave secreta'

csrf=CSRFProtect()

@app.route("/")
def index():
    titulo="Flask IDGS801"
    lista=["Juan", "Mario","Pedro", "Dario"]
    return render_template("index.html", titulo=titulo, lista=lista)

@app.route("/operasBas", methods=['GET','POST'])
def operas1():
    n1=0
    n2=0
    res=0
    if request.method=='POST':
        n1=request.form.get('n1')
        n2=request.form.get('n2')
        res=float(n1)+float(n2)
    return render_template("operasBas.html",n1=n1,n2=n2,res=res)

@app.route("/resultado", methods=['GET','POST'])
def resultado():
    n1=request.form.get('n1')
    n2=request.form.get('n2')
    temp=float(n1)+float(n2)
    return f"La suma de {n1} y {n2} es: {temp}"

@app.route("/alumnos")
def alumnos():
    return render_template("alumnos.html")

@app.route("/usuarios",methods=['GET','POST'])
def usuarios():
    mat=0
    nom=''
    apa=''
    ama=''
    email=''
    usuarios_class=forms.UserForm(request.form)
    if request.method=='POST' and usuarios_class.validate():
        mat=usuarios_class.matricula.data
        nom=usuarios_class.nombre.data
        apa=usuarios_class.apaterno.data
        ama=usuarios_class.amaterno.data
        email=usuarios_class.correo.data
        mensaje='Bienvenido {}'.format(nom)
        flash(mensaje)
        
    return render_template("usuarios.html", form=usuarios_class,
                           mat=mat,nom=nom,apa=apa,ama=ama,email=email)

@app.route("/hola")
def hola():
    return "Hola, mundo"

@app.route("/user/<string:user>")
def user(user):
    return f"Hello, {user}!"

@app.route("/numero/<int:n>")
def numero(n):
    return f"<h1>El numero es:{n}</h1>"

@app.route("/user/<int:id>/<string:username>")
def username(id, username):
    return f"<h1>Hola, {username}! Tu ID es: {id}</h1>"

@app.route("/suma/<float:n1>/<float:n2>")
def suma(n1,n2):
    return f"<h1>La suma es : {n1+n2}</h1>"

@app.route("/default")
@app.route("/default/<string:param>")
def func(param = "juan"):
    return f"<h1>¡Hola, {param}!</h1>"
   
@app.route("/operas")
def operas():
    return """
            <from>
            <label for = "name">Name:<label>
            <input type="text" id="name" name="name" required>
            </br>
            <label for="name">apaterno:</label>
            <input type="text" id="name" name="name" required>
    </form>
            """
  
@app.route('/cinepolis', methods=['GET', 'POST'])
def cinepolis():
    resultado = None
    cinepolis_form = forms.CinepolisForm(request.form)
    
    if request.method == 'POST' and cinepolis_form.validate():
        nombre = cinepolis_form.nombre.data
        personas = cinepolis_form.personas.data
        cantidad = cinepolis_form.cantidad.data
        tarjeta_cineco = cinepolis_form.tarjeta_cineco.data
        
        limite_boletos = 7 * personas
        
        if cantidad > limite_boletos:
            flash(f"Error: Cada persona puede comprar máximo 7 boletos. Para {personas} persona(s) el límite es {limite_boletos} boletos. Intentaste comprar {cantidad} boletos.")
            return render_template('cinepolis.html', form=cinepolis_form, resultado=resultado)
        
        boletos_por_persona = cantidad / personas
        precio_boleta = 12
        subtotal = precio_boleta * cantidad
        
        if boletos_por_persona > 5:
            descuento_cantidad = 0.15
        elif boletos_por_persona >= 3:
            descuento_cantidad = 0.10
        else:
            descuento_cantidad = 0.0
        
        monto_descuento = subtotal * descuento_cantidad
        total = subtotal - monto_descuento
        
        descuento_cineco = 0
        if tarjeta_cineco:
            descuento_cineco = total * 0.10
            total = total - descuento_cineco
        
        resultado = {
            'nombre': nombre,
            'personas': personas,
            'cantidad': cantidad,
            'boletos_por_persona': boletos_por_persona,
            'precio_boleta': precio_boleta,
            'subtotal': subtotal,
            'descuento_cantidad': descuento_cantidad * 100,
            'monto_descuento': monto_descuento,
            'descuento_cineco': descuento_cineco,
            'total': total,
            'tiene_tarjeta': tarjeta_cineco
        }
        
        mensaje = f"Compra procesada para {personas} persona(s). Total: ${total:.2f}"
        flash(mensaje)
    
    return render_template('cinepolis.html', form=cinepolis_form, resultado=resultado)

@app.route("/distancia", methods=["GET", "POST"])
def calcular_distancia():
    resultado_distancia = None
    
    if request.method == "POST":
            x1 = float(request.form.get("x1", 0))
            x2 = float(request.form.get("x2", 0))
            y1 = float(request.form.get("y1", 0))
            y2 = float(request.form.get("y2", 0))
            
            dx = x2 - x1
            dy = y2 - y1
            resultado_distancia = ((dx**2) + (dy**2))**0.5
            resultado_distancia = round(resultado_distancia, 2)
    return render_template("distancia.html", resultado=resultado_distancia)



if __name__ == "__main__":
    csrf.init_app(app)    
    app.run(debug = True)