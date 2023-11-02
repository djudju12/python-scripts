from pynput import mouse
import sys
from pynput.keyboard import Listener, Key
from threading import Thread
from time import sleep

def collect_coords(coords):
    with mouse.Events() as events:
        for event in events:
            if isinstance(event, mouse.Events.Click) \
                and event.button == mouse.Button.left \
                and event.pressed:
                print(f"coords = {event.x, event.y} added to list")
                coords.append((event.x, event.y))    

def task(coords):
    # while escape is not pressed
    while True:
        for coord in coords:
            sleep(0.5)
            print(f"Moving mouse to {coord}")
        # mouse.Controller().position = coord

def main():
    print("""
    Start collecting coordinates by clicking on the screen.
    When you are done, press Ctrl+C to stop the collection of coordinates.
    The last coordinate you clicked will be ignored, so click in the terminal before Ctrl+C.
    """)
    coords = []
    try:
        collect_coords(coords)
    except KeyboardInterrupt:
        print("\nRemoving last coordinate")
        coords.pop()
        print("coords = ", coords)

    print("""
    Now the program will start to repeat the coordinates you clicked.
    If you want to stop, press ESC.
    """)

    # while escape is not pressed
    def on_press(key):
        if key == Key.esc:
            print("Stopping the program")
            sys.exit()
            return False

    with Listener(on_press=on_press) as listener:
        thread = Thread(target=lambda: task(coords))
        # thread.start()
        thread.start()
        listener.join()
        return False
        
    #     if kb.Controller().press(kb.Key.esc):
    #         break
        # for coord in coords:
        #     print(f"Moving mouse to {coord}")
        #     mouse.Controller().position = coord

if __name__ == '__main__':
    main()