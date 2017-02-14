from apicem import *
from datetime import datetime
import json
import apicem_config

def get_resources(event, context):
    response = get(api="network-device")

    response_json = response.json()
    devices = response_json["response"]
    print list(format_resources(devices))
    return list(format_resources(devices))
def format_resources(resources):
     for resource in resources:
         try:
             yield format_resource(resource)
         except KeyError:
             continue

def format_resource(resource):
    
    #cisco api: fetch location data is very very slow...
    location_id = resource["location"]
    location_details = get_location_details(location_id)
    return {
        'base': {
            'name': resource["hostname"],
            'provider_created_at': datetime.utcnow().isoformat() + "Z",
            'native_portal_link': 'https://' + apicem_config.ip
        },
        'id': resource.get("managementIpAddress"),
        'type': 'appliance',
        'details': {
            'appliance': {
                "type_id": '1',
                "family" : resource["family"],
                "location": location_details
            }
        }
    }

def get_location_details(location_id):
    try:
   #     print location_id
   #     response = get(api="location/"+ location_id)
   #     response_json = response.json()
   #     data = response_json["response"]
   #     latitude, longitude =data["geographicalAddress"].split("/")
    
        return {
                "city": {
                      "latitude": '-8.233237111274553',
                      "longitude":'-57.30468749999999',
                      "name": 'dummy city'
                }
        }
    except:
        pass
