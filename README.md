# 590PR Final_Project

# Title: Best Dating Match

## Team Member(s):

SmriitiSinghal, yuexian2, EmmaYazhuo

# Monte Carlo Simulation Scenario & Purpose:
Goal: Finding best match of a person for dating and predicting the probability of it to be a good match in real life.

A person access a dating portal to find a potential best match for him for dating. The portal database has a large pool of people (say 200) to choose from. It is very difficult and time consuming to view each profile, make decision and finally come up with the best one. 
So, we take some input parameters from the user and based on those, try to suggest some potential compatible people to him. 

Input fields/parameters: (subject to change)

About You:

Name-
Sex(dropdown)- Male, Female, Bisexual, Transgender, other
Age- 
Nationality- 
City-
Country-
Personality (dropdown)- Introvert, extrovert, ambivert
Status- single, married, divorced
Likes(multiple checkbox)-  Travelling, adventures, pets, partying etc. 
Relationship Looking for (dropdown)- a) Casual    b) Serious   c) haven’t decided

Partner’s Characteristics

Gender (dropdown)- Male, Female, Bisexual, Transgender, other 
Status- single, married, divorced, N/A
Nationality- 
City- 
Country-

After taking all the inputs- now input 3 parameters among these which according to you should hold highest priority.
Now look at the database containing data of 200 people having these same parameters .
Give an individual Match Score to each person- 
a)	If a preference match – add 1 to the score.
b)	If a preference match which is among one of the highest priority fields – add 1.75 to the score. 

Now, give the user top 5 compatible matches based on the Match Score.

## Simulation's variables of uncertainty
Partner’s acceptance/ decine- Boolean random variable (0 or 1)

a)	If the person declines (value 0)- there is no chance of further communication/ meeting. 
Prob(likeness)= 0.
b)	If the person accepts (value 1)- means they are going to set up a date and meet each other.

                  There are further 2 scenarios

i)	You like your partner- Boolean random variable (0 or 1)
ii)	Your partner likes you - Boolean random variable (0 or 1)

There are four possible scenarios – (0,0), (0,1), (1,0), (1,1)

Condition to be a successful date- (1,1)
Conditions to be an unsuccessful date- (0,0), (0,1), (1,0)

Run Monte Carlo simulation on these 3 variables to find the prob( successful date).

Finally, we predict the probabilities of actually liking the top 5 recommendations, give ranking from 1(highest prob.)to 5 (lowest prob) and returns the most suitable match. 

Note- We are working towards finding more variables to incorporate in monte carlo simulation.


## Hypothesis or hypotheses before running the simulation:

Assumption- If you find a perfect match and the other person also accepts the request- they are going to meet each other on a date to finally decide if they like each other. 

## Analytical Summary of your findings: (e.g. Did you adjust the scenario based on previous simulation outcomes?  What are the management decisions one could make from your simulation's output, etc.)

## Instructions on how to use the program:

## All Sources Used:
