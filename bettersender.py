import pigpio
import time

clockspeed = 0.01

GPIO_TRANSMITTER_NUMBER = 27
GPIO_RECEIVER_NUMBER = 26

start = "000111"
stop = "111000"
wake = "10"

def send_sequence(pi, message):
    for bit in message:
        pi.write(GPIO_TRANSMITTER_NUMBER, int(bit))
        time.sleep(clockspeed)

def transmit_message(message):
    pi = pigpio.pi()

    sequence = wake + start + message + stop

    send_sequence(pi, sequence)

