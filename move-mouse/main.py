from pynput.mouse import Controller, Button, Events
from pynput.keyboard import Listener, Key
from threading import Thread, Event
from time import sleep

def collect_coords(coords):
    with Events() as events:
        for event in events:
            if isinstance(event, Events.Click) \
                and event.button == Button.left \
                and event.pressed:
                print(f"coords = {event.x, event.y} added to list")
                coords.append((event.x, event.y))    

click_time = 0.5
def task(coords, event):
    # while escape is not pressed
    mouse = Controller()
    while True:
        for coord in coords:
            if event.is_set():
                return
            
            sleep(click_time)
            print(f"Moving mouse to {coord}")
            mouse.position = coord
            mouse.press(Button.left)
            mouse.release(Button.left)

def main():
    global click_time
    coords = []

    print("""
    Start collecting coordinates by clicking on the screen.
    When you are done, press Ctrl+C to stop the collection of coordinates.
    The last coordinate you clicked will be ignored, so click in the terminal before Ctrl+C.
    """)

    try:
        collect_coords(coords)
    except KeyboardInterrupt:
        print("\nRemoving last coordinate")
        if len(coords) <= 1:
            print("Provided no coords. Exiting...")
            return

        coords.pop()
        print("coords = ", coords)

    val = input(f"choose a time in seconds to wait between clicks. Default = {click_time}\n")
    try:
        val = float(val)
        click_time = val
    except Exception:
        pass

    print("""
    Now the program will start to repeat the coordinates you clicked.
    If you want to stop, press ESC.
    """)

    # while escape is not pressed
    event = Event()
    def on_press(key):
        if key == Key.esc:
            print("Stopping the program")
            event.set()
            return False

    thread = Thread(target=task, args=(coords, event))
    thread.start()
    
    with Listener(on_press=on_press) as listener:
        listener.join()
        return False
        
if __name__ == '__main__':
    main()