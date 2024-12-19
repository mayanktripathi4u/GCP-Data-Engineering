from google.cloud import healthcare_v1
import socket

# Configuration
PROJECT_ID = "your-gcp-project-id"
LOCATION = "your-region"
HL7V2_STORE = "hl7v2-store"
HL7_MESSAGE = "MSH|^~\\&|SendingApp|SendingFac|ReceivingApp|ReceivingFac|20241120120000||ADT^A01|123456|P|2.3\rPID|||123456^^^Hospital^MR||Doe^John||19700101|M|||123 Main St^^Anytown^CA^12345||555-555-5555||S||123-45-6789"

# MLLP Adapter Host and Port
MLLP_HOST = "mllp-adapter-service"  # Replace with your GKE service IP or domain
MLLP_PORT = 2575

def send_hl7_message():
    """Sends an HL7v2 message to the MLLP adapter"""
    try:
        with socket.create_connection((MLLP_HOST, MLLP_PORT)) as sock:
            sock.sendall(HL7_MESSAGE.encode("utf-8"))
            response = sock.recv(1024)
            print(f"Received response: {response.decode('utf-8')}")
    except Exception as e:
        print(f"Failed to send HL7 message: {e}")

if __name__ == "__main__":
    send_hl7_message()
