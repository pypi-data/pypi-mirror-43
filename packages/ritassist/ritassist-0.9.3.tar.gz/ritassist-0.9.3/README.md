# RitAssist API Access

Simple API class to get access to RitAssist and FleetGO API's

## Authentication
To use this component, you need an **API key** and **API secret**, which can be requested by contacting [info@fleetgo.com](mailto:info@fleetgo.com?subject=API%20Key).

## Example
```
from ritassist import API
import requests

api = API('Client ID', 'Client Secret', 'Username', 'Password')

if api.login():
    try:
        # This fetches the devices in the supplied account.
        devices = api.get_devices()
        
        for device in devices:
            print(f"{device.license_plate}: {device._make} {device._model}: {device._odo}")

            # Query Open Street Map for current maximum speed and current address
            device.get_map_details()

            # Gets the trips for the device, between 2018-06-04 and 2018-06-07
            trips = device.get_trips(a.authentication_info, "2018-06-04", "2018-06-07")

            for trip in trips:
                print(trip)

    except requests.exceptions.ConnectionError:
        print('Error connecting to API')
else:
    print('authetication failed')

```


## Versions
### 0.9.2
- Get country with the address

### 0.9
- Resolve maximum speed and current address using Open Street Map

### 0.8
- Several bug fixes

### 0.7
- Version 0.7 adds access to the trips for a device

### 0.6
- Bug fixes and code cleanup

### 0.5
- Access to devices and their properties
