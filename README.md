# StarWarsDream
StarWar game
### **Introduction to the game：**

     This is a small game based on Python, the game name is called the plane war. The player through the keyboard arrow keys to control a plane to move, the screen has been the emergence of the enemy. Each destroyed a small plane was 1000 points, the elimination of a medium-sized aircraft was 6000 points, the eradication of a large aircraft was 10000 points, and with the score to improve the difficulty of upgrading. The game every 30S will have a random supply package, divided into full-screen bombs and double bullets. Full-screen bombs are initially three and have a maximum of three, double bullets duration of 20S. When the enemy is too much, you can press the space bar to use the full-screen bomb, the enemy will be all detonated. In the game, our plane can not collide with the enemy, otherwise it will lose a life, each game will have three lives, when the end of life after the end of the game.	
        
### **Module function：**

     Font: Fonts stored in the folder settings;
     Images: the game is stored inside the picture;
     sound：The folder is full of game music;
     Bullet.py: defines a bullet class that defines a model of ordinary bullets and super bullets;
     Enemy.py: defines the enemy type, including small enemy, medium enemy and boss machine three models and attributes such as the survival state, moving speed, hit the property and move rules, which speed is divided into high and low three speed;
     Myplane.py: the definition of their own aircraft class, the definition of the aircraft model and some properties such as survival, moving speed, invincible properties and moving rules;
     Supply.py: defines the supply package class, including double bullets and full-screen bomb package class;
     Main.py: is the main thread class, the class important to achieve the game to open the end of the function, the definition of the game difficulty settings, to achieve the collision detection function, the definition of the game control mode and other rules of the game;
     Record.txt: is responsible for recording the history of the highest record.

### **Little improvements to the game：**

    1. Medium-sized aircraft and the boss machine to increase the blood tank display, you can visually see the enemy to eliminate the progress.
    2. Our plane has three lives. Each time being crashed, reborn after three seconds invincible time.
