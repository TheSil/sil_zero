# SilZero 

Experimenting with AI ideas...

TODO in chess backend: 
 - threefold repetition

TODO in AI:
 - connect to actual neural network
 - add exploration noise

Some notable modifications:
 - game states are remembered in search tree nodes to speed up the traversion (each game move is applied exactly once per leaf)
 - numbers of iterations (simulations) per search are rounded down to previous multiple of numbers of legal moves. This way visit counts can be always evened out (less bias in first moves checked)

To play with the repository, you just need to have Python 3 installed. Download this repository and go to its root folder. 

Install python pre-requisities:

`python -m pip install -r requirements.txt`
      
Try running test suite:

`python -m unittest discover`

You can try playing versus random AI:

`python HumanVersusRandomAi.py`

Or you can try autoplay random vs random:

`python RandomAiVersusRandomAi.py`