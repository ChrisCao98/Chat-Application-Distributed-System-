import multiprocessing
import socket
import os

class ServerProcess(multiprocessing.Process):
    def __init__(self, port, server_address, buff_size=1024):
        super().__init__()
        self.port = port
        self.server_address = server_address
        self.buffer_size = buff_size

    def run(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        try:
            server_socket.bind((self.server_address, self.port))
            print(f"Server running on PID {os.getpid()} at {self.server_address}:{self.port}")
            # 这里添加服务器的处理逻辑

        finally:
            server_socket.close()
class GroupMemberServer:
    def __init__(self, number_server=1, server_address='127.0.0.1',base_port=10000):
        self.server_processes = []
        self.number_server = number_server
        self.server_address = server_address
        self.base_port = base_port
    def start_servers(self):
        for i in range(self.number_server):
            port = self.base_port + i
            server_process = ServerProcess(port,self.server_address)
            self.server_processes.append(server_process)
            server_process.start()

        for server_process in self.server_processes:
            server_process.join()

    def stop_servers(self):
        for server_process in self.server_processes:
            server_process.terminate()
    def create_server(self):

        pass



#自定义多线程
class Server(multiprocessing.Process):
    def __init__(self, server_socket, received_data, client_address):
        super(Server, self).__init__()
        self.server_socket = server_socket
        self.received_data = received_data
        self.client_address = client_address

    def run(self):
        message = 'Hi ' + self.client_address[0] + ':' + str(self.client_address[1]) + '. This is server ' + str(
            os.getpid())
        self.server_socket.sendto(str.encode(message), self.client_address)
        print('Sent to client: ', message)


if __name__ == "__main__":
    num_servers = 2
    manager = GroupMemberServer(num_servers)
    manager.start_servers()
