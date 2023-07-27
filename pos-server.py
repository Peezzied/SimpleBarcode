import threading
import time
import json
import sys
import subprocess

import serial
from flask import Flask, request, render_template, jsonify
from flask_socketio import SocketIO, emit
from PIL import Image
from plyer import notification
import os
import pystray
import pyperclip
import pyautogui

app = Flask(__name__, template_folder='templates')
socketio = SocketIO(app, async_mode='threading')
returnVal = 'null'
modeExt = {
    'token': [None, None]
}
isClientOn = False

@app.route('/')
def index():
    return render_template('index.html', product=returnVal)
@app.route('/receive_value', methods=['POST'])
def excel():
    global returnVal
    data = request.json
    returnVal = data['product']
    
    print(f"Return Value: {returnVal}")
    #shared_data['message'] = data['message']
    # Emit a WebSocket event to send the data to connected clients
    socketio.emit('last_scan', {'lastScan': returnVal})
    return 'Value received successfully'
@app.route('/barcode', methods=['GET'])
def process_barcode(data="data"):
    socketio.emit('barcode', 'test')
    print("Barcode Scanned:", data)
    return 'Get'

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('last_scan', {'lastScan': returnVal})
    global isClientOn
    isClientOn = True

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')
    global isClientOn
    isClientOn = False

#@app.route('/last_scan', methods=['GET'])
#def last_scan():
#    return jsonify({'lastScan': returnVal})

@socketio.on('receive_value')
def excel(data):
    global returnVal
    returnVal = data['product']
    print(f"Return Value: {returnVal}")
    emit('value_received', 'Value received successfully')
    return

@socketio.on('send_data')
def send_data(data):
    mode = data['mode']
    if 'token' in data:
        if 'mhyrenzpharmacy' not in data.get('token', []):
            print('Invalid request')
            socketio.emit('response', 'Invalid Request')
            return

    if 'inputBoxValue' or 'quantityValue' in data:
        inputBoxValue = data.get('inputBox')
        quantityValue = data.get('quantity')
        payload = {
            'lastRead': returnVal
        }
        response = {
            'message': f'Product {inputBoxValue} with amount of {quantityValue} has successfully encoded.',
            'payload': payload
        }

        if isinstance(quantityValue, (str, int)):
            pyautogui.press('esc')
            pyautogui.hotkey('shift', 'ctrl', 'f5') if mode == 'withQuantity' or mode == 'instantScan' else None
            pyperclip.copy(str(inputBoxValue))
            pyautogui.write(f'{str(inputBoxValue)}+{str(quantityValue)}') \
                if mode == 'withQuantity' or mode == 'instantScan' else pyautogui.write(str(inputBoxValue))
            pyautogui.press('enter')

            show_notification("Barcode Received", f"{inputBoxValue} with quantity of {quantityValue}")
            # Process the received data as needed
            print(f"Input Box: {inputBoxValue}")
            print(f"Quantity: {quantityValue}")
            print(response)

            socketio.emit('response', json.dumps(response))
            return
        else:
            socketio.emit('response', 'Error: Invalid keystrokes format. Expected a string or number.')
            return

    socketio.emit('response', 'Error: Unauthorized')
    return
@socketio.on('mode')
def get_mode(data):
    global modeExt
    modeExt = data
    print("data is ", modeExt)
    print("mode is ", modeExt['mode'])

#NOTIFS
def exit_action(tray):
    show_notification("Server Stop", "The barcode server will no longer receive datas.")
    tray.stop()
    time.sleep(2)
    os._exit(0)
def show_notification(title, msg):
    notification.notify(
        app_name="Mhyrenz BarcodeSys",
        title=title,
        message=msg,
        app_icon="./templates/icon.ico",
        timeout=2
    )
def setup_system_tray():
    icon = Image.open("./static/icon.png")
    tray = pystray.Icon("Mhyrenz BarcodeSys", icon, menu=pystray.Menu(
        pystray.MenuItem("Stop Server", exit_action)
    ), hover_text="Mhyrenz BarcodeSys")
    tray.run()


#HARDWARE CATCH
SERIAL_PORT = 'COM9'  # Change this to your barcode scanner's serial port
SERIAL_BAUDRATE = 9600

# Create a global variable to hold the serial connection
ser = serial.Serial()
def setup_serial():
    try:
        ser.port = SERIAL_PORT
        ser.baudrate = SERIAL_BAUDRATE
        ser.timeout = 0.1
        ser.open()
        print(f"Serial port {SERIAL_PORT} opened successfully.")
    except Exception as e:
        print(f"Failed to open serial port {SERIAL_PORT}: {e}")
        os._exit(1)
def read_from_scanner():
    while True:
        try:
            if ser.is_open:
                data = ser.readline().strip().decode('utf-8')
                if data:
                    print(f"Barcode scanned: {data}")
                    socketio.start_background_task(handle_barcode_scan, data)

        except Exception as e:
            print(f"Error reading from the scanner: {e}")
def handle_barcode_scan(data):
    # This function will be executed in the main thread, so it can use socketio.emit safely

    global isClientOn
    print("isclienton", isClientOn)
    if isClientOn == False:
        global modeExt
        print(modeExt.get('token', []))
        if 'mhyrenzpharmacy-out' in modeExt.get('token', []):
            print('inside mode')
            print(modeExt)
            modeExt['inputBox'] = data
            send_data(modeExt) if modeExt['mode'] == 'instantScan' else show_notification('Unable to send',
                                                                                          f'Barcode data is {data}. Change mode to Quick Mode on the app.')
        else:
            show_notification('Error', 'Run the app first to set mode.')
    else:
        socketio.emit('barcode', str(data))



if __name__ == '__main__':

    system_tray_thread = threading.Thread(target=setup_system_tray)
    system_tray_thread.start()

    setup_serial()
    scanner_thread = threading.Thread(target=read_from_scanner)
    scanner_thread.daemon = True
    scanner_thread.start()

    print('Server started successfully [WEBSOCKET].')
    socketio.run(app, host='0.0.0.0', port=5000, debug=False, use_reloader=False, allow_unsafe_werkzeug=True)

