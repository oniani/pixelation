import pyxel
import random
import time

"""
I should have the following classes: Element, Dog, and App
"""

class Element:
    def __init__(self):
        pyxel.init(240, 120, caption="Game Title", border_color=4)
        self.x = 0
        self.y = 50
        self.cloud_x = 0 # Starting x coorinate for the cloud

        ########################
        #######JUMP STUFF#######
        ########################
        self.dog_x = 0
        self.dog_y = 0
        self.velocity = 0
        self.acceleration = 0.25
        self.jump_height = 10
        self.is_jumping = False # Variable declaration, for jumping
        self.times = 0 # How many times did it jump?
        ########################
        ########################

        self.gravity = 9.80665 # gravity = pixel/second
        self.on_ground = True
        pyxel.run(self.update, self.draw)

    def update(self):
        self.cloud_x = (self.cloud_x + 1) % pyxel.width
        self.x = (self.x + 1.5) % pyxel.width

        # Character stuff
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
            self.dog_x -= 1
        elif pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
            self.dog_x += 1
        elif pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_W):
            self.is_jumping = True
        elif pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S):
            self.dog_y += 1
        elif pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        # Jump
        if self.is_jumping == True:
            self.jump()
        
        print(self.dog_y)

    def draw(self):
        pyxel.cls(0)
        self.welcome()
        self.cloud()
        self.ground()
        self.dog()
        pyxel.rect(self.x, self.y, self.x + 7, self.y + 5, 4)

    def welcome(self):
        pyxel.text(100, 150, "Welcome!", 7)

    def cloud(self):
        """
        Draw clouds on the screen
        """ 
        for i in range(5):
            pyxel.circ(0  + self.cloud_x + 50*i, 12, 5, 12)
            pyxel.circ(6  + self.cloud_x + 50*i, 15, 5, 12)
            pyxel.circ(11 + self.cloud_x + 50*i, 17, 5, 12)
            pyxel.circ(17 + self.cloud_x + 50*i, 15, 5, 12)
            pyxel.circ(10 + self.cloud_x + 50*i, 10, 5, 12)
            pyxel.circ(16 + self.cloud_x + 50*i, 14, 5, 12)
            pyxel.circ(10 + self.cloud_x + 50*i, 12, 5, 12)
            pyxel.circ(16 + self.cloud_x + 50*i, 15, 5, 12)
            pyxel.circ(21 + self.cloud_x + 50*i, 17, 5, 12)
            pyxel.circ(27 + self.cloud_x + 50*i, 15, 5, 12)
            pyxel.circ(18 + self.cloud_x + 50*i, 10, 5, 12)

    def ground(self):
        """
        Draw the ground
        """
        pyxel.rect(0, 100, 240, 120, 3)
    
    def dog(self):
        """
        Draw the doggo

        For implementing the jump, I'll probably need to do the for loop
        with big range to ensure all the pixels move along and eyes do not
        detect the movement
        """
        pyxel.circ(10 + self.dog_x, 93.5 + self.dog_y, 5, 12)

    def jump(self):
        # How many times did the update go through???
        self.times += 1
        # Smooth "go-up" implementation for the jump
        if self.times <= 20:
            self.velocity = 1
            self.dog_y -= self.velocity
            self.velocity += self.acceleration
        # Smooth "go-down" implementation for the jump
        elif self.times > 20:
            if self.dog_y != 0:
                self.velocity = 1 
                self.dog_y += self.velocity
                self.velocity += self.acceleration
            else:
                self.is_jumping = False
                self.velocity = 0
                self.times = 0


Element()
