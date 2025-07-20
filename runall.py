import subprocess
import time

server_scripts = [
    "root.py",
    "tld_edu.py",
    "tld_in.py",
    "auth_pes.py",
    "auth_mit.py",
    "auth_amazon.py",
    "auth_google.py",
    "local.py"
]

processes = []

try:
    for script in server_scripts:
        print(f"Starting {script}...")
        proc = subprocess.Popen(["python", script])
        processes.append(proc)
        time.sleep(0.5)  

    print("✅ All servers started. Press Ctrl+C to stop.")
    for proc in processes:
        proc.wait()

except KeyboardInterrupt:
    print("\n🛑 Shutting down all servers...")
    for proc in processes:
        proc.terminate()
