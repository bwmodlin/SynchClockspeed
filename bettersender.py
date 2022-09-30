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

def add_bit_stuffing(message, n):
    # n is the length of a repeating bit sequence before adding in a stuff bit
    answer = ""
    n_buffer = " "
    for bit in message:
        if bit != n_buffer[-1]:
            n_buffer = bit
            answer += bit
        else:
            n_buffer += bit
            answer += bit
            if len(n_buffer) == n:
                answer += str((1-int(n_buffer[-1])))
                n_buffer = " "
    return answer
            
def transmit_message(message):
    pi = pigpio.pi()
    sequence = wake + start + message + stop
    bit_stuffed_sequence = add_bit_stuffing(sequence, 5)
    send_sequence(pi, bit_stuffed_sequence)