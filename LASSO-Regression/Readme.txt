Question:
Read about and download the blogFeedback dataset from here:
https://archive.ics.uci.edu/ml/datasets/BlogFeedback
1. Perform Least Squares Regression, Ridge Regression, and LASSO to predict the target
variable. You can use any package to do this, but ensure that the parameters are crossvalidated. Train on BlogData Train.csv and test on blogData test-2012.03.31.01 00.csv.
Report RMSE for each model.
2. What are the most important features according to LASSO?

Solution:

The program is written as a python notebook text, it can be run using Jupyter Notebooks. 
Please run all the cells to find the outputs required which are stored in Outputs.txt
Outputs.txt contains the RMSE for the optimal Alpha for ridge and lasso regression along with the top features found by taking the weights from Lasso regression for the optimum alpha value.
The top features are stored as the column numbers from the original dataset.