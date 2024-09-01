# Table schema options are:
# Options are:
#   '<unique-item>',                          # A unique item from a specified table
#   '<zero-or-more-items>'                    # A list of zero or more items from a table
#   '<one-or-more-items>'                     # A list of one or more items from a table
#   '<one-of-items>'                          # A single table-entry name
#   [ '<zero-or-more>' 'item' 'item' ... ]    # Zero of more from a list of string items
#   [ '<one-or-more>' 'item' 'item' ... ]     # One of more from a list of string items
#   [ '<one-of>' 'item' 'item' ... ]          # One from a list of string items
#   '<str>'                                   # A generic string
#   '<bool>'                                  # A boolean item (value cell is True or False and display value is Yes or No)

CONFIGFILE = ".upscontrol"

# Thist part of the table is based on software details and is not editable by user action
DEFAULT_SYSTEM_CONFIG = {
    "version": 1,
    "global": {
        # Global configuration goes here
    },
    "available": [
        # List of available devices seen by scanner
    ],
    "devices": {
        # Editing schema infomration (format of each field)
        "schema": {
            "name": "<unique-item>",               # Name is a unique device name
            "type": [ "<one-of>", "APC", "OUTPUT" ],  # Output type
            "on-action": "<str>",
            "off-action": "<str>",
        },
        # Headers to display
        "headers": {
            'name': "Device Name",
            'type': "Device Type",
            'on-action': "Turn On",
            'off-action': "Turn Off",
        },
        # Default values when creating new entry
        "default": {
            'name': None,
            'type': None,
            'on-action': None,
            'off-action': None,
        },
        # Fields to show in record edit dialog
        "edit_fields": [
            'name',
            'type',
            'on-action',
            'off-action',
        ],
        # Fields to show in table view
        "table_fields": [
            'name',
            'type',
            'on-action',
            'off-action',
        ],
        'data': [
        ],
    },
    # Remaining items added by user config
}

