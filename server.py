import network
import socket
import time

# --- AP Configuration ---
SSID = 'Arm_Monitor'           # The name of your Pico's Wi-Fi network
PASSWORD = 'something' # Must be at least 8 characters
PORT = 19840

def server():
    # start the access point
    ap = network.WLAN(network.AP_IF)
    ap.config(ssid=SSID, password=PASSWORD)
    ap.active(True)

    print(f"Starting Access Point with SSID: '{SSID}'")
    
    # wait for it to become active
    while not ap.active():
        time.sleep(0.5)
        
    # access ip address of pi pico
    ip = ap.ifconfig()[0]
    print(f"Pico IP Address is: {ip}, AP started")
    print("waiting")

    # start the TCP Server and socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    
    # bind to the port 
    s.bind((ip, PORT))  
    s.listen(2) # listen for one connection
    print(f"TCP Server listening on {ip}:{PORT}...")
    
    while True:
        try:
            conn, addr = s.accept()
            print(f"\n{addr} Device connected!")
            
            while True:
                # receive data from pi 4
                data = conn.recv(1024)
                if not data:
                    print("Connection closed by client.")
                    break
                
                print(f"Received from Pi 4: {data.decode('utf-8')}")
                
                conn.send("From the pico\n".encode('utf-8'))
                
        # on error, wait
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    server()