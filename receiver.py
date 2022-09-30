import pigpio
import time

CLOCKSPEED = 0.01

bitStuffRunLength = 5

switch_time = None

def switch_callback(a, b, c):
    global switch_time
    switch_time = time.perf_counter()

def listen(pi, GPIO_RECEIVER_NUMBER):
    start = "000111"

    stop = "111000"

    state = "readingStart"

    buffer = ""

    message_buffer = ""

    runValue = None

    runLength = 0

    while True:
        bit = str(pi.read(GPIO_RECEIVER_NUMBER))

        if (runLength > 5):
            runLength = 1
            runValue = bit
            continue

        runLength = (runLength + 1) if (bit == runValue) else 1

        runValue = bit

        if state == "readingStart":
            if len(buffer) >= len(start):
                buffer = buffer[1:]

            buffer += bit

            if buffer == start:
                buffer = ""
                state = "readingMessage"

        elif state == "readingMessage":
            message_buffer += bit

            if len(buffer) >= len(stop):
                buffer = buffer[1:]

            buffer += bit

            if buffer == stop:
                buffer = ""
                state = "readingStart"

                message_buffer = message_buffer[:-1 * len(stop)]
                print("received: " + message_buffer)

                message_buffer = ""

        if switch_time is None:
            time.sleep(CLOCKSPEED)
        else:
            difference = time.perf_counter() - switch_time
            if difference <= CLOCKSPEED:
                time.sleep(CLOCKSPEED + (CLOCKSPEED / 2 - difference))
                print(CLOCKSPEED + (CLOCKSPEED / 2 - difference))
            else:
                time.sleep(CLOCKSPEED)

def listenForData(port, dataStream, stream=False):
    GPIO_TRANSMITTER_NUMBER = 27 - (4 * (port - 1))

    GPIO_RECEIVER_NUMBER = 26 - (4 * (port - 1))

    pi = pigpio.pi()

    pi.callback(GPIO_RECEIVER_NUMBER, pigpio.EITHER_EDGE, switch_callback)

    listen(pi, GPIO_RECEIVER_NUMBER)