# This is the 'nodes' table that is stored, retrieved and editable by user action.
DEFAULT_NODE_CONFIG = {
    "nodes": {
        "schema": {
            "name": "<unique-item>",                # name is a unique node name
            "icon": "<icon>",                       # Device icon
            "dns": "<str>",                         # dns is a string (but should be smarter)
            "uri": "<str>",                         # uri is a string (but should be smarter)
            "requires": "<zero-or-more-items>",     # requires is a list of <node names>
            "wants": "<zero-or-more-items>",        # wants is a list of <node names>
            "start": "<str>",                       # start is a string (action function)
            "stop": "<str>",                        # stop is a string (action function)
            "showmain": "<bool>",                   # main is a boolean (show on main page if True)
            "username": "<str>",                    # User name credential for access
            "password": "<password>",               # Password for credential    
            "autostart": "<bool>",                  # If to auto start when power is ready
        },
        # If displayed, use these strings to identify the value on screen
        "headers": {
            "name": "Name",
            "icon": "Icon",
            "dns": "Dns",
            "uri": "URI",
            "requires": "Requires",
            "wants": "Wants",
            "start": "Start Action",
            "stop": "Stop Action",
            "showmain": "On Main Page",
            "username": "User name",
            "password": "Password",
            "autostart": "Auto Start",
        },
        # Include these in the table shown for configuration, in order of display
        'table_fields': [
            'name',
            "uri",
            "requires",
            "wants",
            "showmain",
            "autostart",
        ],
        # Include these in the detailed edit dialog, in order of display
        'edit_fields': [
            'name',
            'icon',
            'dns',
            'uri',
            'requires',
            'wants',
            'start',
            'stop',
            'showmain',
            'username',
            'password',
            "autostart",
        ],
        # A default setting when creating a new entry
        'default': {
            "name": None,
            "icon": None,
            "dns": "",
            "uri": "",
            "requires": [],
            "wants": [],
            "start": "",
            "stop": "",
            "showmain": False,
            "username": "",
            "password": "",
            "autostart": False,
        },
        "data": [{
            "name": "System",
            "icon": None,
            "dns": "",
            "uri": "",
            "requires": [],
            "wants": [],
            "start": "",
            "stop": "",
            "showmain": True,
            "username": "",
            "password": "",
            "autostart": True,
        },{
            "name": "Nimbus",
            "icon": None,
            "dns": "nimbus.aerodesic.net",
            "uri": "APC1:1",
            "requires": ["Nas3"],
            "wants": ["Nas1", "Nas2"],
            "start": "apcstart",
            "stop": "apcstop",
            "showmain": True,
            "username": "",
            "password": "",
            "autostart": False,
        },{
            "name": "Cirrus",
            "icon": None,
            "dns": "cirrus.aerodesic.net",
            "uri": "APC1:2",
            "requires": ["Nas3"],
            "wants": ["Nas1", "Nas2"],
            "start": "apcstart",
            "stop": "apcstop",
            "showmain": True,
            "username": "",
            "password": "",
            "autostart": False,
        },{
            "name": "Cumulus",
            "icon": None,
            "dns": "cumulus.aerodesic.net",
            "uri": "APC1:3",
            "requires": ["Nas3"],
            "wants": [],
            "start": "apcstart",
            "stop": "apcstop",
            "showmain": True,
            "username": "",
            "password": "",
            "autostart": False,
        },{
            "name": "Nas1",
            "icon": None,
            "dns": "nas1.aerodesic.net",
            "uri": "APC1:4",
            "requires": ["Nas3"],
            "wants": [],
            "start": "apcstart",
            "stop": "apcstop",
            "showmain": False,
            "username": "",
            "password": "",
            "autostart": False,
        },{
            "name": "Nas2",
            "icon": None,
            "dns": "nimbus.aerodesic.net",
            "uri": "APC1:5",
            "requires": ["Nas3"],
            "wants": [],
            "start": "apcstart",
            "stop": "apcstop",
            "showmain": False,
            "username": "",
            "password": "",
            "autostart": False,
        },{
            "name": "Nas3",
            "icon": None,
            "dns": "nas3.aerodesic.net",
            "uri": "APC1:6",
            "requires": [],
            "wants": ["Gatekeeper"],
            "start": "apcstart",
            "stop": "apcstop",
            "showmain": False,
            "username": "",
            "password": "",
            "autostart": False,
        },{
            "name": "Gatekeeper",
            "icon": None,
            "dns": "gatekeeper.aerodesic.net",
            "uri": "APC1:7",
            "requires": [ "DmzSwitch", "NasSwitch" ],
            "wants": [],
            "start": "apcstart",
            "stop": "apcstop",
            "showmain": False,
            "username": "",
            "password": "",
            "autostart": False,
        },{
            "name": "DmzSwitch",
            "icon": None,
            "dns": "",
            "uri": "APC1:8",
            "requires": [],
            "wants": [],
            "start": "apcstart",
            "stop": "apcstop",
            "showmain": False,
            "username": "",
            "password": "",
            "autostart": False,
        },{
            "name": "NasSwitch",
            "icon": None,
            "dns": "",
            "uri": "APC2:1",
            "requires": [],
            "wants": [],
            "start": "apcstart",
            "stop": "apcstop",
            "showmain": False,
            "username": "",
            "password": "",
            "autostart": False,
        },{
            "name": "ApcSwitch1",
            "icon": None,
            "dns": "",
            "uri": "",
            "requires": [],
            "wants": [],
            "start": "",
            "stop": "",
            "showmain": False,
            "username": "",
            "password": "",
            "autostart": False,
        },{
            "name": "ApcSwitch2",
            "icon": None,
            "dns": "",
            "uri": "",
            "requires": [],
            "wants": [],
            "start": "",
            "stop": "",
            "showmain": False,
            "username": "",
            "password": "",
            "autostart": False,
        }],
    }
}
