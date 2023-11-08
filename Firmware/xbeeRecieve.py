import serial


uart_port = '/dev/ttyS0'

baud_rate = 9600 


ser = serial.Serial(uart_port, baud_rate, timeout=1)

try:
    while True:
        if ser.inWaiting():
            incoming = ser.readline().decode('utf-8').strip()
            print(f"Received: {incoming}")
except KeyboardInterrupt:

    ser.close()
