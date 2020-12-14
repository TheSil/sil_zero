# SilZero 

Experimenting with AI ideas...

TODO in chess backend: 
 - threefold repetition

TODO in AI:
 - propagate training data from self-play
 - connect to actual neural network
 - propagate actual values from terminal positions during mcts search?
 - add exploration noise

To play with the repository, you just need to have Python 3 installed. Download this repository and go to its root folder. 

Install python pre-requisities:

`python -m pip install -r requirements.txt`
      
Try running test suite:

`python -m unittest discover`

You can try playing versus random AI:

`python HumanVersusRandomAi.py`

Or you can try autoplay random vs random:

`python RandomAiVersusRandomAi.py`