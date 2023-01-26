import socket
import sys
import concurrent.futures
import pickle
import time
from workers import Worker
import multiprocessing

from multiprocessing import Queue, Process

FOUND = False

class Client():
    def __init__(self) -> None:
        self.CPU_AMOUNT = sys.argv[1]
        self.PROCCESSES = self.CPU_AMOUNT
        self.SERVER_IP = '127.0.0.1'
        self.SERVER_PORT = 16720
        self.BUFF_SIZE = 1024
        self.set_socket()
    
    def set_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.SERVER_IP, self.SERVER_PORT))
    
    def send(self, msg):
        self.sock.send(msg.encode())
    
    def recv(self):
        data = self.sock.recv(self.BUFF_SIZE)

        return data.decode()
    
    def pickle_recv(self):
        p_data = self.sock.recv(self.BUFF_SIZE)
        data = pickle.loads(p_data)

        return data
    
    def start_worker(self, TO_FIND, range_given, dpc):
        worker = Worker(TO_FIND, range_given, dpc)
        res = worker.find_all()

        return res

    def with_server(self):
        self.send(self.CPU_AMOUNT)
        print("Sent!")

        self.STRING_TO_FIND = self.recv()
        self.DISTANCE_PER_CPU = int(self.recv())

        self.work_list = self.pickle_recv()

        proccess_amount = int(self.CPU_AMOUNT)
        
        self.proccesses = []

        start = time.perf_counter()

        #for i in range(proccess_amount):
        #    p = Process(target=self.start_worker, args=(self.STRING_TO_FIND, self.work_list[i], self.DISTANCE_PER_CPU))
        #    p.start()
        #    self.proccesses.append(p)

        final_res = -1

        with concurrent.futures.ProcessPoolExecutor() as executor:
            results = [executor.submit(self.start_worker, self.STRING_TO_FIND, self.work_list[i], self.DISTANCE_PER_CPU) for i in range(proccess_amount)]
        
        for f in concurrent.futures.as_completed(results):
            res = f.result()

            if res != -1:
                final_res = res
                break
        
        self.send(str(final_res))

        finished = time.perf_counter()
        print(f"finished searching in {finished - start:0.4f} seconds")
            

if __name__ == "__main__":
    multiprocessing.set_start_method('spawn')
    cli = Client()
    string = cli.with_server()
