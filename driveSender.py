from sender import transmit_message


while True:
    message = input("What message would like to send?")
    transmit_message(message)