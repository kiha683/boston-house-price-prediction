# boston-house-price-prediction

This project predicts the median value of owner-occupied homes in $1000's in the Boston area using linear regression, catboost and neural network.
Requirements

## The code requires the following libraries to be installed:

    numpy
    matplotlib
    pandas
    seaborn
    sklearn
    catboost
    shap
    keras

## Data

The data used in this project is from the sklearn library's Boston Housing dataset. The dataset contains 506 rows and 14 columns. The target variable is the median value of owner-occupied homes in $1000's in the Boston area.

## Methodology

The project uses multiple regression, Yandex Catboost and neural network to predict the median value of owner-occupied homes in the Boston area. First, correlation analysis and scatter plots of the three most correlated variables with the target variable are performed. Then, the data is split into training and testing sets. The linear regression model is trained on the training set and its accuracy is tested on the test set using R2 score. The Catboost model is then trained and optimized using grid search. Finally, a neural network with one hidden layer is trained and evaluated.

## Conclusion

The linear regression model has an R2 score of 0.71, the Catboost model has an R2 score of 0.77 and the neural network has an R2 score of 0.77. All three models provide reasonable accuracy in predicting the median value of owner-occupied homes in the Boston area.
