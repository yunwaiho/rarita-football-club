import numpy as np
import pandas as pd
import random



# initializing fixed variables

# set of players (all players in the database) - list of distinct IDs
P = [1, 2, ...]
# list of MTWs
T = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# set of possible player positions 
R = ['GK', 'DF', 'MF', 'FW']
# max # of player in a team 
N_bar = 25
# max GKs
N_GK = 2
# max DFs
N_DF = 9
# max MFs
N_MF = 9
# max FWs
N_FW = 3
# retiring age
A_bar = 40



# Variables for us to build from our assumptions and knowladge

## Forecasted Revenue figures (times 1...10)
R = []
## Forecasted Cost figures (times 1...10)
C = []
## discount rates for the time period (need to calculate from spot rates)
rho = []
## Build a dataframe with boolean variables containing lending strategies 
## of existing Rarita players (manual strategy building for each young Rarita talents)
K_lending_startegies_df = []
## Build a dataframe with boolean variables containing borrowing strategies 
## of existing foreign players (manual strategy building for each young Rarita talents)
K_borrowing_startegies_df = []




# data needed from the case data
# player ID, Nationality, Age, Market Value, Wage,

### this is just a practice example!!!
df = pd.read_excel (r'C:\Users\Eszter\OneDrive - The University of Melbourne\Documents\0Eszter mappa\unimelb 2022 sem 1\SOA Case study\Player salaries projections.xlsx', sheet_name='Try out sheet')
#df.head()
#df.info()



# boolean variables to be generated for the model's purposes 
# these should be generated for each player, for the whole timeframe, for each sample senario
y_p = [] #indicates whether player belongs to the team or not
lo_p_t =[] #indicates if player is lent to an other team or not for period t
li_p_t = []#indicates if player is borrowed for the period t or not




def Raritan_indicator_generator(x):
    if x == 'Rarita':
        return 1
    else:
        return 0



def lending_bool_generator(x):
    if x == 1:
        return int(random.choice([True, False]))
    else:
        return 0




def borrowing_bool_generator(x):
    if x == 0:
        return int(random.choice([True, False]))
    else:
        return 0




df["Raritan bool indicator"] = df["Country"].apply(Raritan_indicator_generator)


for i in T:
    df["Player lent out for TMW " + str(i)] = df["Raritan bool indicator"].apply(lending_bool_generator)
    df["Player borrowed for TMW " + str(i)] = df["Raritan bool indicator"].apply(borrowing_bool_generator)

print(sum(df["Raritan bool indicator"]))
print(sum(df["Player lent out for TMW 1"]))
print(sum(df["Player borrowed for TMW 5"]))
print(df.head(10))

