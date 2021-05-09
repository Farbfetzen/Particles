A collection of particle effects.

![fire example](example_images/fire.png)

Requires Python 3 and Pygame 2. You can choose the effect by giving its name as the first argument.
If it is missing, the default one is used.
```
python particles.py fire
```
Available effects:
- default
- fire
- fireballs
- bounce
- portal


### Controls:
Action | Binding
--- | ---
Emit particles | Left mouse button
Pause/unpause | Space
Next system | N
Delete all particles | Delete
Show miscellaneous info | F1
Quit | Esc


### Command Line Arguments
- -w, --window-size \<width> \<height>: Specify the window width and height in pixels.
- -h, --help: Show a help message and exit.
