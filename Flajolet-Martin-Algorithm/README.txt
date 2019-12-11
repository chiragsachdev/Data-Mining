Question:
Implement the Flajolet-Martin (FM) algorithm. Count the number of distinct quotes (quotes
are denoted with lines that start with Q) in the MemeTracker dataset (all Files):
https://snap.stanford.edu/data/memetracker9.html

Solution:

This is my implementation of the Flajolet-Martin Algorithm for the dataset provided.
To install dependancies please run the command from a shell.
"python3 -m pip install -r requirements.txt"
Place the Dataset in "./Data/" in the directory where the script is located.
Please run the program using the command
"python3 myscript.py"
The program is designed to read the various txt files containing the data placed in the "./Data/" folder. The data is read in chunks approx. 64 MB where the quotes are hashed and then the tailing 0's are calculated.
The program then writes the poututs to a file Outputs.txt.
