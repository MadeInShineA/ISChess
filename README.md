
![p](https://github.com/LouisMLettry/ISChess/assets/114392644/e996f958-ccf3-4e72-ae8d-d2748ab24cae)
![n](https://github.com/LouisMLettry/ISChess/assets/114392644/25fc2ba7-d69d-4f63-8910-2205226ab65f)
![b](https://github.com/LouisMLettry/ISChess/assets/114392644/d6a80f82-8b3e-445a-818e-3ecec2d02217)
![r](https://github.com/LouisMLettry/ISChess/assets/114392644/f765a7ec-44bc-41b6-b2db-a0183ea67c6e)
![q](https://github.com/LouisMLettry/ISChess/assets/114392644/70e75741-8b8d-43f4-a08f-8ff7326005d4)
![k](https://github.com/LouisMLettry/ISChess/assets/114392644/1c20c806-fe70-4f7a-be0b-a32725c57400)

# ISChess
This is the repository containing the GUI supporting the ISChess project of the algorithmic lecture.

The project aim is to program a chess playing bot by adding a new file in the *Bots/* folder and registering it to the global bot list as shown in *BaseChessBot.py*. This file will produce your final handout.
You are more than welcome to modify these files, be careful that the final evaluation will be using the version of the software presented on this repository. If you would like to share modifications to improve the GUI, don't hesitate to submit a change request.

# Structure
- *Data/* folder: neutral assets location 
   - *maps/* folder: examplar boards which can be loaded
   - *assets/* folder: location of needed images and other assets
   - ui.ui file: GUI file from QtDesigner
- *Bots/* folder: contain the global list of bots (*ChessBotList.py*) as well as as an examplar pawn moving bot (*BaseChessBot.py*)
- main.py: Main execution point
- ParallelPlayer.py: Threaded wrapper for bot execution
- ChessRules.py: Basic custom chess rules and verification
- ChessArena.py: Actual GUI 

# Libraries
This software requires python 3.12+ together with two libraries:
- Numpy
- PyQt6

![ISC Logo inline (preferred)](https://github.com/LouisMLettry/ISChess/assets/114392644/799c6157-3088-4b0b-be09-ac805a2bd024)
