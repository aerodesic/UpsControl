#
# UpsControl.py
#
# Main dbus based generator test control
#

import json


from gi.repository import GObject as gobject
import dbus
import dbus.service
import dbus.mainloop
import pyudev
from dbus.mainloop.glib import DBusGMainLoop
from threading import Thread, RLock, Lock, Timer
# import RPi.GPIO as GPIO
import time
from queue import Queue
import syslog
import logging
import os
import tempfile
from timeit import default_timer as elapsed_time

from UpsControlConfig import *
from UpsControlVartab import *

def syslog_json(name, value):
    prefix = "%s:  " % name

    for line in json.dumps(value, indent=3, sort_keys=True).split('\n'):
        syslog.syslog("%s%s" % (prefix, line))
        prefix = ""

#####################################
# Import a 'sync' function
try:
    # Try to use the one in the os module
    os_sync = os.sync
    # Test it
    os_sync()
    syslog.syslog("os_sync is os.sync()")

except:
    try:
        # Try to use the one in libc
        import ctypes
        os_sync = ctypes.CDLL("libc.so.6").sync
        # Test it
        os_sync()
        syslog.syslog("os_sync is libc.sync()")

    except:
        # If we don't find that, use a system() call
        os_sync = lambda: os.system("sync")
        syslog.syslog("os_sync is system('sync')")

_BUSNAME = "com.robosity.upscontrol.control"
_SERVICENAME = "/com/robosity/upscontrol/control"


class SimpleTimer():
    def __init__(self, time = 0):
        self._STOPPED = 0
        self._RUNNING = 1
        self._EXPIRED = 2
        if time == 0:
            self.stop()

        else:
            self.start(time)

    def start(self, value):
        self._state = self._RUNNING
        self._cycle = value
        self._target = elapsed_time() + value

    def expired(self):
        self._state = self._EXPIRED

    def stop(self):
        self._state = self._STOPPED

    def remaining(self):
        return self._target - elapsed_time() if self._state == self._RUNNING else 0

    def is_expired(self):
        if self._state == self._RUNNING and elapsed_time() >= self._target:
           self._state = self._EXPIRED

        return self._state == self._EXPIRED

    def is_running(self):
        return self._state != self._STOPPED and not self.is_expired()

    def is_stopped(self):
        return self._state == self._STOPPED

    def restart(self):
        if self._state == self._EXPIRED:
            self._target += self._cycle
            self._state = self._RUNNING

class UpsControlException(dbus.DBusException):
    def __init__(self, name, info):
        self._dbus_error_name = name
        self._info = info

class UpsControl(dbus.service.Object):
    def __init__(self):
        self.__dbus_lock = Lock()
        self.__config_lock = Lock()
        self.__config = VarTab()
        self.__activation_queue = Queue()

        # Put in the user portion of the config
        default_config = DEFAULT_NODE_CONFIG

        # Read current config file if available
        self.__config.Load(init=default_config)

        # Overwrite defaults for all of the items in the DEFAULT_SYSTEM_CONFIG
        for item in DEFAULT_SYSTEM_CONFIG:
            self.__config.SetValue(item, DEFAULT_SYSTEM_CONFIG[item])

    def __activation_thread(self):
        running = True

        while running:
            item = self.__activation_queue.get()
            if type(item) is dict:
                if 'activate' in item:
                    if item['activate']:
                        syslog.syslog("Activate %s" % item['device'])
                    else:
                        syslog.syslog("Deactivate %s" % item['device'])
            elif item is None:
                syslog.syslog("activation_thread stopping")
                running = False

    def run(self):

        # Create acivation thread
        self.__activation_thread_id = Thread(target=self.__activation_thread)
        self.__activation_thread_id.start()

        gobject.threads_init()
        dbus.mainloop.glib.threads_init()
        DBusGMainLoop(set_as_default=True)
        bus_name = dbus.service.BusName(_BUSNAME, dbus.SystemBus())
        dbus.service.Object.__init__(self, bus_name, _SERVICENAME)

        try:
            self._loop = gobject.MainLoop()
            syslog.syslog ("UpsControl service running...")
            self._loop.run()
            syslog.syslog ("UpsControl Service stopping...")

        except UpsControlException as e:
            syslog.syslog ("Signal %s caught" % e)

        except KeyboardInterrupt as e:
            syslog.syslog ("Keyboard interrupt")

        except Exception as e:
            syslog.syslog ("General exception '%s'" % e)

        except:
            syslog.syslog ("random exception")

        finally:
            syslog.syslog("leaving main loop")

        syslog.syslog ("UpsControl Service stopped")

        # shutdown activation thread
        self.__activation_queue.put(None)
        self.__activation_thread_id.join()

    def SendIndicateData(self, reason, data=None):
        self.IndicateData(reason, json.dumps(data))

    # Data as json string
    @dbus.service.signal(_BUSNAME, signature='ss')
    def IndicateData(self, reason, data=None):
        pass

    # Activates a device and all dependencies
    @dbus.service.method(_BUSNAME, in_signature='s')
    def Activate(self, device):
        self.__activation_queue.put({'device': device, 'activate': True})

    # Deactivates a device and all dependencies
    @dbus.service.method(_BUSNAME, in_signature='s')
    def Activate(self, device):
        self.__activation_queue.put({'device': device, 'activate': False})

    # Send value as dbus 'value'
    @dbus.service.method(_BUSNAME, in_signature='ss')
    def SetValue(self, name, value):
        with self.__config_lock:
            self.__config.SetValue(name, json.loads(value))

        # Debug
        # self.SendIndicateData("info", "value of '%s' set to %s" % (name, value))

    # Receive data as dbus 'value'
    # If name is blank, retrieve all of the config
    @dbus.service.method(_BUSNAME, in_signature='s', out_signature='s')
    def GetValue(self, name):
        with self.__config_lock:
            return json.dumps(self.__config.GetValue(name))

    # Set full config
    @dbus.service.method(_BUSNAME, in_signature='s')
    def SetConfig(self, config):
        with self.__config_lock:
            self.__config.SetAllValus(json.loads(config))

    # Get full config
    @dbus.service.method(_BUSNAME, in_signature='', out_signature='s')
    def GetConfig(self):
        with self.__config_lock:
            return json.dumps(self.__config.GetAllValues())
