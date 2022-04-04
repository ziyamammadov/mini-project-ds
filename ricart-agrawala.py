import queue
import rpyc
import sys
from rpyc.utils.server import ThreadedServer
from threading import Thread

from process import Process
from state import STATE

processes = []
processees_queue = queue.Queue()
wanted_processes = []
supported_commands = ["list", "time-p", "time-cs", "exit"]
shared_resource = "The data that can be accessed only by one process at one time"


class RA(rpyc.Service):
    def __init__(self, n):
        self.is_accessible = True
        self.start_processes(n)

    def start_processes(self, n):
        for id in range(n):
            process = Process(id=id + 1)
            process.setDaemon(True)
            process.start()
            processes.append(process)
            print(f"Started process with {process.id}, state {process.state.value}")

    def exposed_ask_permission(self):
        wanted_processes = self.get_wanted_processes()
        [processees_queue.put(p) for p in wanted_processes]
        process = processees_queue.get()

        if self.is_accessible:
            process.state = STATE.HELD
            process.data = shared_resource
            self.is_accessible = False
        elif all(p.state is STATE.WANTED for p in processes):
            self.is_accessible = True

    def get_wanted_processes(self):
        for process in processes:
            if process.state == STATE.WANTED and process not in wanted_processes:
                wanted_processes.append(process)

        wanted_processes.sort(key=lambda p: p.time_stamp, reverse=False)
        return wanted_processes

    def exposed_set_is_accessible(self, is_accessible):
        self.is_accessible = is_accessible

    def run(self):
        if not processees_queue.empty():
            process = processees_queue.get()
            process.state = STATE.HELD


def run_server(server):
    server.start()


def list_processes():
    for process in processes:
        print(f"Process {process.id}, state {process.state.value}, time-out {process.process_time_out}")


def set_time_out(processing_time_out):
    print(f"Setting the time-out of {processing_time_out} to the processes")
    for process in processes:
        process.set_time_out(processing_time_out)

    p_queue = queue.Queue()
    while not processees_queue.empty():
        process = processees_queue.get()
        process.set_time_out(processing_time_out)
        p_queue.put(process)


def set_cs_timeout(cs_timeout):
    print(f"Setting the time-out of {cs_timeout} to the critical session")
    for process in processes:
        process.set_cs_time_out(cs_timeout)

    p_queue = queue.Queue()
    while not processees_queue.empty():
        process = processees_queue.get()
        process.set_cs_time_out(cs_timeout)
        p_queue.put(process)


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("USAGE: ricart-agrawala.py <number_of_processes>")
        sys.exit()

    number_of_processes = int(sys.argv[1])
    if number_of_processes < 1:
        print("Number of processes should be greater than 0")
        sys.exit()

    ts = ThreadedServer(RA(number_of_processes), port=23456)
    server_thread = Thread(target=run_server, args=(ts,), daemon=True)
    server_thread.start()

    while True:
        command = input("Input the command: ")
        if command == "list":
            list_processes()
        elif "time-p" in command:
            try:
                processing_time_out = int(command.split(" ")[1])
                if processing_time_out <= 5:
                    print("The value should be more than 5")
                else:
                    set_time_out(processing_time_out)
            except:
                print("Argument should be numeric. For example <time-p 10>")
        elif "time-cs" in command:
            try:
                cs_time_out = int(command.split(" ")[1])
                if cs_time_out <= 10:
                    print("The value should be more than 10")
                else:
                    set_cs_timeout(cs_time_out)
            except:
                print("Argument should be numeric. For example <time-cs 20>")
        elif command == "exit":
            print("Program exited")
            break
        else:
            print(f"Not supported command. Please use following commands {supported_commands}")