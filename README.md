# P I X E L A T I O N

This is a simple retro-style game where you have a hero which roams around
and tries to avoid getting hit by raging clouds. If you get hit by the cloud,
your score goes down by one. However, if you actually manage to hit the cloud
with the laser beam, you will get awarded one point. Be sure to time the laser
beam properly since there is a short delay before being able to reuse it again.

Note that everything in the game is built manually using pixels. Therefore,
every tiny particle has its own coordinates and could be manipulated directly.
This flexibility, however, comes with the price which is hard work for calculating
various measures of moving objects such as the width of cloud.

The game is implemented using retro-style game engine for Python called Pyxel.
For more information, see https://github.com/kitao/pyxel
