from flask import Flask, flash, render_template, request, jsonify, redirect, url_for
from flask_login import LoginManager, current_user, login_required, login_user
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from database import confbd
from sqlalchemy import text
from database.confbd import db, inicializar
from modelos.discapacidad import Discapacidad
from modelos.municipio import Municipio
from modelos.ocupacion import Ocupacion
from modelos.pais import Pais
from modelos.modificardis import ModificarDis

app = Flask(__name__)
inicializar(app)
migrate = Migrate(app, db)

#RUTA PARA PROBAR CONEXION 
@app.route('/test-db')
def test_db():
    try:
       
        result = db.session.execute(text('SELECT 1'))
        return 'Conexión exitosa a la base de datos 🟢'
    except Exception as e:
        return f'Error al conectar con la base de datos 🔴: {str(e)}'


@app.route('/paises', methods = ["GET"])
def paises ():
    lista_paises = Pais.query.order_by(Pais.nombre).all()
    return render_template("paises.html", paises = lista_paises)

@app.route('/discapacidad', methods = ["GET"])
def discapacidades ():
     lista_discapacidades = Discapacidad.query.order_by(Discapacidad.nombre).all() 
     return render_template("discapacidades.html", discapacidades = lista_discapacidades)

@app.route('/ocupacion', methods = ["GET"])
def ocupaciones ():
    lista_ocupaciones = Ocupacion.query.order_by(Ocupacion.nombre).all()
    return render_template("ocupaciones.html", ocupacion = lista_ocupaciones)

@app.route('/municipio', methods = ["GET"])
def municipios ():
    lista_municipio = Municipio.query.order_by(Municipio.nombre).all()
    return render_template("municipios.html", municipio = lista_municipio)

@app.route('/modificardis', methods=["GET"])
def modificardis():
    lista_modificardis = ModificarDis.query.order_by(ModificarDis.nombre).all()
    return render_template("modificardis.html", modificarDIS=lista_modificardis)

@app.route('/modificardis/agregar', methods=['GET', 'POST'])
def agregar_modificardis():
    if request.method == 'POST':
        nombre = request.form['nombre']
        tipo_doc = request.form['tipo_doc']
        numero_doc = request.form['numero_doc']

        nuevo_documento = ModificarDis(
            nombre=nombre,
            tipo_doc=tipo_doc,
            numero_doc=numero_doc
        )
        try:
            db.session.add(nuevo_documento)
            db.session.commit()
            return redirect(url_for('modificardis'))
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error al agregar documento: {e}")
            return render_template('agregar_modificardis.html')
    return render_template('agregar_modificardis.html')

@app.route('/modificardis/editar/<int:id>', methods=['GET', 'POST'])
def editar_modificardis(id):
    documento = ModificarDis.query.get_or_404(id)
    if request.method == 'POST':
        documento.nombre = request.form['nombre']
        documento.tipo_doc = request.form['tipo_doc']
        documento.numero_doc = request.form['numero_doc']
        try:
            db.session.commit()
            return redirect(url_for('modificardis'))
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error al actualizar documento: {e}")
            return render_template('editar_modificardis.html', documento=documento)
    return render_template('editar_modificardis.html', documento=documento)

@app.route('/modificardis/eliminar/<int:id>', methods=['GET'])
def eliminar_modificardis(id):
    documento = ModificarDis.query.get_or_404(id)
    try:
        db.session.delete(documento)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error al eliminar documento: {e}")
    return redirect(url_for('modificardis'))

if __name__ == '__main__':
    with app.app_context():  
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)
