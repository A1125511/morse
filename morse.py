import keyboard
import time
import json
import yaml
import threading

running = True
last_pressed_time = None
last_morse_time = None
decoded = ''
morse = []
char = []
string = []
convert_timer = None

with open("morse_dict.json", "r", encoding="utf-8") as f:
    morse_data = json.load(f)

with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

key = config["keyboard"]["key"]
exit = config["keyboard"]["exit_key"]
auto_convert_timeout = config["timing"]["auto_convert_timeout"]

morse2char = morse_data["morse2char"]

def morse_symbol(duration):
    return "─" if duration > 0.3 else "·"

def auto_convert_morse():
    global morse, char, last_morse_time, convert_timer

    if last_morse_time and time.time() - last_morse_time >= auto_convert_timeout:
        if morse:
            decoded = morse2char.get("".join(morse), "?")
            if decoded != "?":
                char.append(decoded)
            morse = []
            output = "".join(char) + "".join(morse)
            print("\r" + output + " " * 20, end='', flush=True)

    convert_timer = None

while running:
    try:
        event = keyboard.read_event(suppress=True)
        if event.event_type == keyboard.KEY_DOWN:
            inp = event.name
            match inp:
                case value if value == exit:
                    if morse:
                        print("\r", end='', flush=True)
                        for c in char:
                            print(f"{c}", end='', flush=True)
                        print(" " * 20, end='', flush=True)
                        
                    running = False
                    break

                case value if value == key:            
                    start_time = time.time()

                    if last_pressed_time is None:
                        interval = None
                    else:
                        interval = start_time - last_pressed_time
                        
                        if interval > 3:
                            char.append(' ')
                        elif interval > 1.5:
                            decoded = morse2char.get("".join(morse), "?")
                            if decoded != "?":
                                char.append(decoded)
                            morse = []
                            output = "".join(char) + "".join(morse)
                            print("\r" + output + " " * 20, end='', flush=True)

                    last_pressed_time = start_time

                    if convert_timer:
                        convert_timer.cancel()

                    while True:
                        release_event = keyboard.read_event(suppress=True)
                        if release_event.event_type == keyboard.KEY_UP and release_event.name == inp:
                            break

                    end_time = time.time()
                    duration = end_time - start_time

                    char_w = morse_symbol(duration)
                    
                    morse.append(char_w)
                    last_morse_time = time.time()
                    print("\r", end='', flush=True)
                    for c in char:
                        print(f"{c}", end='', flush=True)
                    print("".join(morse), end='', flush=True)
                    print(" " * 20, end='', flush=True)

                    convert_timer = threading.Timer(auto_convert_timeout,  auto_convert_morse)
                    convert_timer.daemon = True
                    convert_timer.start()
    
    except Exception as e:
        print(f"Error: {e}")
        running = False

print("\nProgram end")
