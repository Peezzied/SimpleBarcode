import threading
import time
import json
import sys
import subprocess
from flask import Flask, request, render_template, jsonify
from flask_socketio import SocketIO, emit
from PIL import Image
from plyer import notification
import os
import pystray
import pyperclip
import pyautogui

app = Flask(__name__, template_folder='templates')
socketio = SocketIO(app)
returnVal = 'null'

shared_data = {}

def install_module(module_name):
    subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])
def import_module(module_name):
    try:
        __import__(module_name)
    except ImportError:
        print(f"Module '{module_name}' not found. Installing...")
        install_module(module_name)
        print(f"Module '{module_name}' installed successfully.")
required_modules = ["threading", "time", "json", "flask", "flask_socketio", "PIL", "plyer", "os", "pystray", "pyperclip", "pyautogui"]
# Check and install missing modules
for module in required_modules:
    import_module(module)

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


@socketio.on('connect', namespace='ws')
def handle_connect():
    print('Client connected')
    emit('last_scan', {'lastScan': returnVal})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

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
        token = data['token']
        if token != 'mhyrenzpharmacy':
            emit('response', 'Invalid Request')
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

        #CUSTOMIZE THIS FOR CUSTOM HOTKEY(S)
        #CUSTOMIZE THIS FOR CUSTOM HOTKEY(S)
        #CUSTOMIZE THIS FOR CUSTOM HOTKEY(S) \/ \/ \/
        if isinstance(quantityValue, (str, int)):
            pyautogui.press('esc') if mode == 'withQuantity' else None
            pyautogui.hotkey('shift', 'ctrl', 'f5') if mode == 'withQuantity' else None
            pyautogui.write(str(inputBoxValue)) #2
            pyperclip.copy(str(inputBoxValue))
            pyautogui.press('tab') if mode == 'withQuantity' else None
            pyautogui.write(str(quantityValue)) if mode == 'withQuantity' else None
            pyautogui.press('tab') if mode == 'withQuantity' else pyautogui.press('enter')

            show_notification("Barcode Received", f"{inputBoxValue} with quantity of {quantityValue}")
            # Process the received data as needed
            print(f"Input Box: {inputBoxValue}")
            print(f"Quantity: {quantityValue}")
            print(response)

            socketio.emit('response', json.dumps(response))
            return
        else:
            emit('response', 'Error: Invalid keystrokes format. Expected a string or number.')
            return

    emit('response', 'Error: Unauthorized')
    return


#NOTIFS

def show_notification(icon, item):
    # Add your notification logic here
    print("Notification triggered!")

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



if __name__ == '__main__':
    print('Server started successfully [WEBSOCKET].')
    flask_thread = threading.Thread(target=socketio.run, kwargs={'app': app, 'host': '0.0.0.0', 'port': 5000, 'debug': True, 'use_reloader': False})
    flask_thread.start()

    system_tray_thread = threading.Thread(target=setup_system_tray)
    system_tray_thread.start()

