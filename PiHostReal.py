## File to run at 2026 ACE competition

# type:ignore is how we ignore errors. You'll find it used to shut up the compiler 
# When type hints want imports we don't have access to (moteus, GPIO)

import asyncio
import moteus
import moteus_pi3hat # type: ignore
import time
import math
import RPi.GPIO as GPIO # type: ignore
import typing
from enum import Enum

### Our own imports
from exo_algorithm import Algorithm
from arm_monitor import ArmMonitorDummy
from alg_neutral import AlgNeutral
from alg_walk_forward import AlgWalkForward
from alg_testbench import AlgTest
from exoskeleton import Exoskeleton
import constants

# ==========================================
# 1. SHARED STATE
# ==========================================
shared_data = {
    "BATT": 100.0,
    "M1": 0.0,  # motor temperatures
    "M2": 0.0,
    "M3": 0.0,
    "M4": 0.0,
    "PICO_MODE": 1, 
    "PICO_HEIGHT": 69
}

# ==========================================
# 2. THE ASYNC BACKGROUND SERVER
# ==========================================
async def handle_pico_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"\n[SERVER] --- Connected by Pico at IP: {addr[0]} ---")
    
    # Concurrent task 1: Read incoming data and watch for timeouts
    async def read_loop():
        while True:
            try:
                # Wait for data, timeout after 5 seconds (The Heartbeat check!)
                data = await asyncio.wait_for(reader.read(1024), timeout=5.0)
                if not data:
                    print("[SERVER] Pico disconnected cleanly.")
                    break
                
                msg = data.decode('utf-8').strip()
                # print(f"[SERVER] Pico says: {msg}") # Uncomment for raw logs
                
                # Parse incoming UI commands
                if "Mode" in msg:
                    shared_data["PICO_MODE"] = int(msg.split()[1])
                    print(f"[SERVER] Mode changed to {shared_data['PICO_MODE']}")
                elif "Height" in msg:
                    shared_data["PICO_HEIGHT"] = int(msg.split(':')[1])
                    print(f"[SERVER] Height changed to {shared_data['PICO_HEIGHT']}")
                    
            except asyncio.TimeoutError:
                print("[SERVER] Pico timed out (Ghost Connection). Dropping.")
                break
            except Exception as e:
                print(f"[SERVER] Read error: {e}")
                break
        writer.close()

    # Concurrent task 2: Blast outgoing telemetry data
    async def write_loop():
        while not writer.is_closing():
            payload = f"BATT {shared_data['BATT']:.1f}\nM1 {shared_data['M1']:.1f}\nM2 {shared_data['M2']:.1f}\nM3 {shared_data['M3']:.1f}\nM4 {shared_data['M4']:.1f}\n"
            try:
                writer.write(payload.encode('utf-8'))
                await writer.drain() # Safely push data to network
            except Exception:
                break
            await asyncio.sleep(1.5) # Send every 1.5s
            
    # Run the read and write loops simultaneously for this client
    await asyncio.gather(read_loop(), write_loop(), return_exceptions=True)

async def run_tcp_server():
    # Start the server on port 19840
    server = await asyncio.start_server(handle_pico_client, '0.0.0.0', 19840)
    print(f"[SERVER] Listening on port 19840...")
    async with server:
        await server.serve_forever()

# ==========================================
# 3. EXOSKELETON LOGIC
# ==========================================
am = ArmMonitorDummy()

async def main():
    
    # FIRE AND FORGET THE SERVER
    # This runs the TCP server natively in the background of your asyncio event loop
    server_task = asyncio.create_task(run_tcp_server())

    # Define various system-level structures
    exo = Exoskeleton()
    # await exo.config()

    # Todo run init functions on algorithms
    
    # Begin the controlling loop:
    sexy = True
    try:
        while sexy:
            start_time = time.time()
            
            # --- TELEMETRY UPDATE ---
            # Update the shared dictionary with real exo data so the server can broadcast it
            # shared_data["BATT"] = exo.get_battery_voltage()
            # shared_data["M1"] = exo.get_motor_temp(1)
            
            algo : Algorithm = AlgNeutral()
            
            # We do this to find if our algorithm is a new algorithm
            new_alg = get_algo(am, exo)
            # await exo.set_algorithm(new_alg)
            
            # await exo.run_iteration()

            elapsed = time.time() - start_time
            # Maintain 50Hz update rate (20ms period)
            await asyncio.sleep(max(constants.PERIOD - elapsed, 0))
    except Exception as e:
        print(f'\nGoodnight, Ralph! Error: {e}')
        # await exo.teardown()
        
def get_algo(arm_monitor, exoskeleton : Exoskeleton) -> Algorithm:
    
    # Check if the Pico UI overrode the algorithm!
    if shared_data["PICO_MODE"] == 1:
        return AlgNeutral()
    elif shared_data["PICO_MODE"] == 2:
        return AlgWalkForward()
    elif shared_data["PICO_MODE"] == 3:
        return AlgTest()
    
    # Determine what algo we run
    if(arm_monitor.Get_Algorithm() is not AlgNeutral):
    # Run arm monitor's algorithm.
        algo_selected = arm_monitor.Get_Algorithm()
        return algo_selected
    else:
        pass
        # Arm monitor has nothing to say. 
        # Let's ask the exoskeleton how fast we're walking; 
        # If we don't meet the threshold, let's go into neutral.
    if (exoskeleton.get_pilot_speed() >= constants.MIN_WALK_ACTIVATION_SPEED):
        pass # return walk
    
    return AlgNeutral()

 
if __name__ == "__main__":
    asyncio.run(main())