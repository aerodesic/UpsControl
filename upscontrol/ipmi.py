import pyipmi
import pyipmi.interfaces

class IPMI_Exception(Exception):
    pass

class IPMI_Control():
    def __init__(self, interface_type="rmcp", slave_address=0x81, host_target_address=0x20, keep_alive_interval=1, host_address=None, host_port=623):
        self.interface_type = interface_type
        self.slave_address = slave_address
        self.host_target_address = host_target_address
        self.keep_alive_interval = keep_alive_interval
        self.host_address = host_address
        self.host_port = host_port
        self.ipmi = None
        self.sensors = {}


    def set_credentials(self, username, password):
        self.username = username
        self.password = password

    def connect(self, username = None, password = None):
        if username is None:
            username = self.username
        if password is None:
            password = self.password

        self.interface = pyipmi.interfaces.create_interface(interface=self.interface_type,
                                                            slave_address=self.slave_address,
                                                            host_target_address=self.host_target_address,
                                                            keep_alive_interval=self.keep_alive_interval)

        self.ipmi = pyipmi.create_connection(self.interface)
        self.ipmi.session.set_session_type_rmcp(host=self.host_address, port=self.host_port)
        self.ipmi.session.set_auth_type_user(username, password)

        # self.ipmi.session.set_priv_level(ipmi.session.PRIV_LEVEL_ADMINISTRATOR)
        self.ipmi.target = pyipmi.Target(ipmb_address=0x20)
        self.ipmi.session.establish()

    def disconnect(self):
        if self.ipmi is not None:
            del(self.ipmi)
            self.ipmi = None

    def is_power_on(self):
        self.connect()

        if self.ipmi is None:
            raise IPMI_Exception("Not connected")

        power_on = self.ipmi.get_chassis_status().power_on

        self.disconnect()

        return power_on

    def hard_reset(self):
        self.connect()

        if self.ipmi is None:
            raise IPMI_Exception("Not connected")

        self.ipmi.chassis_control_hard_reset()

        self.disconnect()

    def power_cycle(self):
        self.connect()

        if self.ipmi is None:
            raise IPMI_Exception("Not connected")

        self.ipmi.chassis_control_power_cycle()

        self.disconnect()

    def power_down(self):
        self.connect()

        if self.ipmi is None:
            raise IPMI_Exception("Not connected")

        self.ipmi.chassis_control_power_down()

        self.disconnect()

    def power_up(self):
        self.connect()

        if self.ipmi is None:
            raise IPMI_Exception("Not connected")

        self.ipmi.chassis_control_power_up()

        self.disconnect()

    def soft_shutdown(self):
        self.connect()

        if self.ipmi is None:
            raise IPMI_Exception("Not connected")

        self.ipmi.chassis_control_soft_shutdown()

        self.disconnect()

    def read_sensors(self):
        self.connect()

        if self.ipmi is None:
            raise IPMI_Exception("Not connected")

        iterator = None

        device_id = self.ipmi.get_device_id()
        if device_id.supports_function("sdr_repository"):
            iterator = self.ipmi.sdr_repository_entries()
        elif device_id.supports_function("sensor"):
            iterator = self.ipmi.device_sdr_entries()

        count = 0

        if iterator is not None:
            for sensor in iterator:
                sensor_name = sensor.device_id_string.decode()
                try:
                    if sensor.type is pyipmi.sdr.SDR_TYPE_FULL_SENSOR_RECORD:
                        try:
                            (value, states) = self.ipmi.get_sensor_reading(sensor.number)
                            number = sensor.number
                            if value is not None:
                                # Convert value to sensor value
                                value = sensor.convert_sensor_raw_to_value(value)
                        except:
                            # Leave value as-is
                            pass 
                    elif sensor.type is pyipmi.sdr.SDR_TYPE_COMPACT_SENSOR_RECORD:
                        (value, states) = self.ipmi.get_sensor_reading(sensor.number)
                        number = sensor.number

                    if value is not None:
                        print("Adding sensor %d: %s = %s" % (number, sensor.device_id_string, value))
                        self.sensors[sensor_name] = { 'id': sensor.id, 'number': number, 'value': value }
                        count += 1

                except pyipmi.errors.CompletionCodeError as e:
                    if sensor.type in (pyipmi.sdr.SDR_TYPE_COMPACT_SENSOR_RECORD, pyipmi.sdr.SDR_TYPE_FULL_SENSOR_RECORD):
                        print("Error %s sensor %d: %s" % (e.cc, sensor.number, sensor.device_id_string))
                        self.sensors[sensor_name] = { 'id': sensor.id, 'number': sensor.number, 'error': e.cc}

        self.disconnect()

        return count

