from apicem import *
from datetime import datetime
import json
import apicem_config


def get_resources(event, context):
    response_appliance = get(api="network-device")
    response_appliance_json = response_appliance.json()  
    devices = response_appliance_json["response"]
    #print list(format_resources(devices))
    #print(json.dumps(devices, indent=4))

    response_flow = get(api="flow-analysis")
    response_flow_json = response_flow.json()
    flows = response_flow_json["response"]
    #print list(format_flows(flows))
    #print(json.dumps(flows, indent=4))

    results = []
    results.append(list(format_resources(devices)))
    results.append(list(format_flows(flows)))
    print "-------------results-------------"
    print (json.dumps(results, indent=4))
                   

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
    state = _map_status(resource["reachabilityStatus"])
    return {
        'base': {
            'name': resource["hostname"],
            'provider_created_at': datetime.utcnow().isoformat() + "Z",
            'native_portal_link': 'https://' + apicem_config.ip
        },
        'id': resource["id"],
        'type': 'appliance',
        'details': {
            'appliance': {
                "type_id": resource["type"],
                "family" : resource["family"],
                "location": location_details,
            }
        },
        'metadata': {
            "provider_specific": {
                "state": state,
            },
        }
    }

def _map_status(native_state):
    if native_state == 'Reachable':
        return 'Active'
    else:
        return 'Disabled'


def format_flows(flows):
    for flow in flows:
        try:
            yield format_flow(flow)
        except KeyError:
            continue

def format_flow(flow):
    flow_id = flow["id"]

    response_flow_details = get(api="flow-analysis" + "/" + flow_id)
    response_flow_details_json = response_flow_details.json()
    flow_details = response_flow_details_json["response"]

    return {
        'base': {
            'name': flow["id"],
            'provider_created_at': datetime.utcnow().isoformat() + "Z",
            'native_portal_link': 'https://' + apicem_config.ip
        },
        'id': flow["id"],
        'type': 'flow',
        'details': {
            'appliance': {
                "type_id": '',
                "family" : '',
                "location": '',
            }
        },
        'metadata': {
            "provider_specific": {
                "state": flow["status"],
                "sourceIP":flow["sourceIP"],
                "destIP":flow["destIP"],
                "detailedStatus":flow_details["detailedStatus"]["aclTraceCalculation"]
            },
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

