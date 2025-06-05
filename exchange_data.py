import rtde.rtde as rtde
import rtde.rtde_config as rtde_config
from time import sleep


class RTDE_ed:
    def __init__(self, robot_ip="192.168.1.100", robot_port=30004,config_file_path="data.xml",frequency=500):
        print("-------------------------------")
        print("[LOG]: Initial RTDE parameters")

        ROBOT_HOST = robot_ip
        ROBOT_PORT = robot_port
        config_filename = config_file_path

        # Get data
        conf = rtde_config.ConfigFile(config_filename)
        self.out_names, self.out_types = conf.get_recipe("outs")
        self.in_names, self.in_types = conf.get_recipe("ins")
        self.watchdog_name, self.watchdog_type = conf.get_recipe("watchdog")

        # Connect to robot
        self.con = rtde.RTDE(ROBOT_HOST, ROBOT_PORT)
        self.con.connect()
        if not self.con.is_connected():
            self.con.connect()
            sleep(1)
        # Setup recipes
        self.con.send_output_setup(self.out_names, self.out_types)
        self.inputs = self.con.send_input_setup(self.in_names, self.in_types)
        self.watchdog = self.con.send_input_setup(
            self.watchdog_name, self.watchdog_type
        )
        # Initial input value
        self.init_rtde_parameters()
        print("[INFO]: Done! Now you can use RTDE to exchange data with robot")
        # Start data synchronization
        while not self.con.send_start():
            print("[Error]: Cannot synchronize data. Try to reconnect in 3s")
            sleep(3)
            self.reconnect()
        # Frequency send data
        self.con.send_output_setup(frequency=frequency)
    def init_rtde_parameters(self):
        """
        Button:
        - 64: Dpad-X-up
        - 65: Dpad-X-down
        - 66: Dpad-y-up
        - 67: Dpad-y-down
        - 68: Button 0 (Z-up)
        - 69: Button 1 (Rz-up)
        - 70: Button 2 (Z-down)
        - 71: Button 3 (Rz-down)
        - 72: Button 4
        - 73: Button 5
        - 74: Button 6
        - 75: Button 7
        """
        self.inputs.input_bit_register_64 = False
        self.inputs.input_bit_register_65 = False
        self.inputs.input_bit_register_66 = False
        self.inputs.input_bit_register_67 = False
        self.inputs.input_bit_register_68 = False
        self.inputs.input_bit_register_69 = False
        self.inputs.input_bit_register_70 = False
        self.inputs.input_bit_register_71 = False
        self.inputs.input_bit_register_72 = False
        self.inputs.input_bit_register_73 = False
        self.inputs.input_bit_register_74 = False
        self.inputs.input_bit_register_75 = False
        self.inputs.input_bit_register_76 = False

        """
           Analog:
            - 24: Analog axis 1 up  
            - 25: Analog axis 1 down
            - 26: Analog axis 2 up  
            - 27: Analog axis 2 down
            - 28: Analog axis 3 up  
            - 29: Analog axis 3 down
            - 30: Analog axis 4 up  
            - 31: Analog axis 4 down

        """
        self.inputs.input_double_register_24 = 0.0
        self.inputs.input_double_register_25 = 0.0
        self.inputs.input_double_register_26 = 0.0
        self.inputs.input_double_register_27 = 0.0
        self.inputs.input_double_register_28 = 0.0
        self.inputs.input_double_register_29 = 0.0
        self.inputs.input_double_register_30 = 0.0
        self.inputs.input_double_register_31 = 0.0

        """
            Input value explain:
                - 0: Not detect
                - 1: Cylinder - Assembly
                - 2: Cylinder - Good 
                - 3: Cylinder - NG
                - 4: Retangle - Good
                - 5: Retangle - NG 
                - 6: Square
        """
        self.inputs.input_int_register_24 = 0

        """
            Initial watchdog value
        """
        self.watchdog.input_int_register_0 = 0

    def receive_data_from_robot(self):
        result = self.con.receive()
        return result.output_bit_register_64

    def bool_list_to_inputs(self, data, start=64):
        for i, value in enumerate(data[0:2]):
            if value > 0:
                self.inputs.__dict__[f"input_bit_register_{start + i * 2}"] = True
                self.inputs.__dict__[f"input_bit_register_{start + i * 2 + 1}"] = False
            elif value < 0:
                self.inputs.__dict__[f"input_bit_register_{start + i * 2}"] = False
                self.inputs.__dict__[f"input_bit_register_{start + i * 2 + 1}"] = True
            else:
                self.inputs.__dict__[f"input_bit_register_{start + i * 2}"] = False
                self.inputs.__dict__[f"input_bit_register_{start + i * 2 + 1}"] = False

        # Bắt đầu lại từ thanh ghi 68
        start = 68
        for i, value in enumerate(data[2:]):
            if value != 0:
                value = True
            else:
                value = False
            self.inputs.__dict__[f"input_bit_register_{start + i}"] = value

    def double_list_to_inputs(self, data, start=24):
        for i, value in enumerate(data):
            self.inputs.__dict__[f"input_double_register_{start + i}"] = value

    def send_data_to_robot_joystick(self, bool_data, double_data):
        self.bool_list_to_inputs(bool_data)
        self.double_list_to_inputs(double_data)
        self.con.send(self.inputs)
        return print("[INFO]: Data sent to robot completely")

    def send_data_to_robot_vision(self, data):
        if isinstance(data, int):
            self.inputs.input_int_register_24 = data
        if isinstance(data, str):
            for i in range(1, 6, 1):
                if f"class_{i}" == data:
                    data = i
                    self.inputs.input_int_register_24 = data
                    break
        self.con.send(self.inputs)
        self.watchdog.input_int_register_0 += 1
        self.con.send(self.watchdog)
        return print("[INFO]: Data sent to robot completely")

    def reconnect(self):
        print("[INFO]: Disconnecting ...")
        self.con.disconnect()
        sleep(0.1)
        print("[INFO]: Connecting to robot")
        self.con.connect()
        sleep(0.5)
        print("[INFO]: Initial RTDE")
        self.con.send_output_setup(self.out_names, self.out_types)
        self.inputs = self.con.send_input_setup(self.in_names, self.in_types)
        self.init_rtde_parameters()

        # Cần thêm phần này:
        success = self.con.send_start()
        if not success:
            print(
                "[FATAL]: Không thể đồng bộ với robot sau khi reconnect. Kiểm tra trạng thái robot."
            )
            raise RuntimeError("RTDE synchronization failed.")

    def disconnect_rtde(self):
        print("[INFO]: Disconnecting RTDE .....")
        self.con.disconnect()
        print("[INFO]: Disconnect completed")


# Test
# robot = RTDE_ed()
# robot.send_data_to_robot(5)
