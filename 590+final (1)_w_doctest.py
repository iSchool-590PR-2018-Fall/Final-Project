import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats

# PERT distribution will be used for generate diet calorie, diet_break calorie, exercise time
def pert_rand(s:int,p:int,l:int,con:int,size:int):
    ''' Generalize excercise duration by modified PERT distribution
    :param s: lower bound
    :param p: most likely value
    :param l: upper bound
    :param con: confidence level
    :param size: population size
    :return:an nd.array containing samples from pert distribution with parameters input

    >>> pert_rand('a',3,6,3,1000)# type error
    Traceback (most recent call last):
    TypeError: must be str, not int
    >>> sample=pert_rand(3,5,10,4,100)
    >>> type(sample)
    <class 'numpy.ndarray'>
    >>> len(sample)
    100
    '''
    con = min(8, con)
    con = max(2, con)
    # calculate the mean of PERT dist
    m = (s + con * p + l) / (con + 2)
    # lower & upper bound in beta dist
    a = (m - s) / (l - s) * (con + 2)
    b = ((con + 1) * l - s - con * p) / (l - s)
    beta = np.random.beta(a, b, size)
    beta = beta * (l - s) + s
    return beta

def diet_monthly(diet_pop,month=1):
    '''given a series of people who wants to lose weight, this function will generate number = len(diet_pop) of calories
    return a list of total calorie changes for each female who wants to lose weight over 30 days
    :param diet_pop: panda series containing people who wants to lose weight by only dieting
    :param month: an int the represent months during which the person wil have diet
    
    :return diet_list: total calorie cuts for each female in a month, stored in a list
    >>> test_data=pd.DataFrame(list(range(1,10001)))
    >>> sample=diet_monthly(test_data,month=3)
    >>> len(sample) # length of output data should correspond to the length of input dataframe
    10000
    '''
    # 0.9 chance the person will have a diet; 0.1 chance the person will have a diet-break and eat more
    diet_list = []

    for i in range(len(diet_pop)):
        diet = pert_rand(-1000, -250, 0, 4, int(month * 30 * 0.9))
        diet_break = pert_rand(0, 250, 500, -100, int(month * 30 * 0.1))
        diet_list.append(sum(diet)+sum(diet_break))
    return diet_list       

def exercise_monthly(ex_pop, month =1):
    '''return a list of total exercise time for each female who wants to lose weight over 30 days
    :param ex_pop: panda series containing people who wants to lose weight by only exercising
    :param month: an int the represent months during which the person wil have exercise. 
    :return ex_time: total exercising time in minutes over a month, stored in a list
    >>> test_data=pd.DataFrame(list(range(1,10001)))
    >>> sample=exercise_monthly(test_data,3)
    >>> len(sample) # length of data output should correspond to the length of dataframe input
    10000
    >>> min(sample)>=0 # minimum exercise time
    True
    >>> max(sample)<=4320 # maximun exercise time
    True
    '''
    ex_time = []
    for i in range(len(ex_pop)):
        ex_time.append(sum(pert_rand(0,60,120,4,int(12*month)))) # exercise 3 times a week, 4 week per month, so 12 times per month
    return ex_time

def meal_multiple(maintain_pop,month =1):
    '''return a list of multiples that will be used to multiple with BMR and get a total calorie change due to meals for each person who wants to maintain 
    their weights over 30 days.  
    :param maintain_pop: panda series containing people who wants to maintain weights
    :param month: an int the represent months during which the person wil have a random calorie intake that follows a normal distribution with the mean of 0
    
    :return multiple: total multiples over a month, stored in a list
    >>> test_data=pd.DataFrame(list(range(1,10001)))
    >>> sample=meal_multiple(test_data,3)
    >>> len(sample) # length of data output should correspond to the length of dataframe input
    10000
    >>> min(sample)>=-9
    True
    >>> max(sample)<=90
    True
    '''
    multiple = []
    for i in range(len(maintain_pop)):
        multiple.append(sum(pert_rand(-0.1,0.1,1.5,10,int(30*month)))) # exercise 3 times a week, 4 week per month, so 12 times per month
    multiple = np.array(multiple)
    return multiple

def ex_multiple(maintain_pop,month=1):
    '''return a list of multiples that will be used to multiple with BMR and get a total calorie change due to exercise for each person who wants to maintain 
    their weights over 30 days
    :param maintain_pop: panda series containing people who wants to maintain weights
    :param month: an int the represent months during which the person wil have a random exercise amont follows  PERT distribution
    
    :return multiple: total multiples over a month, stored in a list
    >>> test_data=pd.DataFrame(list(range(1,10001)))
    >>> sample=ex_multiple(test_data,3)
    >>> len(sample) # length of data output should correspond to the length of dataframe input
    10000
    >>> min(sample)>=0
    True
    >>> max(sample)<=18
    True

    '''
    multiple = []
    for i in range(len(maintain_pop)):
        multiple.append(sum(pert_rand(0,0.1,0.2,1,int(30*month)))) 
    multiple = np.array(multiple)
    return multiple

