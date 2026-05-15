import threading
import socket
import select
import time
import random

# ==========================================
# 1. SHARED VARIABLES & THE LOCK
# ==========================================
# This dictionary holds the data both threads will use.
shared_data = {
    "BATT": 100.0,
    "M1": 0.0,
    "M2": 0.0,
    "M3": 0.0,
    "M4": 0.0,
    "PICO_MODE": 1, # pi pico mode is here
    "Height": 0 # you can use height too
}

# The lock prevents both threads from modifying the dictionary at the exact same time
data_lock = threading.Lock()

# ==========================================
# 2. THE BACKGROUND SERVER THREAD
# ==========================================
def run_tcp_server():
    HOST = '0.0.0.0'
    PORT = 19840
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"[SERVER] Listening on port {PORT}...")
        
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"\n[SERVER] --- Connected by Pico at IP: {addr[0]} ---")
                conn.setblocking(False)
                last_send_time = time.time()
                last_pico_seen_time = time.time()
                
                while True:
                    try:
                        # --- RECEIVE DATA FROM PICO ---
                        ready_to_read, _, _ = select.select([conn], [], [], 0.1)
                        if ready_to_read:
                            data = conn.recv(1024)
                            if not data:
                                print("[SERVER] Pico disconnected cleanly.")
                                break 
                            
                            msg = data.decode('utf-8').strip()
                            print(f"[SERVER] Pico says: {msg}")
                            
                            # Example: If the Pico sends "Mode 2", save it to shared_data!
                            if "Mode" in msg:
                                mode_num = int(msg.split()[1])
                                with data_lock:
                                    shared_data["PICO_MODE"] = mode_num
                            if "Height" in msg:
                                height = int(msg.split()[1])
                                with data_lock:
                                    shared_data["Height"] = height

                        # --- SEND DATA TO PICO ---
                        current_time = time.time()
                        
                        # ADJUST THIS VALUE TO AFFECT HOW OFTEN DATA IS SENT TO THE PICO
                        # in seconds 
                        if current_time - last_send_time > 10:
                            
                            # Safely read the latest variables from the main loop
                            with data_lock:
                                b = shared_data["BATT"]
                                m1 = shared_data["M1"]
                                m2 = shared_data["M2"]
                                m3 = shared_data["M3"]
                                m4 = shared_data["M4"]
                            
                            # Format and send the payload
                            payload = f"BATT {b}\nM1 {m1}\nM2 {m2}\nM3 {m3}\nM4 {m4}\n"
                            conn.sendall(payload.encode('utf-8'))
                            
                            last_send_time = current_time

                    except ConnectionResetError:
                        print("[SERVER] Connection forcibly reset by Pico.")
                        break
                    except Exception as e:
                        print(f"[SERVER] Unexpected Error: {e}")
                        break

# ==========================================
# 3. YOUR MAIN LOOP
# ==========================================
def main_task():
    while True:
        time.sleep(0.5) 
        
        # acquire the shared data lock
        with data_lock:
            shared_data["BATT"] = max(0.0, shared_data["BATT"] - 0.1)
            
            # Update motor temps based on the Mode the Pico selected!
            current_mode = shared_data["PICO_MODE"]
            if current_mode == 1:
                shared_data["M1"] = round(random.uniform(30.0, 35.0), 1)
            else:
                shared_data["M1"] = round(random.uniform(60.0, 80.0), 1) 
# ==========================================
# 4. START EVERYTHING
# ==========================================
if __name__ == "__main__":
    # daemon=True means if the main program crashes, the server cleanly dies with it.
    server_thread = threading.Thread(target=run_tcp_server, daemon=True)
    
    # start the hotspot server thread while doing the other stuff
    server_thread.start()

    try:
        main_task()
    except KeyboardInterrupt:
        print("\n[MAIN] Shutting down...")