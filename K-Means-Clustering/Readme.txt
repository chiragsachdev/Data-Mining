Question:
Download the fine foods dataset from:
http://snap.stanford.edu/data/web-FineFoods.html
Perform the following:
• Identify all the unique words that appear in the “review/text” field of the reviews. Denote
the set of such words as L.
• Remove from L all stopwords in “Long Stopword List” from http://www.ranks.nl/stopwords.
Denote the cleaned set as W.
• Count the number of times each word in W appears among all reviews (“review/text” field)
and identify the top 500 words.
• Vectorize all reviews (“review/text” field) using these 500 words.
• Cluster the vectorized reviews into 10 clusters using k-means. You are allowed to use any
program or code for k-means (Weka has k-means too). This will give you 10 centroid
vectors.
• From each centroid, select the top 5 words that represent the centroid (i.e., the words with
the highest feature values)
• Submit the following:
1. Top 500 words + counts for these words
2. The top 5 words representing each cluster and their feature values (50 words + 50
values).

Solution:

This file is made as a python3 program.

1. Place this script in a folder.
2. Create a Folder called "DataSet" inside this folder usch that the path of the dataset would be "./DataSet/foods.txt"
3. Place the long stopwords in the Datset Folder such that the path of the stopwords would be "./DataSet/long_stopwords.txt"

4. Execute the script from the commandline using python3 in unix and py in windows.*

The required outputs get stored in the Outputs folder.
The program has ben made on a windows system and has been tested on a unix commandline as well.
If using windows, please use powershell instead of the command prompt to run this code.

The program has been designed to read contents in the DataSet folder, namely the dataset and stopwords.
Perform Preprossessing and then cluster the data and find out the top 5 words.
In the outputs folder, top 500 words along with their counts are stored as a csv file whereas the top 5 words of every cluster is stored as in a text file.

*
For unix based systems run the program using "python3 myscript.py"
for windows based systems run the program using powershell using "py myscript.py"
