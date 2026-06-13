import uvicorn
import webbrowser
import threading
import time
import socket

def wait_for_port(port, host="127.0.0.1", timeout=30):
    start_time = time.time()
    while True:
        try:
            with socket.create_connection((host, port), timeout=0.5):
                return True
        except (socket.timeout, ConnectionRefusedError, OSError):
            if time.time() - start_time > timeout:
                return False
            time.sleep(0.5)

def open_browser():
    # Wait until the port is open and listening
    wait_for_port(8000)
    # Give a tiny extra delay (e.g., 0.5s) to ensure the server is ready to handle requests
    time.sleep(0.5)
    # This will open the default browser, which is typically Edge on Windows
    webbrowser.open("http://localhost:8000")

if __name__ == "__main__":
    print("Starting Advanced AI Interview System...")
    # Start the browser open task in the background
    threading.Thread(target=open_browser, daemon=True).start()
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

