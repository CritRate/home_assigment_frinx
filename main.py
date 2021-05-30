from db import create_session,add_interface, get_interface, delete_interface_table_data, Interface
from parse_data import parse_interface_data

if __name__ == '__main__':
    try:
        with create_session() as session, session.begin():
                # delete data from the table 
                delete_interface_table_data(session=session)
                for data in parse_interface_data():
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
    except ValueError as e:
        print(e)
    except Exception as e:
        print(e)