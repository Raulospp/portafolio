import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
from datetime import datetime
import random

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXT = {'png', 'jpg', 'jpeg', 'gif', 'svg'}

app = Flask(__name__)
app.secret_key = 'dev-secret-key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- DATOS DE EJEMPLO ---
conductores = [
    {'id': 1, 'name': 'Laura Gómez', 'email': 'laura@icesi.edu', 'model': 'Mazda 3', 'plate': 'HBG-214', 'route': 'Ciudad Jardín → Icesi', 'city': 'Cali', 'status': 'Disponible'},
    {'id': 2, 'name': 'Andrés Torres', 'email': 'andres@javeriana.edu', 'model': 'Renault Logan', 'plate': 'JKL-980', 'route': 'Valle del Lili → Javeriana', 'city': 'Cali', 'status': 'Disponible'},
    {'id': 3, 'name': 'Camila Rivas', 'email': 'camila@univalle.edu', 'model': 'Kia Picanto', 'plate': 'ZXP-111', 'route': 'Palmira → Univalle', 'city': 'Palmira', 'status': 'Disponible'},
    {'id': 4, 'name': 'Santiago Pérez', 'email': 'santiago@usc.edu', 'model': 'Chevrolet Onix', 'plate': 'LHT-440', 'route': 'Meléndez → USC', 'city': 'Cali', 'status': 'Disponible'},
    {'id': 5, 'name': 'Daniela Romero', 'email': 'daniela@usb.edu', 'model': 'Hyundai i20', 'plate': 'BGR-567', 'route': 'Pance → San Buenaventura', 'city': 'Cali', 'status': 'Disponible'},
    {'id': 6, 'name': 'Kevin López', 'email': 'kevin@autonoma.edu', 'model': 'Toyota Corolla', 'plate': 'PRT-342', 'route': 'Caney → Autónoma', 'city': 'Cali', 'status': 'Disponible'},
    {'id': 7, 'name': 'Paula Torres', 'email': 'paula@icesi.edu', 'model': 'Nissan March', 'plate': 'UHY-556', 'route': 'Pampalinda → Icesi', 'city': 'Cali', 'status': 'Disponible'},
    {'id': 8, 'name': 'Sebastián Ruiz', 'email': 'sebastian@univalle.edu', 'model': 'Kia Rio', 'plate': 'MNB-778', 'route': 'Jamundí → Univalle', 'city': 'Jamundí', 'status': 'Disponible'},
    {'id': 9, 'name': 'Natalia Castro', 'email': 'natalia@javeriana.edu', 'model': 'Chevrolet Spark GT', 'plate': 'HJP-219', 'route': 'El Ingenio → Javeriana', 'city': 'Cali', 'status': 'Disponible'},
    {'id': 10, 'name': 'Felipe Vargas', 'email': 'felipe@usc.edu', 'model': 'Volkswagen Gol', 'plate': 'RTS-871', 'route': 'Ciudad Córdoba → USC', 'city': 'Cali', 'status': 'Disponible'}
]

pasajeros = [
    {'id': 1, 'name': 'Nicolás Jiménez', 'email': 'nico@javeriana.edu', 'university': 'Javeriana', 'destination': 'Javeriana', 'time': '06:30 AM', 'neighborhood': 'Valle del Lili', 'city': 'Cali', 'status': 'Disponible'},
    {'id': 2, 'name': 'Daniela Cobo', 'email': 'daniela@univalle.edu', 'university': 'Univalle', 'destination': 'Univalle', 'time': '07:00 AM', 'neighborhood': 'Palmira', 'city': 'Palmira', 'status': 'Disponible'},
    {'id': 3, 'name': 'Carlos Mora', 'email': 'carlos@icesi.edu', 'university': 'Icesi', 'destination': 'Icesi', 'time': '08:00 AM', 'neighborhood': 'Ciudad Jardín', 'city': 'Cali', 'status': 'Disponible'},
    {'id': 4, 'name': 'Valentina Ruiz', 'email': 'vale@usc.edu', 'university': 'USC', 'destination': 'USC', 'time': '10:00 AM', 'neighborhood': 'Caney', 'city': 'Cali', 'status': 'Disponible'},
    {'id': 5, 'name': 'Juan Esteban', 'email': 'juan@usb.edu', 'university': 'San Buenaventura', 'destination': 'San Buenaventura', 'time': '12:00 PM', 'neighborhood': 'Pance', 'city': 'Cali', 'status': 'Disponible'},
    {'id': 6, 'name': 'Sara López', 'email': 'sara@autonoma.edu', 'university': 'Autónoma', 'destination': 'Autónoma', 'time': '02:00 PM', 'neighborhood': 'Ciudad Jardín', 'city': 'Cali', 'status': 'Disponible'},
    {'id': 7, 'name': 'Mateo Rojas', 'email': 'mateo@univalle.edu', 'university': 'Univalle', 'destination': 'Univalle', 'time': '05:00 PM', 'neighborhood': 'Jamundí', 'city': 'Jamundí', 'status': 'Disponible'},
    {'id': 8, 'name': 'Luisa Fernández', 'email': 'luisa@icesi.edu', 'university': 'Icesi', 'destination': 'Icesi', 'time': '06:30 PM', 'neighborhood': 'El Ingenio', 'city': 'Cali', 'status': 'Disponible'},
    {'id': 9, 'name': 'Esteban Ortiz', 'email': 'esteban@usc.edu', 'university': 'USC', 'destination': 'USC', 'time': '07:00 PM', 'neighborhood': 'Meléndez', 'city': 'Cali', 'status': 'Disponible'},
    {'id': 10, 'name': 'Juliana Castro', 'email': 'juliana@usb.edu', 'university': 'San Buenaventura', 'destination': 'San Buenaventura', 'time': '08:00 PM', 'neighborhood': 'Pampalinda', 'city': 'Cali', 'status': 'Disponible'}
]

