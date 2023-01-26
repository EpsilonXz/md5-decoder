import socket
import threading
import sys
import time
import pickle

#The actual number -> 3735928559 : Found in 647.2154 seconds

DISTANCE_PER_CPU = 1_000_000
FOUND = False

class MD5_Server():
    def __init__(self) -> None:
        self.SERVER_IP = '127.0.0.1'
        self.SERVER_PORT = 16720
        self.BUFF_SIZE = 1024
        self.STRING_LEN = 10
        self.STRING_TO_FIND = "EC9C0F7EDCC18A98B1F31853B1813301"
        self.sock = self.open_socket()
        self.list = self.build_mission_list()
        self.in_proccess = []
          
    def build_mission_list(self):        
        range_to_cover = 10 ** self.STRING_LEN
        repeat = range_to_cover // DISTANCE_PER_CPU
        list_of_mission = list()
        current_range = 0

        for i in range(repeat):
            list_of_mission.append(current_range)
            current_range += DISTANCE_PER_CPU

        return list_of_mission

    def open_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.SERVER_IP, self.SERVER_PORT))
        print("Server online!")

        return self.sock
    
    def get_client(self):
        self.sock.listen()

        self.client_sock, self.client_addr = self.sock.accept()

        return self.client_sock
    
    def send(self, msg, sock):
        sock.send(msg.encode())
    
    def recv(self, sock):
        data = sock.recv(self.BUFF_SIZE)

        return data.decode()
    
    def pickle_send(self, data, sock):
        p_data = pickle.dumps(data)
        sock.send(p_data)
    
    def pickle_recv(self, sock):
        p_data = sock.recv(self.BUFF_SIZE)
        data = pickle.loads(p_data)

        return data

    def calc_by_cpu(self):
        return DISTANCE_PER_CPU * self.CPU_AMOUNT

    def fill_by_len(self, current):
        return current.zfill(self.STRING_LEN)

    def make_to_send_list(self):
        to_send_list = list()

        for i in range(self.CPU_AMOUNT):
            to_send_list.append(self.list[0])
            self.in_proccess.append(to_send_list[i])
            self.list.pop(0)
        
        return to_send_list

    def with_client(self, sock):
        global FOUND

        self.CPU_AMOUNT = int(self.recv(sock))

        self.send(self.STRING_TO_FIND, sock)
        time.sleep(0.5)
        self.send(str(DISTANCE_PER_CPU), sock)

        to_send_list = self.make_to_send_list()
        
        time.sleep(0.5)
        
        self.pickle_send(to_send_list, sock)
        
        res = self.recv(sock)

        if res != "-1":
            print("Found the number!")
            print("The number is: " + res)
            FOUND = True
            sys.exit()
    
    def main(self):
        global FOUND 

        start = time.perf_counter()

        while not FOUND:
            print("Waiting for client!")
            sock = self.get_client()

            x = threading.Thread(target=self.with_client, args=(sock,))
            x.start()
        
        finished = time.perf_counter()
        print(f"finished searching in {finished - start:0.4f} seconds")       


if __name__ == "__main__":
    md_server = MD5_Server()
    md_server.main()
