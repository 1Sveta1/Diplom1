import warnings
import serial
import serial.tools.list_ports

arduino_ports = [
    p.device
    for p in serial.tools.list_ports.comports()
    if "Standard Serial over Bluetooth link" in p.description or 'USB-SERIAL CH340' in p.description
]
if not arduino_ports:
    raise IOError("No Arduino found")
else:
    for p in serial.tools.list_ports.comports():
        print(p)

if len(arduino_ports) > 1:
    warnings.warn('Multiple Arduinos found - using the first')
    print(arduino_ports)

ser = serial.Serial(arduino_ports[0])