def cal2lb(calories,month=1):
    '''calcualte weight changes in pounds reflecting the calorie effects
    :param calories: an array of calories
    :param month: an int the represent months during which the person is to realize his/her goal
    
    :return lb: a list of weight changes
    >>> cal2lb([-300,200])
    [-0.08105228571428572, -0.018666714285714286]
    '''
    lb = []
    for i in range(len(calories)):
        if calories[i]<0:
            wl_adj = 0.0002*month*0.9*month*0.9+0.005*month*0.9
            lb.append(calories[i]/3500+wl_adj)
        elif calories[i]>=0:
            wg_adj = 0.0001*month*0.9*month*0.9+0.027*month*0.9
            lb.append(calories[i]/35000-wg_adj)
    return lb


def eat_more(diet_gw_pop, month =1):
    '''given a series of people who wants to lose weight, this function will generate a list of calories
    :param diet_gw_pop: a dataframe containing males who want to gain weight by only eat more calories
    :param month: an int the represent months during which the person is to realize his/her goal
    
    :return diet_list: a list of total calories that a man will add in a month
    >>> diet_gw_pop = np.random.randint(10,50,8)
    >>> len(diet_gw_pop)
    8
    '''
    # 0.9 (27 days a month) chance follow diet calorie and 0.1 of diet-break
    diet_list = []

    for i in range(len(diet_gw_pop)):
        diet = pert_rand(200, 1000, 1500, 1000, int(30 * month))
        diet_list.append(sum(diet))
    return diet_list       


def light_ex(ex_gw_pop,month =1):
    '''given a series of people who wants to lose weight, this function will generate a list of exercise time
    :param diet_gw_pop: a dataframe containing males who want to gain weight by eat more and exercise
    :param month: an int the represent months during which the person is to realize his/her goal
    
    :return diet_list: a list of total exercise time in minutes that a man will do in a month
    >>> diet_gw_pop = np.random.randint(5,10,19)
    >>> len(diet_gw_pop)
    19
    '''
    ex_time = []
    for i in range(len(ex_gw_pop)):
        ex_time.append(sum(pert_rand(0,15,30,4,int(4*month)))) # exercise 4 times per month
    return ex_time    


# ## Population simulation

# FIRST, DETERMINE THE DISTRIBUTION BY EXPLORING REAL DATA
data = pd.read_csv('590final.csv')
age = pd.read_csv('590age.csv')
m = data[data.Gender=='Male']
f = data[data.Gender=='Female']

