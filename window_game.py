# Names: Sreekar Karra, Zayan Sikder, John Steele
# Period: 2
# Date Last Edited: 10/20/26

#Import configuration 
import pygame
import os
import sys
import queue
import time
import getpass
import builtins
import importlib.util
import contextlib
from threading import Thread

# Creates a terminal writer to type write strings into the terminal of Stage 2 game 
class TerminalWriter:
    def __init__(self, window, timeout:float = 0.004):
        self.window = window
        self.timeout = timeout
        self.buffer = ""

    # Writes lines into the terminal 
    def write(self, text):
        self.buffer += text
        while "\n" in self.buffer:
            line, self.buffer = self.buffer.split("\n", 1)
            self.window.type_write(line, self.timeout)
        return len(text)

    def flush(self):
        pass

# Creates new game class 
class WindowGame:
    def __init__(self):
        #Starts up pygame library and set various variables such as display, caption, color, font, etc
        pygame.init()
        pygame.key.set_repeat(400, 40)
        self.running = True
        self.hero_name = None
        self.color = (0,0,0)
        self.width = 500
        self.win = pygame.display.set_mode((500, 500))
        self.font = pygame.font.Font(size=16)
        #Creates fake terminal inside of the window 
        self.terminal_line = ""
        self.terminal = []
        self.prompt = ""
        self.hidden = False
        self.line = 0
        #Max rendered lines of the terminal 
        self.max_lines = 15
        self.submitted = queue.Queue()
        #Graphics 
        self.images = []
        self.image_index = 0
        #Loading in the graphics for the game 
        i = 0
        while True:
            i += 1
            try:
                self.images.append(pygame.transform.smoothscale(pygame.image.load(f"assets/room{i}.png"), (500, 250)))
            except FileNotFoundError:
                break
        self.input_enabled = False
        pygame.display.set_caption("The Labyrinth of Zayan II")

    #Make sure strings do not surpass the size of the terminal 
    def wrap(self, text):
        lines = []
        current = ""
        for word in text.split(" "):
            attempt = word if current == "" else current + " " + word
            if self.font.size(attempt)[0] >= self.width - 50 and current != "":
                lines.append(current)
                current = word
            else:
                current = attempt
        lines.append(current)
        return lines

    #Writes text so that there is a pause between each character 
    def type_write(self, string, timeout:float):
        if not self.running:
            return 
        for line in self.wrap(string):
            self.terminal.append("")
            for s in line:
                self.terminal[-1] += s
                time.sleep(timeout)
        self.line = len(self.terminal)

    #Instantly set text 
    def set_text(self, text):
        self.terminal = []
        self.line = 0
        if text != "":
            for line in text.split("\n"):
                self.terminal.extend(self.wrap(line))
        self.line = len(self.terminal)

    #Render different room graphic based on the room 
    def set_room(self, room_type, explored):
        if room_type == "Stairs":
            self.image_index = 2
        elif room_type == "Object":
            self.image_index = 3 if explored else 1
        else:
            self.image_index = 0
        self.image_index = min(self.image_index, len(self.images) - 1)

    #Reads the line of input from user 
    def read_line(self, prompt:str = "", hidden:bool = False):
        self.prompt = prompt
        self.hidden = hidden
        self.terminal_line = ""
        self.input_enabled = True
        text = self.submitted.get()
        self.input_enabled = False
        if text is None:
            raise EOFError
        shown = "*" * len(text) if hidden else text
        self.type_write(prompt + shown, 0)
        self.prompt = ""
        return text

    #Function for built in key event of pygame, registering keys and appending them to terminal 
    def on_key(self, event):
        if not self.input_enabled:
            return
        if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            text = self.terminal_line
            self.terminal_line = ""
            self.submitted.put(text)
        elif event.key == pygame.K_BACKSPACE:
            self.terminal_line = self.terminal_line[:-1]
        elif event.unicode.isprintable() and event.unicode != "":
            self.terminal_line += event.unicode

    #Gets login if wanted, plays game, end line. 
    def play(self):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-labyrinth-of-zayan.py")
        spec = importlib.util.spec_from_file_location("zayan", path)
        zayan = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(zayan)
        old_input = builtins.input
        old_getpass = getpass.getpass
        builtins.input = self.read_line
        getpass.getpass = lambda prompt="Password: ": self.read_line(prompt, True)
        #Utilizes the main game class, just renders text in the new display 
        try:
            with contextlib.redirect_stdout(TerminalWriter(self)):
                zayan.main(self, True, self.hero_name)
        except EOFError:
            pass
        finally:
            builtins.input = old_input
            getpass.getpass = old_getpass
        self.type_write("You may now close the window.", 0.004)

    # Main game loop: Blits text, images, handles pygame events, fills background, and clock. 
    def loop(self):
        clock = pygame.time.Clock()
        Thread(target=self.play, daemon=True).start()
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                    self.submitted.put(None)
                if event.type == pygame.KEYDOWN:
                    self.on_key(event)
            self.win.fill(self.color)
            if len(self.images) > 0:
                self.win.blit(self.images[self.image_index], (0,0))

            visible = list(self.terminal[-self.max_lines:])
            for i in range(len(visible)):
                surface = self.font.render(visible[i], False, (255, 255, 255))
                self.win.blit(surface, (25, 500 - 250 + (i*15)))

            if self.input_enabled:
                shown = "*" * len(self.terminal_line) if self.hidden else self.terminal_line
                surface = self.font.render(self.prompt + shown + "_", False, (255, 255, 255))
                self.win.blit(surface, (25, 500 - 250 + (len(visible) * 15)))
            pygame.display.flip()
            clock.tick(30)
        pygame.quit()


