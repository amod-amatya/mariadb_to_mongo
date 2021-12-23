sensor_input_components = ['Multi-Purpose Camera', 'Parking Assistance Module', 'Ultrasonic Sensor', 'Motion and Position Sensor',
                    'Mid-Range Radar Sensor', 'Near-Range Camera']
network_input_components = ['Telematics Unit', 'Telematics Unit:Bluetooth',
                            'Telematics Unit:Wifi', 'Telematics Unit:Cellular', 'Tire Pressure Measurement System' 'V2X']
OBD_input_component = ['Diagnostic Port']
input_components = sensor_input_components + network_input_components + OBD_input_component
output_components = ['VCU', 'V2X', 'Info Domain Computer', 'Body Computer Module']
output_components_VCU = ['Brake System', 'Electronic Engine Control',
                         'ESP Unit', 'Steering Control Unit', 'Navigation CU', 'Airbag CU']
environment1 = ['Hacker', 'Hacker: GNU Radio', 'Mechanic', 'Anonymous', 'Driver']
environment2 = ['Traffic Sign', 'Lenticulated Traffic Image', 'Manipulated Traffic Sign']
input_comp_dict = [{'name': name, 'type': 'sensor', 'child': [
    'DASy', 'CGU'], 'parent':None} for name in sensor_input_components]
network_input_comp_dict = [{'name': name, 'type': 'remote', 'child': [
    'CGU'], 'parent':None} for name in network_input_components]
component_OBD = [{'name': 'Diagnostic Port', 'type': 'OBD',
                  'child': ['CGU'], 'parent': None}]
component_CGU = [{'name': 'CGU', 'type': 'gateway',
                  'child': output_components, 'parent': network_input_components + ['DASy']}]
component_DASy = [{'name': 'DASy', 'type': 'mid_interface',
                   'child': ['CGU'], 'parent': sensor_input_components}]
output_comp_dict = [{'name': name, 'type': 'output', 'child': None if name != 'VCU' else output_components_VCU, 
                        'parent': ['CGU'],'output_level':0} for name in output_components]
output_comp_VCU_dict = [{'name': name, 'type': 'output', 'child': None, 'parent': [
                        'VCU'], 'output_level':1} for name in output_components_VCU]
component_dict = input_comp_dict + network_input_comp_dict + component_OBD + \
                    component_CGU + component_DASy + output_comp_dict + output_comp_VCU_dict

def add_components(component_collection):
    component_collection.delete_many({})
    component_collection.insert_many(component_dict)