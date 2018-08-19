import pyxel
import random
import time


class App:
    def __init__(self):
        pyxel.init(180, 120, caption="Pixelation")
        # pyxel.image(0).load(0, 0, '1.png')
        # Global variables
        self.elapsed_time = 0
        self.run = False

        # Variables for clouds
        self.cloud_x0 = 0 # Starting x coordinate for the cloud 0
        self.cloud_x1 = 0 # Starting x coordinate for the cloud 1
        self.cloud_x2 = 0 # Starting x coordinate for the cloud 2
        self.loop_1 = False # Do not use reset cloud
        self.loop_2 = False # Do not use reset cloud
        self.go_into_loop_1 = True # Check whether x coordinate is greated than the limit
        self.go_into_loop_2 = True # Check whether x coordinate is greated than the limit

        # Character stuff
        self.x = 0
        self.y = 0

        # Jump variables
        self.velocity = 0         # Increment velocity
        self.jump_height = 20     # Jump height
        self.is_jumping = False   # Variable declaration, for jumping
        self.jump_num = 0         # How many times did it jump?

        # Bullet variables
        self.bullet_x = 0
        self.bullet_y = 0
        self.is_shooting = False

        pyxel.run(self.update, self.draw)

    def update(self):
        start_time = time.time()
        if pyxel.btnp(pyxel.KEY_Q):
                pyxel.quit()
        elif pyxel.btn(pyxel.KEY_ENTER):
            self.run = True

        if self.run:
            # Clouds
            self.cloud_x0 = (self.cloud_x0 + 1.25) % pyxel.width
            self.cloud_x1 = (self.cloud_x1 + 1.25) % pyxel.width
            self.cloud_x2 = (self.cloud_x2 + 1.25) % pyxel.width

            self.bullet_y = (self.bullet_y + 3) % pyxel.width
            
            self.constraints() # Constraints

            # Character stuff
            if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
                self.x -= 1
            elif pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
                self.x += 1
            elif pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W):
                self.is_jumping = True
            elif pyxel.btn(pyxel.KEY_SPACE):
                self.is_shooting = True
                self.bullet_x = self.x
            elif pyxel.btnp(pyxel.KEY_Q):
                pyxel.quit()
            
            # Jump
            if self.is_jumping:
                self.jump()
            
            end_time = time.time()
            self.elapsed_time += end_time - start_time

    def draw(self):
        pyxel.cls(13)
        self.welcome()
        self.clouds()
        self.ground()
        self.hero()
        self.shoot()

    # Environment and elements functions starting here
    def welcome(self):
        if not self.run:
            pyxel.text(45, 50, "Welcome to Pixelation!", pyxel.frame_count % 16)

    def cloud(self, x):
        pyxel.circ(15 + x, 12, 5, 17)
        pyxel.circ(21 + x, 15, 5, 17)
        pyxel.circ(26 + x, 17, 5, 17)
        pyxel.circ(32 + x, 15, 5, 17)
        pyxel.circ(25 + x, 10, 5, 17)
        pyxel.circ(31 + x, 14, 5, 17)
        pyxel.circ(25 + x, 12, 5, 17)
        pyxel.circ(31 + x, 15, 5, 17)
        pyxel.circ(36 + x, 17, 5, 17)
        pyxel.circ(42 + x, 15, 5, 17)
        pyxel.circ(33 + x, 10, 5, 17)

        # Code below is not functional, should fix it
        # if self.elapsed_time >= 0.005: # Start shooting after 5 seconds
        self.cloud_shooting(x) # Enable rainy clouds

    def cloud_shooting(self, x):
        # Cloud shooting animations
        # Cycle 1 ~ Stage 1
        # Cloud 0
        pyxel.rect(20 + x/5, 20 + x, 20.05 + x/5, 22 + x, 2)
        pyxel.rect(30 + x/5, 20 + x, 30.05 + x/5, 22 + x, 2)
        pyxel.rect(40 + x/5, 20 + x, 40.05 + x/5, 22 + x, 2)
        # Cloud 4
        pyxel.rect(80 + x/5, 20 + x, 80.05 + x/5, 22 + x, 2)
        pyxel.rect(90 + x/5, 20 + x, 90.05 + x/5, 22 + x, 2)
        pyxel.rect(100 + x/5, 20 + x, 100.05 + x/5, 22 + x, 2)
        # Cloud
        pyxel.rect(140 + x/5, 20 + x, 140.05 + x/5, 22 + x, 2)
        pyxel.rect(150 + x/5, 20 + x, 150.05 + x/5, 22 + x, 2)
        pyxel.rect(160 + x/5, 20 + x, 160.05 + x/5, 22 + x, 2)

        # Cycle 2 ~ Stage 2
        # Cloud 0
        # pyxel.rect(20 - x/5, 20 + x, 20.25 - x/5, 20 + x, 12)
        # pyxel.rect(30 - x/5, 20 + x, 30.25 - x/5, 20 + x, 12)
        # pyxel.rect(40 - x/5, 20 + x, 40.25 - x/5, 20 + x, 12)
        # # Cloud 1
        # pyxel.rect(60 - x/5, 20 + x, 60.25 - x/5, 20 + x, 12)
        # pyxel.rect(70 - x/5, 20 + x, 70.25 - x/5, 20 + x, 12)
        # pyxel.rect(80 - x/5, 20 + x, 80.25 - x/5, 20 + x, 12)
        # # Cloud 2
        # pyxel.rect(100 - x/5, 20 + x, 100.25 - x/5, 20 + x, 12)
        # pyxel.rect(110 - x/5, 20 + x, 110.25 - x/5, 20 + x, 12)
        # pyxel.rect(120 - x/5, 20 + x, 120.25 - x/5, 20 + x, 12)

        # # Cycle 3 ~ Stage 3
        # # Cloud 0
        # pyxel.rect(20, 20 + x/5, 20.25, 20 + x/5, 12)
        # pyxel.rect(30, 20 + x/5, 30.25, 20 + x/5, 12)
        # pyxel.rect(40, 20 + x/5, 40.25, 20 + x/5, 12)
        # # Cloud 1
        # pyxel.rect(60, 20 + x/5, 60.25, 20 + x/5, 12)
        # pyxel.rect(70, 20 + x/5, 70.25, 20 + x/5, 12)
        # pyxel.rect(80, 20 + x/5, 80.25, 20 + x/5, 12)
        # # Cloud 2
        # pyxel.rect(100, 20 + x/5, 100.25, 20 + x/5, 12)
        # pyxel.rect(110, 20 + x/5, 110.25, 20 + x/5, 12)
        # pyxel.rect(120, 20 + x/5, 120.25, 20 + x/5, 12)

        # # Implement the collision (what happens? instanteneous death or -hp?)
        # WILL NEED A FOOR LOOP TO ITERATE THROUGH ALL THE BODY POINTS OF THE HERO
        # if [20.25 + x, 20 + x] == [10 + self.x, 90 + self.y]:
        #     pyxel.quit()

    def clouds(self):
        """
        Draw clouds on the screen
        """
        if self.go_into_loop_1:
            if self.cloud_x1 > 119:
                self.loop_1 = True
                self.cloud_x1 = 0
                self.go_into_loop_1 = False

        if self.go_into_loop_2:
            if self.cloud_x2 > 59:
                self.loop_2 = True
                self.cloud_x2 = 0
                self.go_into_loop_2 = False

        self.cloud(self.cloud_x0)
        
        if self.loop_1:
            self.cloud(self.cloud_x1) # reset
        else:
            self.cloud(self.cloud_x1 + 60)
        
        if self.loop_2:
            self.cloud(self.cloud_x2) # reset
        else:
            self.cloud(self.cloud_x2 + 120)

    def ground(self):
        """
        Draw the ground
        """
        pyxel.rect(0, 110, 180, 120, 2)
    

    # Hero functions starting here
    def hero(self):
        """
        Draw the hero
        """
        pyxel.circ(10 + self.x, 102 + self.y, 7, 7)         # Head

        pyxel.circ(8    + self.x, 99.5  + self.y, 0.25, 12)   # Left Eye  0
        pyxel.circ(8    + self.x, 100.5 + self.y, 0.25, 12)   # Left Eye  1
        pyxel.circ(8    + self.x, 101.5 + self.y, 0.25, 12)   # Left Eye  2

        pyxel.circ(12   + self.x, 99.5  + self.y, 0.25, 12)   # Right Eye 0
        pyxel.circ(12   + self.x, 100.5 + self.y, 0.25, 12)   # Right Eye 1
        pyxel.circ(12   + self.x, 101.5 + self.y, 0.25, 12)   # Right Eye 2

        pyxel.circ(6    + self.x, 103.5 + self.y, 0.25, 4)   # Smile Left
        pyxel.circ(7    + self.x, 104.5 + self.y, 0.25, 4)   # Smile Left
        pyxel.circ(8    + self.x, 105.5 + self.y, 0.25, 4)   # Smile Left
        pyxel.circ(11   + self.x, 105.5 + self.y, 0.25, 4)   # Smile Center
        pyxel.circ(10   + self.x, 105.5 + self.y, 0.25, 4)   # Smile Center
        pyxel.circ(8.5  + self.x, 105.5 + self.y, 0.25, 4)   # Smile Center
        pyxel.circ(13.5 + self.x, 103.5 + self.y, 0.25, 4)   # Smile Right
        pyxel.circ(12.5 + self.x, 104.5 + self.y, 0.25, 4)   # Smile Right
        pyxel.circ(11.5 + self.x, 105.5 + self.y, 0.25, 4)   # Smile Right

    def jump(self):
        """
        Jump implementation

        Note: We do not have accelerations
        on both axes since the jump is vertical
        that is the degree between the jump trajectory
        and the X axis is constant and equals π radians
        """
        self.jump_num += 1
        # Up
        if self.jump_num <= self.jump_height:
            self.velocity = 1.5
            self.y -= self.velocity
        # Down
        elif self.jump_num > self.jump_height:
            if self.y != 0:
                self.velocity = 1.5
                self.y += self.velocity
            else:
                self.is_jumping = False
                self.velocity = 0
                self.jump_num = 0

    def shoot(self):
        if self.is_shooting:
            if self.bullet_y == 177:
                self.is_shooting = False
            
            pyxel.rect(10 + self.bullet_x, 107 - self.bullet_y, 10 + self.bullet_x, 111 - self.bullet_y, 4)

    def constraints(self):
        """
        Making sure that everything
        is within the borders
        """
        if self.x + 10 > 180:
            self.x = 0
        elif self.x < 0:
            self.x = 170
        elif self.y + 82 > 120:
            self.y = 0


App()
