import socket
import time


class ClientError(Exception):
    pass

class Client:

    def __init__(self, host, port, timeout = None):
        sock = socket.create_connection((host,port), timeout) # with socket.socket(...) as sock:
        self.socket = sock
    def __del__(self):
         self.socket.close()

    def put(self, name, number, timestamp = None):
        """Не возвращает ничего в случае успеха и ClientError в случае неуспешной отправки"""
        if timestamp == None:
            timestamp = int(time.time())
        request_string = 'put {} {} {}\n'.format(name, number, timestamp) # формат отправки данных
        self.socket.sendall(request_string.encode('utf8'))
        try:
            data_from_server = self.socket.recv(1024) # наша инфа с сервера
        except socket.error:
            raise ClientError
        if data_from_server.decode('utf8') == 'ok\n\n':
            return
        else:
            raise ClientError


    def get(self, name):
        request_string = 'get {}\n'.format(name) # эту строчку надо отправять на сервер
        self.socket.sendall(request_string.encode('utf8')) # отправляем
        data_dict = dict()

        try:
            data_from_server = self.socket.recv(1024).decode('utf8')
        except socket.error:
            raise ClientError
        if data_from_server.startswith('ok') and data_from_server.endswith('\n\n'):
            if data_from_server == 'ok\n\n':
                return {}
            n_count = data_from_server.count('\n')
            blocks = data_from_server[3:-2].split('\n') # делим по \n,которая разграничивает сообщения
            if len(blocks) == n_count - 2:
                if name == '*':
                    for data in blocks: # blocks содержат строчки типа 'key value time'
                        list_of_data = data.split()
                        if len(list_of_data) == 3:
                            if data_dict.get(list_of_data[0]) == None:
                                data_dict[list_of_data[0]] = []
                            try:
                                data_dict[list_of_data[0]].append((int(list_of_data[2]), float(list_of_data[1])))
                            except ValueError:
                                raise ClientError
                        else:
                            raise ClientError
                else:
                    for data in blocks:
                        list_of_data = data.split()
                        if len(list_of_data) == 3:
                            if list_of_data[0] == name:
                                if data_dict.get(name) == None:
                                    data_dict[name] = []
                            try:
                                data_dict[name].append((int(list_of_data[2]), float(list_of_data[1])))
                            except ValueError:
                                raise ClientError
                        else:
                            raise ClientError
            else:
                raise ClientError # кол-во разделяющих \n != кол-ву блоков сообщений
        else:
            raise ClientError
        for lists in data_dict.values():
            lists.sort()
        return data_dict
