import json
from collections import namedtuple

interface_data = namedtuple('interface', ['name', 'description', 'config', 'max_frame_size', 'port_channel_id'])

# trailing coma in configClear_v2.json on line 1890 removed, json.load() was throwing error

def parse_interface_data(config_url):
    try:
        with open(config_url, 'r', encoding='utf-8') as file:
            frinx_data = json.load(file)
            # frinx-uniconfig-topology:configuration/Cisco-IOS-XE-native:native/interface/
            interfaces = frinx_data['frinx-uniconfig-topology:configuration']['Cisco-IOS-XE-native:native']['interface']
            # save port channels first to the database for ethernets port_channel_id
            for ports in interfaces['Port-channel']:
                yield interface_data(
                    name=f'Port-channel{ports.get("name")}',
                    description=ports.get('description'),
                    config=ports,
                    max_frame_size=ports.get('mtu'),
                    port_channel_id=None
                )
            # save everything else
            keys = interfaces.keys()
            for key in keys:
                # for now skip BDI and Loopback
                if key in ['TenGigabitEthernet', 'GigabitEthernet'] and key != 'Port-channel':
                    for interface in interfaces[key]:
                        yield interface_data(
                            name=f'{key}{interface.get("name")}',
                            description=interface.get('description'),
                            config=interface,
                            max_frame_size=interface.get('mtu'),
                            port_channel_id=interface.get('Cisco-IOS-XE-ethernet:channel-group', {}).get('number')
                        )
    except FileNotFoundError as e:
        print(e)
    except KeyError as e:
        print(f'Key missing from json file: {e}')
    except TypeError as e:
        print(f'Json file has wrong data type: {e}')
    except json.JSONDecodeError as e:
        print(f'Json Decode error: {e}')
            