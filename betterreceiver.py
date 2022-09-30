import pigpio
import time

clockspeed = 0.01

GPIO_TRANSMITTER_NUMBER = 27
GPIO_RECEIVER_NUMBER = 26

pi = pigpio.pi()

start = "000111"
stop = "111000"

state = "ready"

buffer = ""

message_buffer = ""

switch_time = None

def switch_callback(a, b, c):
    global switch_time
    switch_time = time.perf_counter()

pi.callback(GPIO_RECEIVER_NUMBER, pigpio.EITHER_EDGE, switch_callback)

while True:
    bit = str(pi.read(GPIO_RECEIVER_NUMBER))
    if state == "ready":
        if len(buffer) >= len(start):
            buffer = buffer[1:]

        buffer += bit

        if buffer == start:
            print("start received")
            buffer = ""
            state = "reading"

    elif state == "reading":
        message_buffer += bit

        if len(buffer) >= len(stop):
            buffer = buffer[1:]

        buffer += bit

        if buffer == stop:
            print("stop received")
            buffer = ""
            state = "ready"

            message_buffer = message_buffer[:-1 * len(stop)]
            print("received: " + message_buffer)

            message_buffer = ""

    if switch_time is None:
        time.sleep(clockspeed)
    else:
        difference = time.perf_counter() - switch_time
        if difference <= clockspeed:
            print("here")
            time.sleep(clockspeed + (clockspeed / 2 - difference))
            print(clockspeed + (clockspeed / 2 - difference))
        else:
            time.sleep(clockspeed)