# BASE ON THE ABOVE DISTRIBUTIONS, SIMULATION A POPULATION WITH SIZE DETERMINED BY USER. THE USER WILL ALSO DECIDE WHO MANY MONTHS
# OF RESULTS HE/SHE WANTS TO SEE
def population(pop_size=1000,male=m,female=f):
    ''' Generate a population with age, gender, body weight, height, and goals (lose weight, maintain, or gain weight)
    :param pop_size: an int representing the size of the population
    :param male: a dataframe containing real male body weight and height. It provides the distribution that will be used to generate male body weight&height
    :param female: a dataframe containing real female body weight and height. It provides the distribution that will be used to generate female body weight&height
    
    :return male_pop, female_pop: two dataframes containing male/female population information
    :return male_lw: dataframe, male who wants to lose weight
    :return male_maintain: dataframe, male who wants to maintain weight
    :return male_gw: dataframe, male who wants to gain weight
    :return female_lw: dataframe, female who wants to lose weight
    :return female_maintain: dataframe, female who wants to maintain weight
    >>> sample=population(10000)
    >>> type(sample[0])
    <class 'pandas.core.frame.DataFrame'>
    >>> round(len(sample[2])/sample[7],2)
    0.26
    >>> sample[0].columns.values
    array(['Age', 'Gender', 'Weight', 'Height', 'Target Heart Rate', 'Goal'],
          dtype=object)

    '''
    # age - custom discrete distribution
    # ocurred ages in dataset
    xk = (42, 41, 40, 39, 38, 37, 36, 35, 34, 33, 32, 31, 30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 12)
    # frequency of ocurrance of each age 
    pk = (0.0209509471835403, 0.00259273198678543, 0.00301091456529921, 0.00374273407769832, 0.0043490988165433, 0.00497637268431397, 0.00554091916530757, 0.00635637519340944, 0.00805001463639025, 0.00920001672730314, 0.0109145652992096, 0.012169113034751, 0.0149082089240162, 0.0190063981934513, 0.0236064065571028, 0.0263455024463681, 0.0305273282315059, 0.0396437084431063, 0.0605110191109438, 0.104901099820181, 0.161188474888136, 0.16281938694434, 0.157278467779032, 0.104692008530925, 0.00242545895537992, 0.00020909128925689, 6.27273867770669E-05, 0.000020909128925689)
    # customed age distribution
    custm = stats.rv_discrete(name='custm', values=(xk, pk))
    rdm_age = custm.rvs(size=pop_size)
    rdm_age = pd.DataFrame(rdm_age)

    # Gender - custom discrete distribution (according to UIUC, male:female  = 0.541156783:0.458843217)
    # male: 1; female: 0
    xk = (1,0)
    pk = (0.541156783,0.458843217)
    gender_dist = stats.rv_discrete(name='gender_dist', values=(xk, pk))
    rdm_gender = gender_dist.rvs(size=pop_size)
    rdm_gender = pd.DataFrame(rdm_gender)
    age_gender = pd.concat([rdm_age, rdm_gender],axis=1)
    age_gender.columns=['Age','Gender']

    # calculate number of male
    num_male = len(age_gender[age_gender.Gender == 1])
    #calculate number of female
    num_female = len(age_gender[age_gender.Gender == 0])

    # body weight & height - 2D normal distribution
    #male
    male_cov = np.cov(male.Weight, male.Height)
    male_mean = (np.mean(male.Weight-27), np.mean(male.Height))
    male = np.random.multivariate_normal(male_mean, male_cov,(num_male))
    rdm_male = pd.DataFrame(male)
    rdm_male.columns=['Weight','Height']
    
    #female
    female_cov = np.cov(female.Weight, female.Height)
    female_mean = (np.mean(female.Weight), np.mean(female.Height))
    female = np.random.multivariate_normal(female_mean, female_cov,(num_female))
    rdm_female = pd.DataFrame(female)
    rdm_female.columns=['Weight','Height']
    
    #combine age and body weight&height; identify male and female
    age_gender_male = age_gender[age_gender.Gender == 1]
    age_gender_female = age_gender[age_gender.Gender == 0]
    age_gender_male.reset_index(drop=True, inplace=True)
    rdm_male.reset_index(drop=True,inplace=True)
    age_gender_female.reset_index(drop=True, inplace=True)
    rdm_female.reset_index(drop=True,inplace=True)
    
    male_pop = pd.concat([age_gender_male,rdm_male],axis=1)
    female_pop = pd.concat([age_gender_female,rdm_female],axis=1)
    
    male_pop['Target Heart Rate'] = 188.5-0.775*male_pop.Age
    female_pop['Target Heart Rate'] = 188.5-0.775*female_pop.Age
    
    # Set goals for male and female 
    # Suppose 26% male wants to lose weight, 14% of them wants to gain wegiht, and the rest 60% wants to maintain

    male_lw = male_pop.sample(frac=0.26)
    male_gw = male_pop.drop(male_pop.index[male_lw.index.values]).sample(frac=0.14/(1-0.26))
    male_maintain = male_pop.drop(male_pop.index[list(male_lw.index.values)+list(male_gw.index.values)])
    male_pop['Goal']= np.zeros(len(male_pop))
    male_pop.loc[male_lw.index.values,'Goal'] = 'Lose Weight'
    male_pop.loc[male_gw.index.values,'Goal'] = 'Gain Weight'
    male_pop.loc[male_maintain.index.values,'Goal'] = 'Maintain'


    # Suppose 87% female wants to lose weight, and the rest 13% wants to maintain
    female_lw = female_pop.sample(frac = 0.75)
    female_maintain = female_pop.drop(female_pop.index[female_lw.index.values])
    female_pop['Goal']= np.zeros(len(female_pop))
    female_pop.loc[female_lw.index.values,'Goal'] = 'Lose Weight'
    female_pop.loc[female_maintain.index.values,'Goal'] = 'Maintain'

    return male_pop, female_pop, male_lw, male_maintain,male_gw, female_lw, female_maintain,num_male, num_female


# ## Results

# In[26]:

