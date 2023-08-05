import serial


READ_ACTUAL_VAL = "I"

class Connection:
    def __init__(self, port='/dev/ttyS4', baudrate=9600, chamber_address="00"):
        self.port=port
        self.baudrate=baudrate
        self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
    def serial_read(self):
        try:
            return self.ser.readline().decode()
        except UnicodeDecodeError:
            print("read line error. (pyVT4002)")
            return ""
    def serial_write(self, data):
        self.ser.write(data.encode('utf-8'))

    def get_temp(self):
        self.ser.write(("$"+self.chamber_address+data+READ_ACTUAL_VAL).encode('utf-8'))
        return self.serial_read()
