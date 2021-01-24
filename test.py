request_string = 'get {}\n'.format('privet.ru')
class ClientError(Exception):
    pass
test_string1 = 'ok\npalm.cpukk 2.0 1150864255\npalm.cpu 0.5 1150864248\npalm.cpu 0.5 1150864250\neardrum.cpu 3.0 1150864250\n\n'
test_string2 = 'ok\npalm.cpu 2.0 1150864247\npalm.cpu 0.5 1150864248\n\n'
test_string3 = 'ok\npalm.cpu 10.5 1501864247\neardrum.cpu 15.3 1501864259\n\n'
test_string4 = 'error\n\n\n'
test_string5 = 'ok\npalm.\ee\cpu 10.5 1501864247\neadrum.cpu 15.3 1501864259\n\n'
def test(name):
    data_dict = dict()
    data_from_server = 'privet'
    if data_from_server.startswith('ok\n') and data_from_server.endswith('\n\n'):
        # формат,но без учета \n между
        n_count = data_from_server.count('\n') - 1
        server_answer = data_from_server[4:-2]  # те без ok\n ... \n\n те будет inf \n onf \n
        list_of_data = data_from_server.split('\n')  # ['ok', '...', '...', ..., '', '']
        if data_from_server == 'ok\n\n':
            data_dict.clear()
        elif data_from_server == 'ok\n\n\n':
            raise ClientError
        else:
            if len(list_of_data) == n_count + 2:
                if name == '*':
                    for string in list_of_data[1:-2]:
                        name_inf_time = string.split()
                        if len(name_inf_time) == 3:
                            if data_dict.get(name_inf_time[0]) == None:  # те не существуют значений по данному ключу
                                data_dict[name_inf_time[0]] = []
                            try:
                                data_dict[name_inf_time[0]].append((int(name_inf_time[2]), float(name_inf_time[1])))
                                # data_dict[name_inf_time][0].sort()
                            except ValueError:
                                raise ClientError
                        else:
                            raise ClientError
                        # data_dict[name_inf_time][0].sort()
                else:
                    for string in list_of_data:
                        if name in string:
                            inf_time = string.split()
                            if len(inf_time) == 3:
                                if inf_time[0] == name:
                                    if data_dict.get(name) == None:
                                        data_dict[name] = []
                                    try:
                                        data_dict[name].append((int(inf_time[2]), float(inf_time[1])))
                                    # data_dict[name].sort()
                                    except ValueError:
                                        raise ClientError
                            else:
                                raise ClientError
                            # data_dict[name].sort()
            else:
                raise ClientError
    else:
        raise ClientError
    for names in data_dict.keys():
        data_dict[names].sort()
    return data_dict

print('ok\npalm.cpu 2.0 1150864247\npalm.cpu 0.5 1150864248\neardrum.cpu 3.0 1150864250\n\n'[3:-2].split('\n')[0])