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
            'id': 'PUMP',
            'pin': 12,
            'name': 'Pump',
            'status':'OFF',
            'location':'Bed Room'
        },
        {
            'id': 'FAN',
            'pin': 4,
            'name': 'Fan',
            'status':'on',
            'location':'Kitchen'
        }
    ]
    return devices
