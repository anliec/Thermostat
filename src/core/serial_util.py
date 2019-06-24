import serial


class ArdiunoSerialInterface:
    def __init__(self, serial_port="/dev/ttyUSB0"):
        try:
            self.serial = serial.Serial(serial_port)
            self.is_fake_serial = False
        except serial.SerialException:
            print("Unable to setup Serial connection, setting up fake serial for testing purpose")

            class FakeSerial:
                write = print
                in_waiting = 0

            self.serial = FakeSerial()
            self.is_fake_serial = True
        self.last_values = {"temperature": -999.0,
                            "humidity": -999.0,
                            "relay1": -1,
                            "relay2": -1}

    def read_data(self):
        while self.serial.in_waiting > 2:
            line = self.serial.readline()
            line = line.decode()
            if line[-1] != "\n":
                print("line not fully read: '{}'".format(line))
                break
            line = line[:-1]
            split = line.split(":")
            if len(split) != 2:
                # print("Unreconised data ligne: \"{}\"".format(line))
                break
            label, data = split
            if label == "t":
                self.last_values["temperature"] = float(data)
            elif label == "h":
                self.last_values["humidity"] = float(data)
            elif label == "1":
                self.last_values["relay1"] = int(data)
            elif label == "2":
                self.last_values["relay2"] = int(data)
            else:
                pass
                print("unknown label: '{}', line was '{}'".format(str(label), str(line)))
        return self.last_values

    def write_relay1(self, status: bool):
        # print("write send")
        if status:
            self.serial.write("0".encode())
        else:
            self.serial.write("1".encode())

    def write_relay2(self, status: bool):
        # print("write send")
        if status:
            self.serial.write("2".encode())
        else:
            self.serial.write("3".encode())



