import pyxel
import random
import time

"""
I should have the following classes: Element, Dog, and App
"""


class App:
    def __init__(self):
        pyxel.init(150, 120, caption="Pixelation")
        self.block_x = 0
        self.block_y = 50
        # Variables for clouds
        self.cloud_x0 = 0 # Starting x coordinate for the cloud 0
        self.cloud_x1 = 0 # Starting x coordinate for the cloud 1
        self.cloud_x2 = 0 # Starting x coordinate for the cloud 2
        self.loop_1 = False # Do not use reset cloud
        self.loop_2 = False # Do not use reset cloud
        self.go_into_loop1 = True # Check whether x coordinate is greated than the limit
        self.go_into_loop2 = True # Check whether x coordinate is greated than the limit
        # Character stuff
        self.x = 0
        self.y = 0
        ########################
        #######JUMP STUFF#######
        ########################
        self.velocity = 0
        self.acceleration = 0.25
        self.jump_height = 30 # Jump height
        self.is_jumping = False # Variable declaration, for jumping
        self.jump_num = 0 # How many times did it jump?
        ########################
        ########################

        ############################
        #######SHOOTING STUFF#######
        ############################
        self.is_shooting = False
        ############################
        ############################

        pyxel.run(self.update, self.draw)

    def update(self):
        # Clouds
        self.cloud_x0 = (self.cloud_x0 + 1.25) % pyxel.width
        self.cloud_x1 = (self.cloud_x1 + 1.25) % pyxel.width
        self.cloud_x2 = (self.cloud_x2 + 1.25) % pyxel.width

        self.block_x = (self.block_x + 1.5) % pyxel.width # Moving blocks
        
        self.constraints() # Constraints

        # Character stuff
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
            self.x -= 1
        elif pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
            self.x += 1
        elif pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W):
            self.is_jumping = True
        # elif pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S):
            # self.y += 1
        elif pyxel.btn(pyxel.KEY_SPACE):
            self.is_shooting = True
        elif pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        # Jump
        if self.is_jumping:
            self.jump()
        
        # print(self.x) # Print the horizontal coordinate every update
        # print(self.y) # Print the vertical coordinate every update

    def draw(self):
        pyxel.cls(0)
        self.welcome()
        self.clouds()
        self.ground()
        self.hero()
        pyxel.rect(self.block_x, self.block_y, self.block_x + 7, self.block_y + 5, 4)

    def welcome(self):
        pyxel.text(100, 150, "Welcome!", 7)

    def cloud(self, x):
        pyxel.circ(0  + x, 12, 5, 12)
        pyxel.circ(6  + x, 15, 5, 12)
        pyxel.circ(11 + x, 17, 5, 12)
        pyxel.circ(17 + x, 15, 5, 12)
        pyxel.circ(10 + x, 10, 5, 12)
        pyxel.circ(16 + x, 14, 5, 12)
        pyxel.circ(10 + x, 12, 5, 12)
        pyxel.circ(16 + x, 15, 5, 12)
        pyxel.circ(21 + x, 17, 5, 12)
        pyxel.circ(27 + x, 15, 5, 12)
        pyxel.circ(18 + x, 10, 5, 12)

    def clouds(self):
        """
        Draw clouds on the screen
        """
        if self.go_into_loop1:
            if self.cloud_x1 > 99:
                self.loop_1 = True
                self.cloud_x1 = 0
                self.go_into_loop1 = False

        if self.go_into_loop2:
            if self.cloud_x2 > 49:
                self.loop_2 = True
                self.cloud_x2 = 0
                self.go_into_loop2 = False

        self.cloud(self.cloud_x0)
        
        if self.loop_1:
            self.cloud(self.cloud_x1) # reset
        else:
            self.cloud(self.cloud_x1 + 50)
        
        if self.loop_2:
            self.cloud(self.cloud_x2) # reset
        else:
            self.cloud(self.cloud_x2 + 100)

    def ground(self):
        """
        Draw the ground
        """
        pyxel.rect(0, 100, 240, 120, 3)
    
    def hero(self):
        """
        Draw the hero

        For implementing the jump, I'll probably need to do the for loop
        with big range to ensure all the pixels move along and eyes do not
        detect the movement
        """
        pyxel.circ(10 + self.x, 82 + self.y, 3, 12)
        # pyxel.rect(11.5 + self.x, 82 + self.y, 13 + self.x, 83 + self.y, 12)

    def jump(self):
        """
        Jump implementation
        """
        self.jump_num += 1
        # Smooth "go-up" implementation for the jump
        if self.jump_num <= self.jump_height:
            self.velocity = 1
            self.y -= self.velocity
            self.velocity += self.acceleration
        # Smooth "go-down" implementation for the jump
        elif self.jump_num > self.jump_height:
            if self.y != 0:
                self.velocity = 1 
                self.y += self.velocity
                self.velocity += self.acceleration
            else:
                self.is_jumping = False
                self.velocity = 0
                self.jump_num = 0
    
    # def shoot(self):
    #     """
    #     Shoot bad guys LUL
    #     """
    #     self.is_shooting = True

    def constraints(self):
        """
        Making sure that everything
        is within the borders
        """
        if self.x + 10 > 240:
            self.x = 0
        elif self.y + 82 > 120:
            self.y = 0

App()