def female_monthly( female_pop, goal ,month=1):
    '''Gives result after a month for women
    :param female_pop: a dataframe representing a subset of female with a certain goal
    :param goal: a string that shows the goal. Two goals avaialbe: "Lose Weight","Maintain"
    :return result: a dataframe with columns: 'BMR','Diet (calories)','Exercise Time/Multiple','Weight Change',and 'New Weight'  
    >>> p = population(15)
    >>> result = female_monthly(p[1],'Maintain') # doctest:+ELLIPSIS
    There are ... weight change.
    >>> type(result)
    <class 'pandas.core.frame.DataFrame'>
    '''
    female_reset = female_pop.reset_index(drop=True)
    one_month_later = pd.DataFrame()
    one_month_later['BMR'] = 655+(4.35*female_reset.Weight)+(4.7*female_reset.Height)-(4.7*female_reset.Age)
    
    one_month_later['Diet (calories)'] =  np.zeros(len(female_reset))
    one_month_later['Exercise Time/Multiple'] =  np.zeros(len(female_reset))
    one_month_later['Weight Change'] = np.zeros(len(female_reset))
    one_month_later['New Weight'] = np.zeros(len(female_reset))
    # For women who wants to lose weight:
    if goal == 'Lose Weight':       
        diet_pop = female_reset.sample(frac = 1/3)
        diet_result = one_month_later.loc[diet_pop.index.values,:]
        ex_pop =  female_reset.drop(diet_pop.index.values).sample(frac=1/2)
        ex_result = one_month_later.loc[ex_pop.index.values,:]
        combo_pop = female_reset.drop(list(diet_pop.index.values) +  list(ex_pop.index.values))
        combo_result = one_month_later.loc[combo_pop.index.values,:]
        #simulate total diet change and exercise time over a month for each woman who wants to lose weight
        diet_result['Diet (calories)']=diet_monthly(diet_pop)
        ex_result['Exercise Time/Multiple'] = exercise_monthly(ex_pop)
        combo_result['Diet (calories)']=diet_monthly(combo_pop)
        combo_result['Exercise Time/Multiple'] = exercise_monthly(combo_pop)

        #calculate net calorie change for each women in the month
        ex_cal = np.array(-(((0.074*ex_pop.Age) - (0.05741*ex_pop.Weight) + (ex_pop['Target Heart Rate']*0.4472) - 20.4022)*ex_result['Exercise Time/Multiple']/4.184))
        combo_cal = np.array(diet_monthly(combo_pop))-np.array(((0.074*combo_pop.Age) - (0.05741*combo_pop.Weight) + (combo_pop['Target Heart Rate']*0.4472) - 20.4022)*combo_result['Exercise Time/Multiple']/4.184)

        # calculate weight change based on the total calorie changes through diet and exercise
        diet_result['Weight Change']= cal2lb(np.array(diet_result['Diet (calories)']))
        ex_result['Weight Change'] = cal2lb(ex_cal)
        combo_result['Weight Change']= cal2lb(combo_cal)
        
        # calculate new weights
        diet_result['New Weight']= diet_result['Weight Change']+diet_pop['Weight']
        ex_result['New Weight'] = ex_result['Weight Change']+ex_pop['Weight']
        combo_result['New Weight']= combo_result['Weight Change']+combo_pop['Weight']
            
        # result
        result = pd.concat([diet_result, ex_result, combo_result])
        result.sort_index(inplace= True)
        
        #visualization
        plt.plot((0,mon),(np.nanmean(diet_pop['Weight']),np.nanmean(diet_result['New Weight'])),'go-',color='steelblue',label='Only Diet Δ={}'.format(round(np.nanmean(diet_pop['Weight'])-np.nanmean(diet_result['New Weight']),4)))
        plt.plot((0,mon),(np.nanmean(ex_pop['Weight']),np.nanmean(ex_result['New Weight'])),'go-',color='firebrick',label='Only Exercise Δ={}'.format(round(np.nanmean(ex_pop['Weight'])-np.nanmean(ex_result['New Weight'])),4))
        plt.plot((0,mon),(np.nanmean(combo_pop['Weight']),np.nanmean(combo_result['New Weight'])),'go-',color='chocolate',label='Diet&Exercise Δ={}'.format(round(np.nanmean(combo_pop['Weight'])-np.nanmean(combo_result['New Weight'])),4))
        plt.title(('Average Weight: {} Months Before vs. After').format(mon))
        plt.legend(loc='best')
        plt.xlabel('Month(s)')
        plt.ylabel('Weight (lb)')
        l = np.arange(mon+1)
        x = ['Month {}'.format(i) for i in range(mon+1)]
        plt.xticks(l,x)
        plt.show()
        
        plt.hist(diet_result['Weight Change'],color='steelblue',label = 'Only Diet',alpha = 0.5)
        plt.hist(ex_result['Weight Change'],color='firebrick',label = 'Only Exercise',alpha = 0.5)
        plt.hist(combo_result['Weight Change'],color='chocolate',label = 'Diet&Exercise',alpha = 0.5)
        plt.title('Weight Change Distribution')
        plt.xlabel('Weight Change (lb)')
        plt.ylabel('Frequency')
        plt.legend(loc='best')
        plt.show()
        print('There are {} of female students chose to lose weight during the past {} months. There are {} of them chose to lose weight by only dieting, and they lost {} lb on average; there are {} of them chose to only exercise and they lost {} lb on average; there are {} of them chose to combine dieting and exercsing and they lost {} lb on average.'.format(len(female_reset),mon,len(diet_pop),round(np.nanmean(diet_pop['Weight'])-np.nanmean(diet_result['New Weight']),4),len(ex_pop),round(np.nanmean(ex_pop['Weight'])-np.nanmean(ex_result['New Weight']),4),len(combo_pop),round(np.nanmean(combo_pop['Weight'])-np.nanmean(combo_result['New Weight']),4)))
    
    if goal == 'Maintain':
        one_month_later['Diet (calories)'] = np.array(one_month_later['BMR'])*meal_multiple(female_reset)
        one_month_later['Exercise Time/Multiple'] = ex_multiple(female_reset)
        
        cal = np.array(one_month_later['Diet (calories)']) - ex_multiple(female_reset)*np.array(one_month_later['BMR'])
        
        one_month_later['Weight Change'] = cal2lb(cal)
        one_month_later['New Weight'] =  female_reset['Weight'] + one_month_later['Weight Change']
        
        result = one_month_later
        
        # visualization
        plt.plot((0,mon),(np.mean(female_reset.Weight),np.mean(result['New Weight'])),'go-',color = 'steelblue',label='Maintain Weight Δ={}'.format(round(np.mean(female_reset.Weight)-np.mean(result['New Weight']),4)))
        plt.legend(loc='best')
        plt.title(('Average Weight: {} Months Before vs. After').format(mon))
        plt.xlabel('Month(s)')
        plt.ylabel('Weight (lb)')
        l = np.arange(mon+1)
        x = ['Month {}'.format(i) for i in range(mon+1)]
        plt.xticks(l,x)
        plt.show()
        
        plt.hist(one_month_later['Weight Change'],color='steelblue',label = 'Maintain')
        plt.title('Weight Change Distribution')
        plt.xlabel('Weight Change (lb)')
        plt.ylabel('Frequency')
        plt.legend(loc='best')
        plt.show()
        print('There are {} of female students chose to maintain weight during the past {} months. There is an average of {} lb weight change.'.format(len(female_reset),mon,round(np.mean(female_reset.Weight)-np.mean(result['New Weight']),4)))
        
    result = pd.concat([female_reset,result],axis =1)
    return result

