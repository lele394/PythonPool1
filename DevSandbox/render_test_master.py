import time
import threading
from math import cos, sin, pi

# Import the App class from the appropriate file
from renderer_test import App

# You may need to import moderngl_window here as well if it's required in the App class
# import moderngl_window

def render_thread():
    app = App()
    app.run()

if __name__ == "__main__":
    app_thread = threading.Thread(target=render_thread, daemon=True)
    app_thread.start()

    deltat = 0.1
    theta = 0
    r = 5

    while True:
        x = r * cos(theta)
        y = r * sin(theta)

        theta += 0.1
        try:
            # Accessing app_thread.app assumes that the App instance has an "app" attribute
            # Update positions here if needed
            app_thread.app.update_positions(x, y)
        except:
            print("error on var change")

        time.sleep(0.01)
