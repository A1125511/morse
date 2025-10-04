import keyboard
import time

running = True
last_pressed_time = None
decoded = ''
morse = []
char = []
string = []

char2morse = {
    'A': '·─',    'B': '─···',  'C': '─·─·',
    'D': '─··',   'E': '·',     'F': '··─·',
    'G': '──·',   'H': '····',  'I': '··',
    'J': '·───',  'K': '─·─',   'L': '·─··',
    'M': '──',    'N': '─·',    'O': '───',
    'P': '·──·',  'Q': '──·─',  'R': '·─·',
    'S': '···',   'T': '─',     'U': '··─',
    'V': '···─',  'W': '·──',   'X': '─··─',
    'Y': '─·──',  'Z': '──··',}
morse2char = {v: k for k, v in char2morse.items()}

def morse_symbol(duration):
    return "─" if duration > 0.3 else "·"

while running:
    event = keyboard.read_event(suppress=True)
    if event.event_type == keyboard.KEY_DOWN:
        inp = event.name
        match inp:
            case 'esc':
                if morse:
                    decoded = morse2char.get("".join(morse), "?")
                    if not decoded == "?":
                        char.append(decoded)
                    print("\r", end='', flush=True)
                    output = "".join(char) + "".join(morse)
                    for c in char:
                        print(f"{c}", end='', flush=True)
                    print(" " * 20, end='', flush=True)
                    
                running = False
                break

            case 'space':            
                start_time = time.time()

                if last_pressed_time is None:
                    interval = None
                else:
                    interval = start_time - last_pressed_time
                    if interval > 3:
                        char.append(' ')
                    elif interval > 1.5:
                        decoded = morse2char.get("".join(morse), "?")
                        if decoded.isalpha():
                            char.append(decoded)
                        morse = []
                        output = "".join(char) + "".join(morse)
                        print("\r" + output + " " * 20, end='', flush=True)

                last_pressed_time = start_time

                while True:
                    release_event = keyboard.read_event(suppress=True)
                    if release_event.event_type == keyboard.KEY_UP and release_event.name == inp:
                        break

                end_time = time.time()
                duration = end_time - start_time

                char_w = morse_symbol(duration)
                
                morse.append(char_w)
                print("\r", end='', flush=True)
                for c in char:
                    print(f"{c}", end='', flush=True)
                print("".join(morse), end='', flush=True)
    

            
                
