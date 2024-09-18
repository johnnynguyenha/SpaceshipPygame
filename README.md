# SpaceshipPygame
## Summary
Spaceship Pygame is a game developed by Johnny Nguyen made using Pygame. Pygame is a Python library that helps developers create games. Spaceship Pygame is a simple game where the player moves a ship and fires lasers at incoming meteors. If the player gets hit by a meteor, the player dies and the game is over. If the player shoots a laser at a meteor and it hits, the meteor is destroyed. The score is tallied at the bottom of the screen.
![{E15032DA-8A2D-48D4-9035-E5981EC9729A}](https://github.com/user-attachments/assets/d5a9f865-89f7-4a75-a5c5-8dea1f2d5846)

## Elements
Spaceship Pygame showcases and utilizes various essential elements of game design.  
✓ Collisions  
✓ Music/Audio  
✓ Movement  
✓ Random Generation of Objects  
✓ Animation  
✓ Importing Sprites  
✓ Timers  
✓ Knowledge of Rects, Sprites, Image, Key Detection

## Notes
- Stars are randomly generated throughout the screen.
- Meteors are rotated at a random speed and spawn every 0.5 seconds at a random location near the top of the screen.
- Accurate hitboxes, not just rect but utilizing masks.
- Timers used to ensure spaceship cannot shoot too fast.
- Player cannot go off screen, objects (lasers, meteors) are deleted when they are off screen to enhance performance.
- FPS of the game does not affect movement.

## Controls
W - Move up  
A - Move down  
S - Move left  
D - Move right  
Spacebar - Shoot laser


## Running
To run, Python must be installed. In addition, Pygame-ce must be installed.   
Pygame can be installed via   
```
pip install pygame-ce
or   
pip3 install pygame-ce  
```
Afterwards, the game can be ran using 
```
python "main.py"
or
python3 "main.py"
```

