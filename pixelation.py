"""
P I X E L A T I O N

David Oniani
Licensed under MIT

TODO:
    1. Randomize the raindrops' behavior
"""


# Have to manually disable pylint for this project.
# Otherwise, get pylint(E1101) warning.
# Below is the explanation of why it happens
# NOTE: pyxel initiates an object and binds its methods to the pyxel module.
#       You canont use these methods until the init function has been called.
#       This makes a nice API but unfortunately not so good for static analysis.

# pylint: disable-all


import pyxel
import time
import random


WINDOW_WIDTH  = 180
WINDOW_HEIGHT = 120

JUMP_HEIGHT = 20
RAIN_COEFF  = 0

HIT_SCORE = 1


class Pixelation:
    """The core class of the game."""
    def __init__(self) -> None:
        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT, caption="Pixelation")

        self.start_time = 0                 # Start time
        self.timer      = 0                 # Track the time
        self.run        = False             # The state of the game - have not started yet, running or over

        # Cloud variables
        self.cloud0_x = 0                   # Starting x coordinate for the cloud 0
        self.cloud1_x = 0                   # Starting x coordinate for the cloud 1
        self.cloud2_x = 0                   # Starting x coordinate for the cloud 2

        self.loop_1 = False                 # Do not use reset cloud
        self.loop_2 = False                 # Do not use reset cloud

        self.go_into_loop_1 = True          # Check whether x coordinate is greater than the limit
        self.go_into_loop_2 = True          # Check whether x coordinate is greater than the limit

        # Rain variables
        self.rain0_x = 0                    # Cloud 0 rain x coordinate
        self.rain1_x = 0                    # Cloud 1 rain x coordinate
        self.rain2_x = 0                    # Cloud 2 rain x coordinate

        self.rain_coeff = RAIN_COEFF        # Rain coefficient - the speed of precipitation

        # Character variables
        self.hero_x = 0                     # Current coordinate of the hero - X axis
        self.hero_y = 0                     # Current coordinate of the hero - Y axis
        self.score  = 0                     # Total score

        # Jump variables
        self.velocity    = 0                # Increment velocity
        self.jump_height = JUMP_HEIGHT      # Jump height
        self.is_jumping  = False            # Variable declaration, for jumping
        self.jump_num    = 0                # How many times did it jump?

        # Laser beam variables
        self.laser_is_shooting = False      # Are the clouds shooting?
        self.laser_beam_timer  = 0          # Laser beam time gap (reset time to be able to reuse it again)
        self.hit_score         = HIT_SCORE  # Increment in score when laser beam hits the cloud

        # Sound settings
        pyxel.sound(0).set(
            "e2e2c2g1 g1g1c2e2 d2d2d2g2 g2g2rr" "c2c2a1e1 e1e1a1c2 b1b1b1e2 e2e2rr",
            "p",
            "6",
            "vffn fnff vffs vfnn",
            25,
        )

        pyxel.sound(1).set(
            "r a1b1c2 b1b1c2d2 g2g2g2g2 c2c2d2e2" "f2f2f2e2 f2e2d2c2 d2d2d2d2 g2g2r r ",
            "s",
            "6",
            "nnff vfff vvvv vfff svff vfff vvvv svnn",
            25,
        )

        pyxel.sound(2).set(
            "c1g1c1g1 c1g1c1g1 b0g1b0g1 b0g1b0g1" "a0e1a0e1 a0e1a0e1 g0d1g0d1 g0d1g0d1",
            "t",
            "7",
            "n",
            25,
        )

        self.play_music()                   # Play the music

        pyxel.run(self.update, self.draw)   # Rn the environment

    def update(self) -> None:
        """Update the environment."""

        # Press the 'Q' key to quit the game
        if pyxel.btnp(pyxel.KEY_Q):
                pyxel.quit()
        
        # Press 'enter' to start the game
        elif pyxel.btn(pyxel.KEY_ENTER):
            self.run = True
            self.start_time = time.time()

        # If the player pressed 'enter', run the game
        if self.run:
            self.timer = round(time.time() - self.start_time, 1)  # Update time

            self.cloud0_x = (self.cloud0_x + 1.25) % pyxel.width  # Cloud 0
            self.cloud1_x = (self.cloud1_x + 1.25) % pyxel.width  # Cloud 1
            self.cloud2_x = (self.cloud2_x + 1.25) % pyxel.width  # Cloud 2

            self.rain0_x = (self.rain0_x + 1.75) % pyxel.width    # Cloud 0 laser
            self.rain1_x = (self.rain1_x + 1.75) % pyxel.width    # Cloud 1 laser
            self.rain2_x = (self.rain2_x + 1.75) % pyxel.width    # Cloud 2 laser

            # Press 'leftarrow' or 'A' key to move left
            if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
                self.hero_x -= 1

            # Press 'rightarrow' or 'D' key to move left
            elif pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
                self.hero_x += 1

            # Press 'uparrow' or 'W' key to move left
            elif pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W):
                self.is_jumping = True

            # Press 'SPACE' key to shoot the laser beam
            elif pyxel.btnp(pyxel.KEY_SPACE):
                self.laser_is_shooting = True

            # Press the 'Q' key to quit the game
            elif pyxel.btnp(pyxel.KEY_Q):
                pyxel.quit()

    def draw(self) -> None:
        """Draw the environment."""
        pyxel.cls(13)

        self.welcome()      # Welcome the player
        self.clouds()       # Draw the clouds

        if time.time() - self.start_time >= 3:
            self.rain()     # Enable rain 3 seconds after the 'enter' key is hit

        self.ground()       # Draw the ground
        self.hero()         # Draw the hero
        self.jump()         # Jump
        self.laser_beam()   # Laser beam activation
        self.game_over()    # Check if the game is over
        self.constraints()  # Impose constraints on the hero
        self.show_score()   # Draw the score
        self.show_timer()   # Show the elapsed time

    def welcome(self) -> None:
        """Welcome text."""
        if not self.run and self.score >= -100:
            pyxel.text(28, 50, "Welcome to P I X E L A T I O N!", pyxel.frame_count % 16)

    def show_score(self) -> None:
        """Put the score in the upper-right corner."""
        score = f"SCORE {self.score}"
        pyxel.text(4, 5, score, 1)
        pyxel.text(4, 4, score, 7)

    def show_timer(self) -> None:
        """Show the timer under the score."""
        timer = f"TIME {self.timer}"
        pyxel.text(4, 13, timer, 1)
        pyxel.text(4, 12, timer, 7)

    def cloud(self, x: float) -> None:
        """Representation of the cloud."""
        pyxel.circ(15 + x, 12, 5, 17)
        pyxel.circ(21 + x, 15, 5, 17)
        pyxel.circ(25 + x, 10, 5, 17)
        pyxel.circ(25 + x, 12, 5, 17)
        pyxel.circ(26 + x, 17, 5, 17)
        pyxel.circ(31 + x, 14, 5, 17)
        pyxel.circ(31 + x, 15, 5, 17)
        pyxel.circ(32 + x, 15, 5, 17)
        pyxel.circ(33 + x, 10, 5, 17)
        pyxel.circ(36 + x, 17, 5, 17)
        pyxel.circ(42 + x, 15, 5, 17)

    def clouds(self) -> None:
        """Draw the clouds on the screen."""
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
            self.cloud(self.cloud1_x)  # Reset
        else:
            self.cloud(self.cloud1_x + 60)

        if self.loop_2:
            self.cloud(self.cloud2_x)  # Reset
        else:
            self.cloud(self.cloud2_x + 120)

    def rain(self) -> None:
        """Shooting animations for the clouds."""
        # Cloud 0 rain
        for i in range(20, 41, 10):
            pyxel.rect(i + self.rain0_x / 5, 20 + self.rain0_x, i + self.rain0_x / 5 + 0.05, 22 + self.rain0_x, 2)

        # Cloud 1 rain
        for j in range(80, 101, 10):
            pyxel.rect(j + self.rain1_x / 5, 20 + self.rain1_x, j + self.rain1_x / 5 + 0.05, 22 + self.rain1_x, 2)

        # Cloud 2 rain
        for k in range(140, 151, 10):
            pyxel.rect(k + self.rain2_x / 5, 20 + self.rain2_x, k + self.rain2_x / 5 + 0.05, 22 + self.rain2_x, 2)

        # NOTE: The part below deals with the collision detection
        # NOTE: We first detect the collision on the x-axis and then proceed by imposing restrictions on y-axis

        cordinates_list = [ 20  + self.rain0_x / 5, 30  + self.rain0_x / 5, 40  + self.rain0_x / 5,
                            80  + self.rain1_x / 5, 90  + self.rain1_x / 5, 100 + self.rain1_x / 5,
                            140 + self.rain2_x / 5, 150 + self.rain2_x / 5, 160 + self.rain2_x / 5 ]

        for coordinate in cordinates_list:
            if self.detect_collision(coordinate, coordinate + 0.05, 5.875 + self.hero_x, 13.625 + self.hero_x):
                if self.detect_collision(20 + self.rain0_x / 5, 22 + self.rain0_x, 99.375 + self.hero_y, 105.625 + self.hero_y):
                    if self.run:
                        self.score -= 10 * self.hit_score  # Subtract tenfold

    def ground(self) -> None:
        """Draw the ground."""
        pyxel.rect(0, 110, 180, 120, 2)

    def hero(self) -> None:
        """Draw the hero."""
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

        pyxel.circ(11  + self.hero_x, 105.5 + self.hero_y, 0.25, 4)   # Smile Center
        pyxel.circ(10  + self.hero_x, 105.5 + self.hero_y, 0.25, 4)   # Smile Center
        pyxel.circ(8.5 + self.hero_x, 105.5 + self.hero_y, 0.25, 4)   # Smile Center

        pyxel.circ(13.5 + self.hero_x, 103.5 + self.hero_y, 0.25, 4)  # Smile Right
        pyxel.circ(12.5 + self.hero_x, 104.5 + self.hero_y, 0.25, 4)  # Smile Right
        pyxel.circ(11.5 + self.hero_x, 105.5 + self.hero_y, 0.25, 4)  # Smile Right

    def jump(self) -> None:
        """A simple jump implementation."""
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

    def laser_beam(self) -> None:
        """Laser beam functionalities."""
        if self.laser_is_shooting:
            start = time.time()
            pyxel.rect(8 + self.hero_x, 95 + self.hero_y, 12 + self.hero_x, 0 + self.hero_y, 8)
            end = time.time()
            self.laser_beam_timer += end - start

            if self.laser_beam_timer > 0.000075:
                self.laser_is_shooting = False
                self.laser_beam_timer = 0
            
            if self.detect_collision(8 + self.hero_x, 12 + self.hero_x, 12.5 + self.cloud0_x, self.cloud0_x + 44.5):
                self.score += self.hit_score
            
            if self.detect_collision(8 + self.hero_x, 12 + self.hero_x, 12.5 + self.cloud1_x, self.cloud1_x + 44.5):
                self.score += self.hit_score
            
            if self.detect_collision(8 + self.hero_x, 12 + self.hero_x, 12.5 + self.cloud2_x, self.cloud2_x + 44.5):
                self.score += self.hit_score

    def detect_collision(self, x_left_1: float, x_right_1: float, x_left_2: float, x_right_2: float) -> bool:
        """Collision detection algorithm.

        There are three possible cases.

        I. Left side collision

             +----------------+
        +----|-+              |
        |    | |              |
        |    +-|--------------+
        |      |
        |      |
        +------+
            
            if x_left_1 < x_left_2 and x_right_1 >= x_left_2

        II. Right side collision

        +----------------+
        |             +--|---+
        |             |  |   |
        +----------------+   |
                      |      |
                      |      |
                      +------+


            if x_left_1 >= x_left_2 and x_right_1 > x_right_2

        III. Full collision

        +----------------+
        |   +------+     |
        |   |      |     |
        +----------------+
            |      |
            |      |
            +------+


            if x_left_1 >= x_left_2 and x_right_1 <= x_right_2


        For the left and right side collision, we do not care about whether the
        object's right x coordinate is greater than that of the other object.

        NOTE: In case of laser beam, no need to worry about the height since it goes all the way up.

        NOTE: Modifications to the inequalities are needed not to mingle the cases.
            For instance, in the first case, if we do not impose the restriction
            x_right_1 <= x_right_2, we get the third case.

        NOTE: We could abstract out the third case, but it is better to have it
            this way since the former option will needlessly overcomplicate things.
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

    def constraints(self) -> None:
        """Making sure that everything is within the borders."""
        if self.hero_x + 10 > 180:
            self.hero_x = 0

        elif self.hero_x < 0:
            self.hero_x = 170

        elif self.hero_y + 82 > 120:
            self.hero_y = 0

    def play_music(self) -> None:
        """Background music for the game."""
        pyxel.play(0, [0, 1], loop=True)
        pyxel.play(1, [2, 3], loop=True)
        pyxel.play(2, 4, loop=True)

    def game_over(self) -> None:
        """If the score is below -100, shows the "GAME OVER" screen."""
        if self.score < -100:
            self.run = False
            pyxel.text(70, 40, "GAME OVER", pyxel.frame_count % 16)
            pyxel.text(45, 50, f"YOUR FINAL SCORE IS {round(self.score / self.timer)}", pyxel.frame_count % 16)


if __name__ == "__main__":
    Pixelation()
