from db import create_session,add_interface, get_interface, delete_interface_table_data, Interface
from parse_data import parse_interface_data
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c','--config_url', type=str, default='configClear_v2.json', help='location of the config file, default: configClear_v2.json')
    parser.add_argument('-u','--user', type=str, default='postgres', help='user connecting to the database, default: postgres')
    parser.add_argument('-pw','--password', type=str, default='', help='password for the user connecting to db, default: empty')
    parser.add_argument('-d','--db_name', type=str, default='frinx', help='name of the database, default: frinx')
    parser.add_argument('-s','--server_ip', type=str, default='localhost', help='ip for the server, default: localhost')
    parser.add_argument('-p','--port', type=int, default=5432, help='port for accessing the db, default 5432')
    return parser.parse_args()

def main(config_url, user, password, db_name, server_ip ,port):
    with create_session(user=user, password=password, db_name=db_name, ip=server_ip, port=port) as session, session.begin():
        # delete data from the table 
        delete_interface_table_data(session=session)
        for data in parse_interface_data(config_url=config_url):
            # link ethernet port with port channel
            if data.port_channel_id:
                port_channel_id = get_interface(session=session, name=str(f'Port-channel{data.port_channel_id}')).id
            else:
                port_channel_id = None

            add_interface(
                session=session,
                name=data.name,
                description=data.description,
                config=data.config,
                max_frame_size=data.max_frame_size,
                port_channel_id=port_channel_id
                )
        print(f'Successfuly added {session.query(Interface).count()} rows:')
        print([str(interface) for interface in session.query(Interface).all()])

if __name__ == '__main__':
    try:
        args = parse_arguments()
        main(
            config_url=args.config_url,
            user=args.user,
            password=args.password,
            db_name=args.db_name,
            server_ip=args.server_ip,
            port=args.port
        )
    except ValueError as e:
        print(e)
    # except Exception as e:
    #     print(e)