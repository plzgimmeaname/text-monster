import pygame
import os 
import sys 
from threading import Thread
import pynput
import time 
class WindowGame:
    def __init__(self):
        pygame.init()
        self.running = True
        self.color = (0,0,0)
        self.win = pygame.display.set_mode((500, 500))
        self.key_input = Thread(target=self.key_listener)
        self.key_input.start()
        self.font = pygame.font.Font(size=16)
        self.terminal_line = ""
        self.terminal = []
        
        self.line = 0
        self.images = [] 
        i = 0 
        while True:
            i += 1 
            try:
                self.images.append(pygame.transform.smoothscale(pygame.image.load(f"assets/room{i}.png"), (500, 250)))
            except FileNotFoundError:
                break
        self.input_enabled = True 
        pygame.display.set_caption("The Labyrinth of Zayan II")
    def on_press(self,key):
        self.type_write("Hi Sreekar, this is slow and dramatic text.", 0.2)
        self.type_write("Hi this is quick and easy", 0.045)
        if self.input_enabled:
            key = str(key)
            self.terminal_line += key.replace("'","")
    def on_release(self,key):
        pass
    def key_listener(self):
        with pynput.keyboard.Listener(on_press=self.on_press,on_release=self.on_release) as l:
            l.join()
    def type_write(self, string, timeout:float):
        for s in string:
            self.terminal_line += s 
            if self.font.size(self.terminal_line)[0] >= 500 - 50:
                self.terminal.append(self.terminal_line)
                self.terminal_line = ""
                self.line += 1 
            time.sleep(timeout)

    def set_text(self, text):
        self.terminal = []
        self.terminal_line = ""
        self.line = 0 
        metrics = self.font.metrics(text)
        current_width = 0 
        index = 0 
        old_index = 0 
        for i, letter in enumerate(metrics):
            current_width += letter[4]
            if current_width > self.width - 50:
                index = i 
                self.terminal.append(text[old_index:index])
                self.line += 1 
                old_index = index 
                current_width = 0
            else:
                index = i 
            if (index == len(metrics) - 1 and current_width != 0):
                self.terminal.append(text[old_index:index + 2])
                self.line += 1 

    def loop(self):
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    os.abort()
                    sys.exit(0)
                if event.type == pygame.KEYDOWN:
                    pass 
            self.win.fill(self.color)
            if self.font.size(self.terminal_line)[0] >= 500 - 50:
                self.terminal.append(self.terminal_line)
                self.terminal_line = ""
                self.line += 1 
            for i in range(len(self.terminal)):
                surface = self.font.render(self.terminal[i], False, (255, 255, 255))
                self.win.blit(surface, (25, 500 - 250 + (i*15)))

            self.win.blit(self.images[0], (0,0))

            surface = self.font.render(self.terminal_line, False, (255, 255, 255))
            self.win.blit(surface, (25, 500 - 250 +  (self.line * 15)))
            pygame.display.flip()

if __name__ == "__main__":
    game = WindowGame()
    game.loop()