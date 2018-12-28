"""
David Oniani
Licensed under MIT

                            P I X E L A T I O N

This is a simple retro-style game where you have a hero which roams around
and tries to avoid getting hit by raging clouds. If you get hit by the cloud,
your score goes down, however, if you actually manage to hit the cloud
with the laser beam, you will get awarded with points. Be sure to time the laser
beam properly since there is a short delay before being able to reuse it again.

Note that everything in the game is built manually using pixels. Therefore,
every tiny particle has its own coordinates and could be manipulated directly.
This flexibility, however, comes with the price which is hard work for calculating
various measures of moving objects such as the width of cloud.

The game is implemented using retro-style game engine for Python called Pyxel.
For more information, see https://github.com/kitao/pyxel


TODO:
    1. Randomize the raindrops' behavior
    3. Consider using numpy for pixels, maybe?
"""


# Have to manually disable pylint for this project.
# Otherwise, get pylint(E1101) warning.

# pylint: disable-all


import pyxel
import time


class Pixelation:
    def __init__(self):
        pyxel.init(180, 120, caption="Pixelation")
        # Global environmental variables
        self.start_time = time.time()
        self.run = False

        # Variables for clouds
        self.cloud0_x = 0           # Starting x coordinate for the cloud 0
        self.cloud1_x = 0           # Starting x coordinate for the cloud 1
        self.cloud2_x = 0           # Starting x coordinate for the cloud 2

        self.loop_1 = False         # Do not use reset cloud
        self.loop_2 = False         # Do not use reset cloud

        self.go_into_loop_1 = True  # Check whether x coordinate is greated than the limit
        self.go_into_loop_2 = True  # Check whether x coordinate is greated than the limit

        self.cloud1_health = 0      # Health of the first cloud
        self.cloud2_health = 0      # Health of the second cloud
        self.cloud3_health = 0      # Health of the third cloud

        # Character stuff
        self.hero_x = 0
        self.hero_y = 0
        self.score  = 0

        # Jump variables
        self.velocity    = 0      # Increment velocity
        self.jump_height = 20     # Jump height
        self.is_jumping  = False  # Variable declaration, for jumping
        self.jump_num    = 0      # How many times did it jump?

        # Laser beam variables
        self.is_shooting      = False
        self.laser_beam_timer = 0

        pyxel.run(self.update, self.draw)

    def update(self):
        """
        Update the environment.
        """
        if pyxel.btnp(pyxel.KEY_Q):
                pyxel.quit()

        elif pyxel.btn(pyxel.KEY_ENTER):
            self.run = True

        if self.run:
            self.cloud0_x = (self.cloud0_x + 1.25) % pyxel.width  # Cloud 0
            self.cloud1_x = (self.cloud1_x + 1.25) % pyxel.width  # Cloud 1
            self.cloud2_x = (self.cloud2_x + 1.25) % pyxel.width  # Cloud 2

            self.constraints()  # Constraints

            # Character stuff
            if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
                self.hero_x -= 1

            elif pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
                self.hero_x += 1

            elif pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W):
                self.is_jumping = True

            elif pyxel.btnp(pyxel.KEY_SPACE):
                self.is_shooting = True

            elif pyxel.btnp(pyxel.KEY_Q):
                pyxel.quit()

    def draw(self):
        """
        Draw the environment.
        """
        pyxel.cls(13)

        self.welcome()
        self.clouds()
        self.ground()
        self.hero()
        self.jump()
        self.laser_beam()

        # Put the score in the upper-right corner
        s = 'SCORE {:>1}'.format(self.score)
        pyxel.text(4, 5, s, 1)
        pyxel.text(4, 4, s, 7)

    def welcome(self):
        """
        Welcome text.
        """
        if not self.run:
            pyxel.text(28, 50, "Welcome to P I X E L A T I O N!", pyxel.frame_count % 16)

    def cloud(self, x):
        """
        Cloud representation

        It spans from (15 + x - 5 / 2) to (42 + x + 5 / 2)

        In other words, the smallest x coordinate is 12.5 + x
        and the biggest one is 44.5 + x
        """
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

        # Start shooting after 3 seconds
        if time.time() - self.start_time >= 3:
            self.cloud_shooting(x)

    def cloud_shooting(self, x):
        """
        Cloud shooting animations.
        """
        pyxel.rect(20 + x / 5, 20 + x, 20.05 + x / 5, 22 + x, 2)
        pyxel.rect(30 + x / 5, 20 + x, 30.05 + x / 5, 22 + x, 2)
        pyxel.rect(40 + x / 5, 20 + x, 40.05 + x / 5, 22 + x, 2)

        pyxel.rect(80  + x / 5, 20 + x, 80.05  + x / 5, 22 + x, 2)
        pyxel.rect(90  + x / 5, 20 + x, 90.05  + x / 5, 22 + x, 2)
        pyxel.rect(100 + x / 5, 20 + x, 100.05 + x / 5, 22 + x, 2)

        pyxel.rect(140 + x / 5, 20 + x, 140.05 + x / 5, 22 + x, 2)
        pyxel.rect(150 + x / 5, 20 + x, 150.05 + x / 5, 22 + x, 2)
        pyxel.rect(160 + x / 5, 20 + x, 160.05 + x / 5, 22 + x, 2)

    def clouds(self):
        """
        Draw clouds on the screen
        """
        if self.go_into_loop_1:
            if self.cloud1_x > 119:
                self.loop_1 = True
                self.cloud1_x = 0
                self.go_into_loop_1 = False

        if self.go_into_loop_2:
            if self.cloud2_x > 59:
                self.loop_2 = True
                self.cloud2_x = 0
                self.go_into_loop_2 = False

        self.cloud(self.cloud0_x)

        if self.loop_1:
            self.cloud(self.cloud1_x)  # reset
        else:
            self.cloud(self.cloud1_x + 60)

        if self.loop_2:
            self.cloud(self.cloud2_x)  # reset
        else:
            self.cloud(self.cloud2_x + 120)

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
        pyxel.circ(10 + self.hero_x, 102 + self.hero_y, 7, 7)         # Head

        pyxel.circ(8 + self.hero_x, 99.5  + self.hero_y, 0.25, 12)    # Left Eye  0
        pyxel.circ(8 + self.hero_x, 100.5 + self.hero_y, 0.25, 12)    # Left Eye  1
        pyxel.circ(8 + self.hero_x, 101.5 + self.hero_y, 0.25, 12)    # Left Eye  2

        pyxel.circ(12 + self.hero_x, 99.5  + self.hero_y, 0.25, 12)   # Right Eye 0
        pyxel.circ(12 + self.hero_x, 100.5 + self.hero_y, 0.25, 12)   # Right Eye 1
        pyxel.circ(12 + self.hero_x, 101.5 + self.hero_y, 0.25, 12)   # Right Eye 2

        pyxel.circ(6 + self.hero_x, 103.5 + self.hero_y, 0.25, 4)     # Smile Left
        pyxel.circ(7 + self.hero_x, 104.5 + self.hero_y, 0.25, 4)     # Smile Left
        pyxel.circ(8 + self.hero_x, 105.5 + self.hero_y, 0.25, 4)     # Smile Left

        pyxel.circ(11   + self.hero_x, 105.5 + self.hero_y, 0.25, 4)  # Smile Center
        pyxel.circ(10   + self.hero_x, 105.5 + self.hero_y, 0.25, 4)  # Smile Center
        pyxel.circ(8.5  + self.hero_x, 105.5 + self.hero_y, 0.25, 4)  # Smile Center

        pyxel.circ(13.5 + self.hero_x, 103.5 + self.hero_y, 0.25, 4)  # Smile Right
        pyxel.circ(12.5 + self.hero_x, 104.5 + self.hero_y, 0.25, 4)  # Smile Right
        pyxel.circ(11.5 + self.hero_x, 105.5 + self.hero_y, 0.25, 4)  # Smile Right

    def jump(self):
        """
        Jump implementation
        """
        if self.is_jumping:
            self.jump_num += 1
            # Up
            if self.jump_num <= self.jump_height:
                self.velocity = 1.5
                self.hero_y -= self.velocity
            # Down
            elif self.jump_num > self.jump_height:
                if self.hero_y != 0:
                    self.velocity = 1.5
                    self.hero_y += self.velocity
                else:
                    self.is_jumping = False
                    self.velocity = 0
                    self.jump_num = 0

    def laser_beam(self):
        """
        NOTE: FREEZE THE ENVIRONMENT FOR TESTING!
        NOTE: Will have to account for annoying floating point errors.

        A code for the laser beam.

        +1 if hit the cloud!
        """
        if self.is_shooting:
            start = time.time()
            pyxel.rect(8 + self.hero_x, 95 + self.hero_y, 12 + self.hero_x, 0 + self.hero_y, 8)
            end = time.time()
            self.laser_beam_timer += end - start

            if self.laser_beam_timer > 0.0003:
                self.is_shooting = False
                self.laser_beam_timer = 0
            
            if self.detect_collision(8 + self.hero_x, 12 + self.hero_x, 12.5 + self.cloud0_x, self.cloud0_x + 44.5):
                self.score += 1
            
            if self.detect_collision(8 + self.hero_x, 12 + self.hero_x, 12.5 + self.cloud1_x, self.cloud1_x + 44.5):
                self.score += 1
            
            if self.detect_collision(8 + self.hero_x, 12 + self.hero_x, 12.5 + self.cloud2_x, self.cloud2_x + 44.5):
                self.score += 1

    def detect_collision(self, x_left_1, x_right_1, x_left_2, x_right_2):
        """
        Collision detection algorithm.

        There are three possible cases.

        I. Left side collision

             ------------------
         ____|_               |
        |    | |              |
        |    --|---------------
        |      |
        |      |
        |______|
            
            if x_left_1 < x_left_2 and x_right_1 >= x_left_2

        II. Right side collision

        ------------------
        |              __|___
        |             |  |   |
        ------------------   |
                      |      |
                      |      |
                      |______|


            if x_left_1 >= x_left_2 and x_right_1 > x_right_2

        III. Full collision

        ------------------
        |    ______      |
        |   |      |     |
        ------------------
            |      |
            |      |
            |______|


            if x_left_1 >= x_left_2 and x_right_1 <= x_right_2


        For the left and right side collision, we do not care about whether the
        object's right x coordinate is greater than that of the other object.

        NOTE: No need to worry about the height since the beam goes all the way up.
        NOTE: Modifications to the inequalities are needed not to mingle the cases.
            For instance, in the first case, if we do not impose the restriction
            x_right_1 <= x_right_2, we get the third case.
        """
        # Case I
        if x_left_1 < x_left_2 and (x_right_1 >= x_left_2 and x_right_1 <= x_right_2):
            return True 

        # Case II
        if (x_left_1 >= x_left_2 and x_left_1 <= x_right_2) and x_right_1 > x_right_2:
            return True

        # Case III
        if x_left_1 >= x_left_2 and x_right_1 <= x_right_2:
            return True
        
        return False

    def constraints(self):
        """
        Making sure that everything is within the borders.
        """
        if self.hero_x + 10 > 180:
            self.hero_x = 0

        elif self.hero_x < 0:
            self.hero_x = 170

        elif self.hero_y + 82 > 120:
            self.hero_y = 0


def main():
    Pixelation()


if __name__ == "__main__":
    main()