#--------------------------------------------------End of Female----------------------------------------------------------

def male_monthly(male_pop, goal = 'Lose Weight',month=1):
    '''Gives result after a month for women
    :param female_pop: a dataframe representing a subset of female with a certain goal
    :param goal: a string that shows the goal. Three goals avaialbe: "Lose Weight","Maintain", and "Gain Weight"
    :return result: a dataframe with columns: 'BMR','Diet (calories)','Exercise Time/Multiple','Weight Change',and 'New Weight'  
    >>> p = population(150)
    >>> result = male_monthly(p[0]) # doctest:+ELLIPSIS
    There are ... on average.
    >>> type(result)
    <class 'pandas.core.frame.DataFrame'>
    '''
    male_reset = male_pop.reset_index(drop=True)
    one_month_later = pd.DataFrame()
    one_month_later['BMR'] = 66+(6.23*male_reset.Weight)+(12.7*male_reset.Height)-(6.8*male_reset.Age)
    one_month_later['Diet (calories)'] =  np.zeros(len(male_reset))
    one_month_later['Exercise Time/Multiple'] =  np.zeros(len(male_reset))
    one_month_later['Weight Change'] = np.zeros(len(male_reset))
    one_month_later['New Weight'] = np.zeros(len(male_reset))
    
    # if lose weight
    if goal == 'Lose Weight':
        diet_pop = male_reset.sample(frac = 1/3)
        diet_result = one_month_later.loc[diet_pop.index.values,:]
        ex_pop =  male_reset.drop(diet_pop.index.values).sample(frac=1/2)
        ex_result = one_month_later.loc[ex_pop.index.values,:]
        combo_pop = male_reset.drop(list(diet_pop.index.values) +  list(ex_pop.index.values))
        combo_result = one_month_later.loc[combo_pop.index.values,:]
        #simulate total diet change and exercise time over a month for each woman who wants to lose weight
        diet_result['Diet (calories)']=diet_monthly(diet_pop)
        ex_result['Exercise Time/Multiple'] = exercise_monthly(ex_pop)
        combo_result['Diet (calories)']=diet_monthly(combo_pop)
        combo_result['Exercise Time/Multiple'] = exercise_monthly(combo_pop)

        #calculate net calorie change for each women in the month
        ex_cal = np.array(-(((0.2017*ex_pop.Age) - (0.09036*ex_pop.Weight) + (ex_pop['Target Heart Rate']*0.6309) - 55.0969)*ex_result['Exercise Time/Multiple']/4.184))
        combo_cal = np.array(diet_monthly(combo_pop))-(np.array(((0.2017*combo_pop.Age) - (0.09036*combo_pop.Weight) + (combo_pop['Target Heart Rate']*0.6309) - 55.0969)*combo_result['Exercise Time/Multiple']/4.184))


        # calculate weight change based on the total calorie changes through diet and exercise
        diet_result['Weight Change']= cal2lb(np.array(diet_result['Diet (calories)']))
        ex_result['Weight Change'] = cal2lb(ex_cal)
        combo_result['Weight Change']= cal2lb(combo_cal)

        diet_result['New Weight']= diet_result['Weight Change']+diet_pop['Weight']
        ex_result['New Weight'] = ex_result['Weight Change']+ex_pop['Weight']
        combo_result['New Weight']= combo_result['Weight Change']+combo_pop['Weight']


        result = pd.concat([diet_result, ex_result, combo_result])
        result.sort_index(inplace= True)
        
        #visualization
        plt.plot((0,mon),(np.mean(diet_pop['Weight']),np.mean(diet_result['New Weight'])),'go-',color='steelblue',label='Only Diet Δ={}'.format(round(np.nanmean(diet_pop['Weight'])-np.nanmean(diet_result['New Weight']),4)))
        plt.plot((0,mon),(np.mean(ex_pop['Weight']),np.mean(ex_result['New Weight'])),'go-',color='firebrick',label='Only Exercise Δ={}'.format(round(np.nanmean(ex_pop['Weight'])-np.nanmean(ex_result['New Weight']),4)))
        plt.plot((0,mon),(np.mean(combo_pop['Weight']),np.mean(combo_result['New Weight'])),'go-',color='chocolate',label='Diet&Exercise Δ={}'.format(round(np.nanmean(combo_pop['Weight'])-np.nanmean(combo_result['New Weight']),4)))
        plt.legend(loc='best')
        plt.title(('Average Weight: {} Months Before vs. After').format(mon))
        plt.xlabel('Month(s)')
        plt.ylabel('Weight (lb)')
        l = np.arange(mon+1)
        x = ['Month {}'.format(i) for i in range(mon+1)]
        plt.xticks(l,x)
        plt.show()
        
        plt.hist(diet_result['Weight Change'],color='steelblue',label = 'Only Diet',alpha = 0.5)
        plt.hist(ex_result['Weight Change'],color='firebrick',label = 'Only Exercise',alpha = 0.5)
        plt.hist(combo_result['Weight Change'],color='chocolate',label = 'Diet&Exercise',alpha = 0.5)
        plt.title('Weight Change Distribution')
        plt.xlabel('Weight Change (lb)')
        plt.ylabel('Frequency')
        plt.legend(loc='best')
        plt.show()
        print('There are {} of male students chose to lose weight during the past {} months. There are {} of them chose to lose weight by only dieting, and they lost {} lb on average; there are {} of them chose to only exercise and they lost {} lb on average; there are {} of them chose to combine dieting and exercsing and they lost {} lb on average.'.format(len(male_reset),mon,len(diet_pop),round(np.nanmean(diet_pop['Weight'])-np.nanmean(diet_result['New Weight']),4),len(ex_pop),round(np.nanmean(ex_pop['Weight'])-np.nanmean(ex_result['New Weight']),4),len(combo_pop),round(np.nanmean(combo_pop['Weight'])-np.nanmean(combo_result['New Weight']),4)))
    
    if goal == 'Maintain':
        one_month_later['Diet (calories)'] = np.array(one_month_later['BMR'])*meal_multiple(male_reset)
        one_month_later['Exercise Time/Multiple'] = ex_multiple(male_reset)
        
        cal = np.array(one_month_later['Diet (calories)']) - ex_multiple(male_reset)*np.array(one_month_later['BMR'])
        
        one_month_later['Weight Change'] = cal2lb(cal)
        one_month_later['New Weight'] =  male_reset['Weight'] + one_month_later['Weight Change']
        
        result = one_month_later
        
        # visualization
        plt.plot((0,mon),(np.mean(male_reset.Weight),np.mean(result['New Weight'])),'go-',color = 'steelblue',label='Maintain Weight Δ={}'.format(round(np.mean(male_reset.Weight)-np.mean(result['New Weight']),4)))
        plt.legend(loc='best')
        plt.title(('Average Weight: {} Months Before vs. After').format(mon))
        plt.xlabel('Month(s)')
        plt.ylabel('Weight (lb)')
        l = np.arange(mon+1)
        x = ['Month {}'.format(i) for i in range(mon+1)]
        plt.xticks(l,x)
        plt.show()
        
        plt.hist(one_month_later['Weight Change'],color='steelblue',label = 'Maintain')
        plt.title('Weight Change Distribution')
        plt.xlabel('Weight Change (lb)')
        plt.ylabel('Frequency')
        plt.legend(loc='best')
        plt.show()
        print('There are {} of male students chose to maintain weight during the past {} months. There is an average of {} lb weight change.'.format(len(male_reset),mon,round(np.mean(male_reset.Weight)-np.mean(result['New Weight']),4)))
        
        
    if goal == 'Gain Weight':
        diet_pop = male_reset.sample(frac = 1/2)
        diet_result = one_month_later.loc[diet_pop.index.values,:]
        combo_pop = male_reset.drop(diet_pop.index.values)
        combo_result = one_month_later.loc[combo_pop.index.values,:]

        #simulate total diet change and exercise time over a month for each woman who wants to lose weight
        diet_result['Diet (calories)']=eat_more(diet_pop)
        combo_result['Diet (calories)']=eat_more(combo_pop)
        combo_result['Exercise Time/Multiple'] = light_ex(combo_pop)

        #calculate net calorie change for each women in the month
        combo_cal = np.array(combo_result['Diet (calories)'])-(np.array(((0.2017*combo_pop.Age) - (0.09036*combo_pop.Weight) + (combo_pop['Target Heart Rate']*0.6309) - 55.0969)*combo_result['Exercise Time/Multiple']/4.184))

        # calculate weight change based on the total calorie changes through diet and exercise
        diet_result['Weight Change']= cal2lb(np.array(diet_result['Diet (calories)']))
        combo_result['Weight Change']= cal2lb(combo_cal)

        # calcualte new weight
        diet_result['New Weight']= diet_result['Weight Change']+diet_pop['Weight']
        combo_result['New Weight']= combo_result['Weight Change']+combo_pop['Weight']

        # result
        result = pd.concat([diet_result, combo_result])
        result.sort_index(inplace= True)

        #visualization
        plt.plot((0,mon),(np.mean(diet_pop['Weight']),np.mean(diet_result['New Weight'])),'go-',color='steelblue',label='Only Diet Δ={}'.format(round(-np.mean(diet_pop['Weight'])+np.mean(diet_result['New Weight']),4)))
        plt.plot((0,mon),(np.mean(combo_pop['Weight']),np.mean(combo_result['New Weight'])),'go-',color='chocolate',label='Diet&Exercise Δ={}'.format(round(-np.mean(combo_pop['Weight'])+np.mean(combo_result['New Weight']),4)))
        plt.legend(loc='best')
        plt.title(('Average Weight: {} Months Before vs. After').format(mon))
        plt.xlabel('Month(s)')
        plt.ylabel('Weight (lb)')
        l = np.arange(mon+1)
        x = ['Month {}'.format(i) for i in range(mon+1)]
        plt.xticks(l,x)
        plt.show()
        
        plt.hist(diet_result['Weight Change'],color='steelblue',label = 'Only Diet',alpha = 0.5)
        plt.hist(combo_result['Weight Change'],color='chocolate',label = 'Diet&Exercise',alpha = 0.5)
        plt.title('Weight Change Distribution')
        plt.xlabel('Weight Change (lb)')
        plt.ylabel('Frequency')
        plt.legend(loc='best')
        plt.show()
        print('There are {} of male students chose to gain weight during the past {} months. There are {} of them chose to gain weight by only dieting, and they gained {} lb on average; there are {} of them chose to combine dieting and exercsing and they gained {} lb on average.'.format(len(male_reset),mon,len(diet_pop),round(-np.mean(diet_pop['Weight'])+np.mean(diet_result['New Weight']),4),len(combo_pop),round(-np.mean(combo_pop['Weight'])+np.mean(combo_result['New Weight']),4)))
    
    result = pd.concat([male_reset,result],axis =1)
    return result


