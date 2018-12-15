# 590PR Final_Project

# Title: Finding Best Dating Match in optimal time

## Team Member(s):

SmriitiSinghal, yuexian2, EmmaYazhuo

# Monte Carlo Simulation Scenario & Purpose:
Goal: 
We are simulating the scenario where a user goes to an online dating website to find the best match for himself. Based on the personal information he enters, the website will recommend a potential list of candidates for real-life dating. Then, the user will meet these candidates one by one in real life. But going through all the candidates and then making a decision is not wise or advisable due to many factors. So, we are helping USER to decide the best time for him to make a choice to find the best matched person. 

Problem with meeting all the candidates and then making a decision:
The problem with this strategy is that because it takes a little bit long time for the USER to meet everybody and then make a decision, there are high chances that the best candidate may have already been chosen by others or loses interest in him as waiting time increases. It is also not very wise for him to make decisions very quickly because the best candidate may be among the remaining candidates. Therefore, choosing a right time to make decisions is really important.
We can not use simple calculations to achieve this goal, so we decide to apply Monte Carlo simulation.

First, we’ve created a user interface where the user can provide his personal information:

First Name
Last Name
Gender: male, female 
Age
Nationality
City
Personality: introvert, extrovert, ambivert 
Likes: travelling, adventures, pets, partying etc. 

Then, we ask the user to enter his three highest priority parameters among them which according to him matters most to him while choosing a match. With these input, we look into the database (dummy dataset containing information of 200 people) and recommend the user his top matches based on the base score. 

Criteria for giving base score:
1.	For city/nationality/personality -> add 1 to the base score.
If any field is chosen as preferred field -> further add .75 to the base score
2.	For the likes  -> add 0.5 to the base score for each match within the list of likes.
If chosen as preferred field -> further add .375 to the base score
 
Then, the user can specify the number of candidates (input parameter)  he wants to meet, and whether to meet these candidates randomly or in the ranking order from highest base scores to the lowest. Based on these, the website will provide the user with a list of top matches.

The base score is system generated, based on the input matches and we cannot solely decide the best matches based on this score. When the user will meet the candidates in real time, he will have certain first impression of these candidates which can be contrasting to the base score as well. So, we have considered a random variable – 'impression score' which follows a normal distribution pattern.

Final score= base score + impression score.

Failure Probability:
prob of user failing to get the best candidate even if he/she already met the candidate in the given stop time.

There are 3 scenarios:
1.	The candidate refuses to meet the user before setting up the meeting -> constant value.
2.	Till the time the user makes decision, the best candidate person has been chosen by someone else, the probability increases linearly with time lapsed. If the candidate has other good matches also within the database, prob. of the chosen by someone else further increases by 10%. -> linear pattern
3.	Till the time the user makes decision, the candidate loses interest because tired of waiting/felt neglected. Prob. increases exponentially with the increase in time interval since meeting the user. -> exponential pattern

Failure Prob.= Prob(refuse before meet) + Prob(chosen by someone else) + Prob(looses interest / tired of waiting)

For each stop time, calculate the probability of user to gets the best candidate successfully. Now, applying Monte Carlo Simulation, simulate the code 10,000 times.

 Finally predict the 'Best Time' for user to make choice when he can have the highest probability to find the best matched person. 
 
## Simulation's varaibles of uncertainty
1. Impression score -> follows normal distribution.
2. Whether the user can get the best candidate -> follows binomial distribution

## Hypothesis or hypotheses before running the simulation:
1. The user will consider meeting all the potential matches recommended by the website and will decide the best match after the first meeting. 
2. For the failure probability, we have hypothetically taken the equations for failure probability for all the 3 failure scenarios.

## Analytical Summary of your findings: (e.g. Did you adjust the scenario based on previous simulation outcomes?  What are the management decisions one could make from your simulation's output, etc.)

Based on User's personal information, the program pfredicts the 'Best Time' for USER to make choice when he can have the highest probability to find the best matched person. The 'Best Time' comes early in the case when the user specifies in meeting the candidates in the ranking order from highest base scores to the lowest in comparison to the case when he chooses to meet the candidates randomly. 

This 'Best Time' varies for user to user based on their specific input parameters.
For a USER having same input paarmeters, the 'Best Time' comes out to be the same every time the program is run -> because of                                                                                                               implementing Monte Carlo Simulation.
## Instructions on how to use the program:
Follow all the steps and input all the information as asked on the user interface. No special setup required.

## All Sources Used:
