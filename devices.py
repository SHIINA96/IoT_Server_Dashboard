def Devices():
    devices = [
        {
            'id': 'LED',
            'pin': 12,
            'name': 'Light',
            'status':'ON',
            'location':'Living Room'
        },
        {
            'id': 'RELAY',
            'pin': 11,
            'name': 'Relay',
            'status':'OFF',
            'location':'Bed Room'
        },
        {
            'id': 'SERVO',
            'pin': 13,
            'name': 'Servo',
            'status':'on',
            'location':'Kitchen'
        }
    ]
    return devices
