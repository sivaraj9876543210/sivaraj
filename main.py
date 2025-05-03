from flask import Flask, request, jsonify, render_template
import base64
from face_matching import match_face, get_license_info
import time


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

cars = [{'id': 0, 'model': 'V60 Twin Engine', 'fuel': 70, 'cost': 0.22, 'hybrid':  'true', 'lat': 47.43225,  'lon': 9.37429,  'cons': 1.9 / 100.0},
        {'id': 1, 'model': 'V60',             'fuel': 50, 'cost': 0.20, 'hybrid': 'false', 'lat': 47.431706, 'lon': 9.373588, 'cons': 5.95 / 100.0}]

car_info = None

unlock_start = None
avg_vel = 50.0 / 3600.0
time_mul = 1000.0


@app.route('/testjson')
def test_json():

    return jsonify({'success': 'true'})


@app.route('/license_validation', methods=['POST'])
def process_image():
    global magic_counter

    # save received file
    req = request.get_json()
    image = base64.decodestring(req['image'])
    image_file = open('received.png', 'wb')
    image_file.write(image)
    image_file.close()

    match = match_face('received.png')
    info = get_license_info('received.png')

    if match:
        info['success'] = 'true'
        info['message'] = 'OK'
    else:
        info['success'] = 'false'
        info['message'] = 'License does not match, please try again'

    return jsonify(info)


@app.route('/get_cars', methods=['POST'])
def getcars():

    return jsonify(cars)


@app.route('/car', methods=['GET', 'POST'])
def car_page():
    global car_info
    global unlock_start
    global time_mul

    # lock/unlock car
    if request.method == 'POST':
        req = request.get_json()
        if req['action'] == 'lock':

            sharing_time = time_mul*(time.time() - unlock_start)
            km = avg_vel * sharing_time
            cons = km * car_info['cons']
            cost = sharing_time * car_info['cost'] / 60.0

            unlock_start = None
            car_info = None

            return jsonify({'success': 'true',
                            'km': km,
                            'cons': cons,
                            'cost': cost})

        elif req['action'] == 'unlock':
            car_id = req['carid']
            car_info = cars[car_id]
            unlock_start = time.time()
            return jsonify({'success': 'true'})

        else:
            return jsonify({'success': 'false'})

    # GET
    if car_info is None:
        return render_template('car.html',
                               car='Cars standying by')

    sharing_time = time_mul * (time.time() - unlock_start)
    km = avg_vel * sharing_time
    cons = km * car_info['cons']
    cost = sharing_time * car_info['cost'] / 60.0

    return render_template('car.html',
                           car='Selected model: ' + car_info['model'],
                           km='Km from start: %0.2f' % km,
                           cons='Fuel consumption: %0.2f' % cons,
                           cost='Total cost: %0.2fCHF' % cost)


# running web app in local machine
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
