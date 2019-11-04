# MAIC2018-Seega
MIFY Articificial Intelligence Contest 2018 

Source code for MIFY Articificial Intelligence Contest 2018 with finalists's AI code.




## The Game

The game chosen for this edition is Seega. It is played by 2 players on a board generally either 5 squares out of 5 or 7 squares out of 7. Each player has 12 pieces of different colors. The object of the game is to capture all the opposing 
pieces. More information on the rules of the game is available [here](http://www.lecomptoirdesjeux.com/seega.htm).

## Setup

The game was written in **Python** and works with versions greater than or equal to **3.6+**.

### Get Python and dependencies


You can download the **3.8** version of Python [here](https://www.python.org/downloads/).
(Don't forget to add python to the path if you are on Windows)

After the installation you need to install **PyQt5** the main dependence of the game.
For that just run the following command (Note that you may replace *pip* by *pip3* if you have different versions of python).


```bash
pip install pyqt5
```

### Run the code

Firstly, just clone this repository or download the zip to get everything you need to work and just run by following the instructions.


**Usage:**

      python ai_game_cli.py -ai0 ai_0.py -ai1 ai_1.py -s 0.5
      
      
      -ai0 
          path to the ai that will play as player 0
      -ai1 
           path to the ai that will play as player 1
      -s 
           time(in second) to show the board(or a move)


**Example:**
        
        git clone https://github.com/Machine-Intelligence-For-You/MAIC2018_Seega.git
        cd MAIC2018/
        python ai_game_cli.py -ai0 ai_0.py -ai1 ai_1.py -s 0.5
        


**Warning**

If the *python* command doesn't work you may try the *py* one.
        
         py ai_game_cli.py -ai0 ia0.py -ai1 ia1.py -s 0.5
        
		   
### Use timeout option 
The timeout option is the option that allows you to execute the play method of each AI for a specific time. Note that we
systematically use this option during matches and that it only works on Unix/Linux systems.

To run your AIs by imposing a time limit on them you will need to add the timeout decorator after importing it by specifying the time above the play function as follows:
            
            from util import timeout
            .
            .
            .
            @timeout(seconds = 0.1)
            def play(self, depth_to_cover, board, can_steal):


Now to run it you will have to use another file which is **ai_game_cli_timeout.py** with the same settings.

**Example:**
        
         python ai_game_cli_timeout.py -ai0 ai_0.py -ai1 ai_1.py -s 0.5
        