# # To use the program, simply run the following cell, and follow the instruction

# In[27]:

print(
    "Hi there, welcome to the UIUC student body weight simulation! This program will simulation a certain size of UIUC students who want to lose, gain, or maintain their weight over a period of time. I will ask you a few questions to customize the program and will show you how their body weight change. Thank you for your interaction!")

# population inputs: population size, number of months
pop_size = input(
    'How large would you like the population to be? (Please enter an integer greater than one, e.g. 1000.)   : ')
if pop_size.isdigit():
    pop_size = int(pop_size)
    pop_size
else:
    print('Please input a valid integer that is greater than 1')

mon = input('How many months wuold you like to simulate? (Please enter an integer greater than zero, e.g. 1)   : ')
if mon.isdigit():
    mon = int(mon)
    mon
else:
    print('Please input a valid integer that is greater than 0')

pop = population(pop_size, male=m, female=f)
#  0          1           2           3           4        5          6   
# male_pop, female_pop, male_lw, male_maintain,male_gw, female_lw, female_maintain
print('Great! I have simulated {} students, and among them {} are females, {} are males'.format(pop_size, pop[-1],
                                                                                                pop[-2]))

# ------------------------------------------------------------------------------------------------------------------------
# Results inputs: gender, goals
while True:
    f_or_m = input(
        'Would you want to see the results of female or male? (Please enter "F" for female or "M" for male)   : ')
    if f_or_m.lower() == "f":
        while True:
            goal = input(
                'Would you want to see the results of women who have lost weight or maintained their weight? (Please enter "L" for lose weight, "M" for maintain)  ')
            if goal.lower() != "l" and goal.lower() != "m":
                print('\n Please enter "L" for lose weight or "M" for maintain weight')
            else:
                break
        break
    elif f_or_m.lower() == "m":
        while True:
            goal = input(
                'Would you want to see the results of men who have lost, gained or maintained their weight?  (Please enter "L" for lose weight, "G" for gain weight, M" for maintain)  ')
            if goal.lower() != "l" and goal.lower() != "m" and goal.lower() != "g":
                print('\n Please enter "L" for lose weight, "M" for maintain weight, or "G" for gain weight')
            else:
                break
        break
    else:
        print('\n Please enter "M" for men or "F" for women')

