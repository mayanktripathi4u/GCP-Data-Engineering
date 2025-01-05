import socket
from generate_hl7_message import create_hl7_message

def send_hl7_message_via_socket(hl7_message, host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(hl7_message.encode())
        response = s.recv(1024)
        print("Received response: ", response.decode())

# Define the MLLP server address and port
mllp_host = "localhost"
mllp_port = 2575

# Send the HL7 message
hl7_message = create_hl7_message()
send_hl7_message_via_socket(hl7_message, mllp_host, mllp_port)
