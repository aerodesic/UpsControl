
#######################################################################################################
# Copyright 2019, CPAC Equipment, Inc.
# All rights reserved.
#######################################################################################################

#
# Simple wrapper class for DBUS activity (services and emitters)
#

import dbus
import dbus.service
import dbus.glib
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GObject as gobject

class DBusObject(dbus.service.Object):
    def __init__(self, busname, servicename, bus):
        self._busname = busname
        self._servicename = servicename
        self._bus = bus

    def _startup(self):
        pass

    def _shutdown(self):
        pass

    def _exception(self, e):
        pass

    def run(self):
        DBusGMainLoop(set_as_default=True)
        bus_name = dbus.service.BusName(self._busname, self._bus)
        dbus.service.Object.__init__(self, bus_name, self._servicename)

        self._startup()

        try:
            self._loop = gobject.MainLoop()
            self._loop.run()

        except Exception as e:
            self._exception(e)

        self._shutdown()