# ----------------------------------------------------------------------------------------------------------------------
# Generating results
if f_or_m.lower() == "f" and goal.lower() == "l":
    f_lw = pop[5]
    result = female_monthly(f_lw, 'Lose Weight', mon)
    print('\n Here is the fist five rows of this subset of students')
    print(result.head())
elif f_or_m.lower() == "f" and goal.lower() == "m":
    f_m = pop[6]
    result = female_monthly(f_m, 'Maintain', mon)
    print('\n Here is the fist five rows of this subset of students')
    print(result.head())
elif f_or_m.lower() == "m" and goal.lower() == "l":
    m_lw = pop[2]
    result = male_monthly(m_lw, 'Lose Weight', mon)
    print('\n Here is the fist five rows of this subset of students')
    print(result.head())
elif f_or_m.lower() == "m" and goal.lower() == "g":
    m_gw = pop[4]
    result = male_monthly(m_gw, 'Gain Weight', mon)
    print('\n Here is the fist five rows of this subset of students')
    print(result.head())
elif f_or_m.lower() == "m" and goal.lower() == "m":
    m_m = pop[3]
    result = male_monthly(m_m, 'Maintain', mon)
    print('\n Here is the fist five rows of this subset of students')
    print(result.head())

# ----------------------------------------------------------------------------------------------------------------------
# Ask the user if they want to quit or to see another result
while True:
    user_input = input(
        'Would you like to see another subset of students or quit? (Please enter "Y" to see results for results of other students and "Q" to quit. If you want to re-simulate the whole popuation, please quit and restart the program.)  ')
    # if user wants to quit
    if user_input.lower() == "Q".lower():
        print('\n Thank you for using the program! Bye!')
        break
    # if user mis-types
    elif user_input.lower() != "Y".lower():
        print('\n Please enter "Y" to continue or "Q" to quit!')
    # if user wants to see another result
    elif user_input.lower() == "Y".lower():
        while True:
            f_or_m = input(
                'Would you want to see the results of female or male? (Please enter "F" for female or "M" for male)   : ')
            if f_or_m.lower() == "f":
                while True:
                    goal = input(
                        'Would you want to see the results of women who have lost weight or maintained their weight? (Please enter "L" for lose weight, "M" for maintain)  ')
                    if goal.lower() != "l" and goal.lower() != "m":
                        print('\n Please enter "L" for lose weight or "M" for maintain weight')
                    else:
                        break
                break
            elif f_or_m.lower() == "m":
                while True:
                    goal = input(
                        'Would you want to see the results of men who have lost, gained or maintained their weight?  (Please enter "L" for lose weight, "G" for gain weight, M" for maintain)  ')
                    if goal.lower() != "l" and goal.lower() != "m" and goal.lower() != "g":
                        print('\n Please enter "L" for lose weight, "M" for maintain weight, or "G" for gain weight')
                    else:
                        break
                break
            else:
                print('\n Please enter "M" for men or "F" for women')
        # generating a new result
        if f_or_m.lower() == "f" and goal.lower() == "l":
            f_lw = pop[5]
            result = female_monthly(f_lw, 'Lose Weight', mon)
            print('\n Here is the fist five rows of this subset of students')
            print(result.head())
        elif f_or_m.lower() == "f" and goal.lower() == "m":
            f_m = pop[6]
            result = female_monthly(f_m, 'Maintain', mon)
            print('\n Here is the fist five rows of this subset of students')
            print(result.head())
        elif f_or_m.lower() == "m" and goal.lower() == "l":
            m_lw = pop[2]
            result = male_monthly(m_lw, 'Lose Weight', mon)
            print('\n Here is the fist five rows of this subset of students')
            print(result.head())
        elif f_or_m.lower() == "m" and goal.lower() == "g":
            m_gw = pop[4]
            result = male_monthly(m_gw, 'Gain Weight', mon)
            print('\n Here is the fist five rows of this subset of students')
            print(result.head())
        elif f_or_m.lower() == "m" and goal.lower() == "m":
            m_m = pop[3]
            result = male_monthly(m_m, 'Maintain', mon)
            print('\n Here is the fist five rows of this subset of students')
            print(result.head())

if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True,optionflags=doctest.ELLIPSIS)



