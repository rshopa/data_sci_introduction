#install.packages("caret")
#install.packages("rpart")
#install.packages("tree")
#install.packages("randomForest")
#install.packages("e1071")
#install.packages("ggplot2")
#install.packages("caTools")

library(caret)
library(rpart)
library(tree)
library(randomForest)
library(e1071)
library(ggplot2)
library(caTools)

##############################################
# Step 1: Read in Data and look at the summary

dataSW <- read.csv('seaflow_21min.csv')
summary(dataSW)

## Question 1
## How many particles labeled "synecho" are in the file provided?

dim(dataSW[dataSW$pop == 'synecho',])[1]
table(dataSW$pop)[['synecho']]

## Question 2
## What is the 3rd Quantile of the field fsc_small?

summary(dataSW$fsc_small)[['3rd Qu.']]
summary(dataSW$fsc_small)[[5]]

#####################################################
## Step 2: Split the data into test and training sets

set.seed(9889)
train <- sample(1:dim(dataSW)[1],dim(dataSW)[1]/2)
dataTrain <- dataSW[train,]
dataTest <- dataSW[-train,]

## Question 3
## What is the mean of the variable "time" for your training set?

mean(dataTrain$time)

########################
## Step 3: Plot the data

# ggplot...

ggplot(dataSW, mapping = aes(x = pe, y = chl_small,
       color = pop)) + geom_point()

# ... or lattice library
       
library(lattice)
xyplot(chl_small ~ pe, data = dataSW, pch = 20,
       auto.key=list(space = "right", points = TRUE),
       groups = pop,
       xlab = "Phycoerythrin fluorescence",
       ylab = "Chlorophyll big")

## Question 4
## In the plot of pe vs. chl_small, the particles labeled ultra
## should appear to be somewhat "mixed" with two other populations
## of particles. Which two populations?

## nano & pico

################################
## Step 4: Train a decision tree


# IMPORTANT NOTE!!!
# a model, proposed in assignment was without one parameter (fsc_big):
# fsc_small + fsc_perp + chl_small + pe + chl_big + chl_small
# as it looks like a mistake, I've put it here as a term:
#                                             |
#                                             V
f1 <- formula(pop ~ fsc_small + fsc_perp + fsc_big 
              + chl_small + pe + chl_big + chl_small)
model <- rpart(f1, method="class", data = dataTrain)
print(model)

# Question 5
# Use print(model) to inspect your tree. Which populations, if any,
# is your tree incapable of recognizing? (Which populations do not appear
# on any branch?) (It's possible, but very unlikely, that
# an incorrect answer to this question is the result of improbable sampling.)

plot(model)
text(model,cex=0.75)

# "crypto" does not appear on the tree branches

levels(dataTrain$pop)
table(dataTrain$pop)

# Question 6
# Most trees will include a node near the root that applies a rule
# to the pe field, where particles with a value less than some threshold
# will descend down one branch, and particles with a value greater
# than some threshold will descend down a different branch. If you look
# at the plot you created previously, you can verify that the threshold
# used in the tree is evident visually. What is the value of the threshold
# on the pe field learned in your model?

# 5004

# Question 7
# Based on your decision tree, which variables appear to be most important
# in predicting the class population?

names(model)
names(which.max(model$variable.importance))

# "chl_small"

######################################################
## Step 5: Evaluate the decision tree on the test data

predTest <- predict(model,dataTest,type='class')
table(predTest)

# Question 8
# How accurate was your decision tree on the test data?
# Enter a number between 0 and 1.

sum(predTest == dataTest$pop)/length(dataTest$pop)

#############################################
## Step 6: Build and evaluate a random forest

# Load the randomForest library, then call randomForest 
# using the formula object and the data, as you did to build a single tree:

library(randomForest)
modelRF <- randomForest(f1, method = "class", data = dataTrain)
predRF <- predict(modelRF, dataTest, type='class')
table(predRF)


# Question 9
# What was the accuracy of your random forest model on the test data?
# Enter a number between 0 and 1

sum(predRF == dataTest$pop)/length(dataTest$pop)

# A random forest can obtain another estimate of variable importance 
# based on the Gini impurity that we discussed in the lecture. 
# The function importance(model) prints the mean decrease in 
# gini importance for each variable.

# Question 10
# After calling importance(model), you should be able to determine 
# which variables appear to be most important in terms of the 
# gini impurity measure. Which ones are they?

importance(modelRF)

# chl_small         8102.789
# pe                8863.055

###################################################################
## Step 7: Train a support vector machine model and compare results

modelSVM <- svm(f1, method = "class", data = dataTrain)

# Question 11
# What was the accuracy of your support vector machine model 
# on the test data? Enter a number between 0 and 1.

predSVM <- predict(modelSVM, dataTest, type='class')
table(predSVM)
accSVM <- sum(predSVM == dataTest$pop)/length(dataTest$pop)
accSVM
# will be used for the final Question

#######################################
## Step 8: Construct confusion matrices

# decision tree
table(pred = predTest, true = dataTest$pop)

# random forest
table(pred = predRF, true = dataTest$pop)

# support vector machine
table(pred = predSVM, true = dataTest$pop)

# Question 12
# What appears to be the most common error the models make?

# ultra -> pico, nano - > ultra

################################
## Step 9: Sanity check the data

# The measurements in this dataset are all supposed to be continuous 
# (fsc_small, fsc_perp, fsc_big, pe, chl_small, chl_big), but one is not. 
# Using plots or R code, figure out which field is corrupted.


# Question 13
# The variables in the dataset were assumed to be continuous, but 
# one of them takes on only a few discrete values, suggesting a problem. 
# Which variable exhibits this problem?

# relationships between predictors - a usefyl tool!
plot(dataSW[,6:11], col = "blue", pch = 20)

# it's clearly visible that fsc_big is corrupted

# Remove this data from the dataset by filtering out all data associated 
# with file_id 208, then repeat the experiment for all three methods, 
# making sure to split the dataset into training and test sets 
# after filtering out the bad data.

dataFiltered <- subset(dataSW, file_id != 208)

# repeat the whole sequence of steps

set.seed(1984)
train <- sample(1:dim(dataFiltered)[1],dim(dataFiltered)[1]/2)
dataTrain <- dataFiltered[train,]
dataTest <- dataFiltered[-train,]

# desision tree
modelDT <- rpart(f1, method="class", data = dataTrain)
predDT <- predict(modelDT,dataTest,type='class')
table(predDT)
sum(predDT == dataTest$pop)/length(dataTest$pop)

# random forest
modelRF <- randomForest(f1, method = "class", data = dataTrain)
predRF <- predict(modelRF, dataTest, type='class')
table(predRF)
sum(predRF == dataTest$pop)/length(dataTest$pop)

# support vector machine
modelSVM <- svm(f1, method = "class", data = dataTrain)
predSVM <- predict(modelSVM, dataTest, type='class')
table(predSVM)
accSVMfiltered <- sum(predSVM == dataTest$pop)/length(dataTest$pop)
accSVMfiltered # accuracy

# Question 14
# After removing data associated with file_id 208, what was the effect 
# on the accuracy of your svm model? Enter a positive or negative number 
# representing the net change in accuracy, where a positive number 
# represents an improvement in accuracy and a negative number 
# represents a decrease in accuracy.

accSVMfiltered - accSVM

# accuracy change:
# 0.97110095 - 0.91974455 = 0.0513564
