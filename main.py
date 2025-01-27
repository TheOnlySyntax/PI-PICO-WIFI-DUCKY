# PicoW Ducky Enhanced with Hak5 USB Rubber Ducky Commands
# Setup for Raspberry Pi Pico W to make a Wifi Ducky.
# Author - WireBits (Enhanced by ChatGPT)

import wifi
import time
import usb_hid
import socketpool
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayout
from adafruit_httpserver import Server, Request, JSONResponse, POST, Response

ssid = "PicoWDucky"
password = "picowducky"

wifi.radio.stop_station()
wifi.radio.start_ap(ssid, password)

pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, "/", debug=True)

kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayout(kbd)

hidKeys = {
    'A': Keycode.A, 'B': Keycode.B, 'C': Keycode.C, 'D': Keycode.D, 'E': Keycode.E,
    'F': Keycode.F, 'G': Keycode.G, 'H': Keycode.H, 'I': Keycode.I, 'J': Keycode.J,
    'K': Keycode.K, 'L': Keycode.L, 'M': Keycode.M, 'N': Keycode.N, 'O': Keycode.O,
    'P': Keycode.P, 'Q': Keycode.Q, 'R': Keycode.R, 'S': Keycode.S, 'T': Keycode.T,
    'U': Keycode.U, 'V': Keycode.V, 'W': Keycode.W, 'X': Keycode.X, 'Y': Keycode.Y,
    'Z': Keycode.Z, 'F1': Keycode.F1, 'F2': Keycode.F2, 'F3': Keycode.F3, 'F4': Keycode.F4,
    'F5': Keycode.F5, 'F6': Keycode.F6, 'F7': Keycode.F7, 'F8': Keycode.F8, 'F9': Keycode.F9,
    'F10': Keycode.F10, 'F11': Keycode.F11, 'F12': Keycode.F12, 'LEFT': Keycode.LEFT_ARROW,
    'UP': Keycode.UP_ARROW, 'RIGHT': Keycode.RIGHT_ARROW, 'DOWN': Keycode.DOWN_ARROW,
    'TAB': Keycode.TAB, 'HOME': Keycode.HOME, 'END': Keycode.END, 'PGUP': Keycode.PAGE_UP,
    'PGDN': Keycode.PAGE_DOWN, 'CAPS': Keycode.CAPS_LOCK, 'NUM': Keycode.KEYPAD_NUMLOCK,
    'SCROLL': Keycode.SCROLL_LOCK, 'CTRL': Keycode.CONTROL, 'SHIFT': Keycode.SHIFT, 'ALT': Keycode.ALT,
    'GUI': Keycode.GUI, 'ESC': Keycode.ESCAPE, 'PRTSCR': Keycode.PRINT_SCREEN, 'PAUSE': Keycode.PAUSE,
    'SPACE': Keycode.SPACE, 'DEL': Keycode.DELETE, 'INSERT': Keycode.INSERT, 'BKSP': Keycode.BACKSPACE,
    'ENTER': Keycode.ENTER, 'APP': Keycode.APPLICATION
}

def convertHID(hidLine):
    newline = []
    for key in filter(None, hidLine.split(" ")):
        key = key.upper()
        command_keycode = hidKeys.get(key, None)
        if command_keycode is not None:
            newline.append(command_keycode)
        elif hasattr(Keycode, key):
            newline.append(getattr(Keycode, key))
        else:
            print("Unknown key! Try another key!")
    return newline

def keyTrigger(hidLine):
    for kd in hidLine:
        kbd.press(kd)
    kbd.release_all()

def typeText(hidLine):
    layout.write(hidLine)

variables = {}
definitions = {}
default_delay = 0.1

# Helper function for status updates
def update_status(status_message, progress):
    print(f"STATUS: {status_message} ({progress}%)")

