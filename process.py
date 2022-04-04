from datetime import datetime
import rpyc
from time import sleep
from random import randint
from threading import Thread

from state import STATE


class Process(Thread):
    def __init__(self, id):
        Thread.__init__(self)
        self.process_time_out = 5
        self.cs_time_out = 10
        self.time_stamp = datetime.now()
        self.state = STATE.DO_NOT_WANT
        self.id = id
        self.data = None

    def set_time_out(self, time_out):
        self.process_time_out = randint(5, time_out)

    def set_cs_time_out(self, time_out):
        self.cs_time_out = randint(10, time_out)

    def set_state(self, state):
        self.state = state
        self.time_stamp = datetime.now()

    def run(self):
        while True:
            if self.state == STATE.DO_NOT_WANT:
                sleep(self.process_time_out)
                self.set_state(STATE.WANTED)
                self.send_message()
            if self.state == STATE.WANTED:
                sleep(self.process_time_out)
                self.send_message()
            elif self.state == STATE.HELD:
                sleep(self.cs_time_out)
                self.set_state(STATE.DO_NOT_WANT)
                self.set_is_accessible(True)
                self.data = None

    def send_message(self):
        conn = self.get_conn()
        conn.root.ask_permission()

    def set_is_accessible(self, is_accessible):
        conn = self.get_conn()
        conn.root.set_is_accessible(is_accessible)

    def get_conn(self):
        return rpyc.connect("localhost", 23456)