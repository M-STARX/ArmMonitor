import network
import socket
import time

# --- Configuration ---
SSID = 'ralph'   # The name of your Pi 4 Hotspot
PASSWORD = 'something'   # The password for your Pi 4 Hotspot
SERVER_IP = '10.42.0.1'           # Default NetworkManager Hotspot Gateway IP
SERVER_PORT = 19840

def connect_to_hotspot():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    print(f"Connecting to Pi 4 Hotspot: '{SSID}'...")
    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('Waiting for Wi-Fi connection...')
        time.sleep(1)

    if wlan.status() != 3:
        raise RuntimeError('Hotspot connection failed! Check SSID/Password.')
    else:
        print('Connected to Pi 4 Hotspot!')
        status = wlan.ifconfig()
        print(f'Pico IP assigned by Pi 4: {status[0]}')

def run_client():
    connect_to_hotspot()
    
    print(f"Attempting to connect to TCP Server at {SERVER_IP}:{SERVER_PORT}...")
    
    while True:
        try:
            # Create a TCP socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((socket.getaddrinfo(SERVER_IP, SERVER_PORT)[0][-1]))
            print("Successfully connected to the Pi 4 Server!")
            
            counter = 1
            while True:
                # Create a message and send it
                msg = f"Sensor reading #{counter}\n"
                print(f"Sending: {msg.strip()}")
                s.send(msg.encode('utf-8'))
                
                counter += 1
                time.sleep(2) # Send data every 2 seconds
                
        except Exception as e:
            print(f"Connection lost or failed: {e}")
            print("Retrying in 3 seconds...")
            s.close()
            time.sleep(3)

if __name__ == "__main__":
    run_client()