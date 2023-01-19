from flask import Flask, render_template, request, redirect, url_for
import os
import database as db

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'src', 'templates')

app = Flask(__name__, template_folder = template_dir)

#Rutas de la app

@app.route('/')
def home():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM vehiculos")
    #fetch datos como tupla
    result = cursor.fetchall()
    #pasar los datos a diccionario
    insertObject=[]
    columnNames=[column[0] for column in cursor.description]
    for record in result:
        #usamos zip (hace algo asi como un producto cartesiano)
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template('index.html', data=insertObject)

#Ruta para guardar patentes en la db
@app.route('/agregarVehiculo', methods=['POST'])
def addVehiculo():
    id = request.form['id']
    patente = request.form['Patente']
    marca = request.form['Marca']
    modelo = request.form['Modelo']
    año = request.form['Año']
  
    if patente:
        cursor = db.database.cursor()
        sql = "INSERT INTO vehiculos (Patente, Marca, Modelo, Año) VALUES (%s, %s, %s, %s)"
        data = (patente, marca, modelo, año)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))

app.route('/delete/<string:patente>')
def delete(patente):
        cursor = db.database.cursor()
        sql = "DELETE FROM vehiculos WHERE patente=%s"
        data = (patente)
        cursor.execute(sql, data)
        db.database.commit()
        return redirect(url_for('home'))

app.route('/edit/<string:patente>', methods=["POST"])
def edit(patente):
    patente = request.form['Patente']
    marca = request.form['Marca']
    modelo = request.form['Modelo']
    año = request.form['Año']
  
    if patente:
        cursor = db.database.cursor()
        sql = "UPDATE vehiculos SET Patente=%s, Marca=%s, Modelo=%s, Año=%s WHERE patente=%s)"
        data = (patente, marca, modelo, año)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug = True, port=4000)

