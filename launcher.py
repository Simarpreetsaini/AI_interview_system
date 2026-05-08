import uvicorn
import webbrowser
import threading
import time

def open_browser():
    time.sleep(5) # Wait 5 seconds to ensure the server is fully started
    # This will open the default browser, which is typically Edge on Windows
    webbrowser.open("http://localhost:8000")

if __name__ == "__main__":
    print("Starting Advanced AI Interview System...")
    # Start the browser open task in the background
    threading.Thread(target=open_browser, daemon=True).start()
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