def generateHID(hidScript):
    global default_delay
    index = 0
    length = len(hidScript)
    while index < length:
        progress = int((index / length) * 100)
        update_status("Running payload", progress)

        hidLine = hidScript[index].strip()

        if hidLine.startswith("REM"):
            index += 1
            continue

        if hidLine.startswith("DELAY"):
            time.sleep(float(hidLine.split(" ")[1]) / 1000)
        elif hidLine.startswith("DEFAULT_DELAY") or hidLine.startswith("DEFAULTDELAY"):
            default_delay = float(hidLine.split(" ")[1]) / 1000

        elif hidLine.startswith("STRING"):
            typeText(hidLine.split(" ", 1)[1])

        elif hidLine.startswith("STRING_DELAY"):
            parts = hidLine.split(" ", 2)
            text_to_type = parts[1]
            delay_ms = float(parts[2])
            for char in text_to_type:
                typeText(char)
                time.sleep(delay_ms / 1000)

        elif hidLine.startswith("HOLD"):
            key = hidLine.split(" ")[1]
            if key in hidKeys:
                kbd.press(hidKeys[key])
        elif hidLine.startswith("RELEASE"):
            key = hidLine.split(" ")[1]
            if key in hidKeys:
                kbd.release(hidKeys[key])

        elif hidLine.startswith("LOOP"):
            loop_count = int(hidLine.split(" ")[1])
            index += 1
            loop_commands = []
            while index < length and not hidScript[index].strip().startswith("END_LOOP"):
                loop_commands.append(hidScript[index])
                index += 1
            for _ in range(loop_count):
                generateHID(loop_commands)

        elif hidLine.startswith("DEFINE"):
            parts = hidLine.split(" ", 2)
            definitions[parts[1]] = parts[2]

        elif hidLine.startswith("VAR"):
            parts = hidLine.split("=", 1)
            name = parts[0].split(" ")[1].strip()
            value = parts[1].strip()
            variables[name] = value

        elif hidLine.startswith("REPEAT"):
            repeat_count = int(hidLine.split(" ")[1])
            for _ in range(repeat_count):
                generateHID([hidScript[index - 1]])

        elif hidLine.startswith("IF"):
            condition = hidLine[3:].strip()
            index += 1
            true_block = []
            false_block = []
            current_block = true_block
            while index < length:
                line = hidScript[index].strip()
                if line.startswith("ELSE"):
                    current_block = false_block
                elif line.startswith("END_IF"):
                    break
                else:
                    current_block.append(line)
                index += 1
            if eval(condition, {}, variables):
                generateHID(true_block)
            else:
                generateHID(false_block)

        elif hidLine.startswith("CALL"):
            func_name = hidLine.split(" ")[1]
            if func_name in definitions:
                generateHID(definitions[func_name])

        else:
            newScriptLine = convertHID(hidLine)
            keyTrigger(newScriptLine)

        time.sleep(default_delay)
        index += 1

    update_status("Payload complete", 100)

progStatus = False

# Add a scheduler
def schedule_payload(hidScript, delay_seconds):
    print(f"Scheduled payload to run in {delay_seconds} seconds...")
    time.sleep(delay_seconds)
    hid_execute(hidScript)

def hid_execute(hidScript):
    global progStatus
    if not progStatus:
        progStatus = True
        generateHID(hidScript)
        progStatus = False
        print("Done")
    else:
        print("Update your payload and start again!")

def handle_index_html(request):
    with open("index.html", "r") as file:
        index_html_content = file.read()
    return Response(request, body=index_html_content, headers={"Content-Type": "text/html"})

@server.route("/")
def base(request: Request):
    return handle_index_html(request)

@server.route("/execute", POST, append_slash=True)
def execute(request: Request):
    if request.method == POST:
        try:
            payload = request.json().get("content", "")
            if isinstance(payload, str):
                payload = payload.splitlines()
                hid_execute(payload)
                return JSONResponse(request, {"message": "Done"})
            else:
                return JSONResponse(request, {"message": "Invalid payload format"}, status_code=400)
        except Exception as e:
            print(f"Error handling request: {e}")
            return JSONResponse(request, {"message": "Error handling request"}, status_code=500)

@server.route("/schedule", POST, append_slash=True)
def schedule(request: Request):
    if request.method == POST:
        try:
            data = request.json()
            payload = data.get("content", "").splitlines()
            delay = int(data.get("delay", 0))
            schedule_payload(payload, delay)
            return JSONResponse(request, {"message": "Scheduled successfully"})
        except Exception as e:
            print(f"Error scheduling payload: {e}")
            return JSONResponse(request, {"message": "Error scheduling payload"}, status_code=500)

try:
    server.serve_forever('192.168.4.1', 80)
except KeyboardInterrupt:
    print("Server stopped by user!")