servicios = []  # Lista de viajes activos o completados

def format_price_by_city(city):
    """Genera un precio ajustado según la ciudad"""
    if city.lower() == 'cali':
        return f"{random.uniform(4.0, 9.0):.1f}k COP"   # viajes urbanos compartidos (baratos)
    else:
        return f"{random.uniform(10.0, 16.0):.1f}k COP"  # viajes fuera de Cali (más caros)


# --- RUTAS PRINCIPALES ---
@app.route('/')
def splash():
    return render_template('splash.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/register_driver', methods=['GET', 'POST'])
def register_driver():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        model = request.form.get('model')
        plate = request.form.get('plate')
        route = request.form.get('route')
        city = request.form.get('city')
        new_id = max([c['id'] for c in conductores]) + 1 if conductores else 1
        conductores.append({'id': new_id, 'name': name, 'email': email, 'model': model, 'plate': plate, 'route': route, 'city': city, 'status': 'Disponible'})
        return redirect(url_for('home_driver', driver_id=new_id))
    return render_template('register_driver.html')

@app.route('/register_passenger', methods=['GET', 'POST'])
def register_passenger():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        university = request.form.get('university')
        destination = request.form.get('destination')
        time = request.form.get('time')
        neighborhood = request.form.get('neighborhood')
        city = request.form.get('city')
        new_id = max([p['id'] for p in pasajeros]) + 1 if pasajeros else 1
        pasajeros.append({'id': new_id, 'name': name, 'email': email, 'university': university, 'destination': destination, 'time': time, 'neighborhood': neighborhood, 'city': city, 'status': 'Disponible'})
        return redirect(url_for('home_passenger', passenger_id=new_id))
    return render_template('register_passenger.html')

@app.route('/home_driver/<int:driver_id>')
def home_driver(driver_id):
    driver = next((c for c in conductores if c['id'] == driver_id), None)
    pasajeros_disponibles = [p for p in pasajeros if p['status'] == 'Disponible']
    my_services = [s for s in servicios if s['driver_id'] == driver_id]
    return render_template('home_driver.html', driver=driver, pasajeros=pasajeros_disponibles, servicios=my_services)

@app.route('/home_passenger/<int:passenger_id>')
def home_passenger(passenger_id):
    passenger = next((p for p in pasajeros if p['id'] == passenger_id), None)
    matched_drivers = [d for d in conductores if passenger['destination'].lower() in d['route'].lower() and d['status'] == 'Disponible']
    return render_template('home_passenger.html', passenger=passenger, conductores=matched_drivers or conductores)

@app.route('/directory')
def directory():
    return render_template('directory.html', conductores=conductores, pasajeros=pasajeros)

# --- CREAR UN SERVICIO ---
@app.route('/schedule_service', methods=['POST'])
def schedule_service():
    data = request.form.to_dict()
    role = data.get('role')
    self_id = int(data.get('self_id', 0))
    target_id = int(data.get('target_id', 0))

    # Determinar quién es conductor y quién pasajero
    if role == 'driver':
        driver_id = self_id
        passenger_id = target_id
    else:
        driver_id = target_id
        passenger_id = self_id

    passenger = next((p for p in pasajeros if p['id'] == passenger_id), None)
    driver = next((d for d in conductores if d['id'] == driver_id), None)

    if not passenger or not driver:
        return jsonify({'status': 'error', 'message': 'Datos inválidos'})

    now = datetime.now().strftime('%I:%M %p')
    city = passenger['city']
    price = format_price_by_city(city)

    servicio = {
        'id': len(servicios) + 1,
        'driver_id': driver_id,
        'passenger_id': passenger_id,
        'time': now,
        'price': price,
        'state': 'pendiente'
    }

    servicios.append(servicio)
    driver['status'] = 'Ocupado'
    passenger['status'] = 'En ruta'

    print("🔹 Servicios guardados:", servicios)
    return jsonify({'status': 'ok', 'message': f'Servicio programado con {driver["name"]}', 'servicio': servicio})

# --- PANELES DE VIAJES ---
@app.route('/my_requests/<int:passenger_id>')
def my_requests(passenger_id):
    my_services = [s for s in servicios if s['passenger_id'] == passenger_id]
    return render_template('my_requests.html', services=my_services, passenger_id=passenger_id, conductores=conductores)

@app.route('/my_trips/<int:driver_id>')
def my_trips(driver_id):
    my_services = [s for s in servicios if s['driver_id'] == driver_id and s['state'] != 'completado']
    return render_template('my_trips.html', services=my_services, driver_id=driver_id, pasajeros=pasajeros)

@app.route('/complete_service', methods=['POST'])
def complete_service():
    sid = int(request.form.get('service_id', 0))
    service = next((s for s in servicios if s['id'] == sid), None)
    if service:
        service['state'] = 'completado'
        driver = next((d for d in conductores if d['id'] == service['driver_id']), None)
        passenger = next((p for p in pasajeros if p['id'] == service['passenger_id']), None)
        if driver: driver['status'] = 'Disponible'
        if passenger: passenger['status'] = 'Disponible'
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True)
