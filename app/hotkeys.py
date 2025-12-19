from pynput import keyboard
import threading

def start_hotkeys(quit_cb, diagnose_cb, sleep_cb, wake_cb):
    def on_press(key):
        try:
            if key == keyboard.Key.f12:
                quit_cb()
            elif key == keyboard.Key.f9:
                diagnose_cb()
            elif key == keyboard.Key.f10:
                sleep_cb()
            elif key == keyboard.Key.f11:
                wake_cb()
        except:
            pass

    def listener():
        with keyboard.Listener(on_press=on_press) as l:
            l.join()

    thread = threading.Thread(target=listener, daemon=True)
    thread.start()

