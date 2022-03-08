import docplex.mp.model as cpx
import itertools
#import pandas
import random
import pandas as pd



# imput parameters
T = 10
P = 12 #max number of players in dataset
set_T = range(1, T+1)   # i in set T
set_P = range(1, P+1)   # j in set P


## Import data
values= {1:[112 for i in range(P)], 2:[116 for i in range(P)], 3:[172 for i in range(P)], 4:[192 for i in range(P)],
5:[116 for i in range(P)], 6:[113 for i in range(P)], 7:[192 for i in range(P)], 8:[142 for i in range(P)], 
9:[110 for i in range(P)], 10:[115 for i in range(P)], 11:[152 for i in range(P)], 12:[132 for i in range(P)]} #some sort of  dict of player value projections...where key is player ID in dataset
salaries= {1:[11.2 for i in range(P)], 2:[11.6 for i in range(P)], 3:[17.2 for i in range(P)], 4:[19.2 for i in range(P)],
5:[11.6 for i in range(P)], 6:[11.3 for i in range(P)], 7:[19.2 for i in range(P)], 8:[14.2 for i in range(P)], 
9:[11.0 for i in range(P)], 10:[11.5 for i in range(P)], 11:[15.2 for i in range(P)], 12:[13.2 for i in range(P)]} #some sort of dict of player value projections...where key is player ID in dataset
discount_rate = [0.03 for i in range(T)] #discount rate wrt time
Rarita_nationality = [1 for i in range(P)] #indicating wheather playeris raritan national ...wrt player ID indexing
age = [random.randint(17, 40) for i in range(P)]
position = {1:"GK", 2:"GK", 3:"FW", 4:"MF",
5:"MF", 6:"DF", 7:"DF", 8:"MF", 
9:"DF", 10:"DF", 11:"MF", 12:"FW"}


V = {(i,j): values[i][j-1] for i in set_T for j in set_P}
W = {(i,j): salaries[i][j-1] for i in set_T for j in set_P}
O = {(i,j): salaries[i][j-1] * 0.1 for i in set_T for j in set_P} #fee received when lending
I = {(i,j): salaries[i][j-1] * 0.1 for i in set_T for j in set_P} #fee paid to borrow
rho = {i: discount_rate[i-1] for i in set_T}
Y_p = {j: Rarita_nationality[j-1] for j in set_P}
A_pt = {(i,j): (age[j-1] + i) for i in set_T for j in set_P}



## Import data
"""values= {1:[112 for i in range(T)], 2:[116 for i in range(T)], 3:[172 for i in range(T)], 4:[192 for i in range(T)],
5:[116 for i in range(T)], 6:[113 for i in range(T)], 7:[192 for i in range(T)], 8:[142 for i in range(T)], 
9:[110 for i in range(T)], 10:[115 for i in range(T)], 11:[152 for i in range(T)], 12:[132 for i in range(T)]} #some sort of  dict of player value projections...where key is player ID in dataset
salaries= {1:[11.2 for i in range(T)], 2:[11.6 for i in range(T)], 3:[17.2 for i in range(T)], 4:[19.2 for i in range(T)],
5:[11.6 for i in range(T)], 6:[11.3 for i in range(T)], 7:[19.2 for i in range(T)], 8:[14.2 for i in range(T)], 
9:[11.0 for i in range(T)], 10:[11.5 for i in range(T)], 11:[15.2 for i in range(T)], 12:[13.2 for i in range(T)]} #some sort of dict of player value projections...where key is player ID in dataset
discount_rate = [0.03 for i in range(T)] #discount rate wrt time
Rarita_nationality = [1 for i in range(T)] #indicating wheather playeris raritan national ...wrt player ID indexing
age = [random.randint(17, 40) for i in range(T)]"""




# set of possible player positions 
R = ['GK', 'DF', 'MF', 'FW']
# max # of player in a team 
N_bar = 11
# max GKs
N_GK = 1
# max DFs
N_DF = 4
# max MFs
N_MF = 4
# max FWs
N_FW = 2
# retiring age
A_bar = 40


## Forecasted Revenue figures (times 1...10)
R_0 = 995000000 #doobloons
C_0 = 150000000 # doubloons
R = [R_0 + R_0*0.05 for i in set_T]
## Forecasted Cost figures (times 1...10)
C = [C_0 + C_0*0.05 for i in set_T]
# Budget
B = {i: R[i-1] -C[i-1] for i in set_T}






## model set up
opt_model = cpx.Model(name="Rarita Football Team Composition")





# decision variables

#bool for lending of p at time t
lO_pt = {(i,j): opt_model.binary_var(name="lO_{0}_{1}".format(i,j)) for i in set_T for j in set_P} 
#bool for borrowing of p at time t
lI_pt = {(i,j): opt_model.binary_var(name="lI_{0}_{1}".format(i,j)) for i in set_T for j in set_P} 
#bool for belonging of p at time t to the team
y_pt = {(i,j): opt_model.binary_var(name="ypt_{0}_{1}".format(i,j)) for i in set_T for j in set_P} 



# contraints

# the Raritan players are always owned time 1 contraint(not necessary constraint)
for j in set_P:
    opt_model.add_constraint(Y_p[j] == y_pt[1,j]) 

#team composition constraints
"""opt_model.add_constraint(N_GK == 2)
opt_model.add_constraint(N_DF >= 8)
opt_model.add_constraint(N_DF <= 10)
opt_model.add_constraint(N_MF >= 8)
opt_model.add_constraint(N_MF <= 10)
opt_model.add_constraint(N_FW >= 3)
opt_model.add_constraint(N_FW <= 4)"""

# Max number of players in a team will always be less that N_bar
constraints2 = {j : opt_model.add_constraint(ct=opt_model.sum(y_pt[i,j] for i in set_T) <= N_bar,
ctname="constraint_{0}".format(j)) for j in set_P}

# number of players at the club, borrowed and lent out are always equal to N_bar
constraints3 = {j : opt_model.add_constraint(sum(y_pt[i,j] + lO_pt[i,j] - lI_pt[i,j] for i in set_T) <= N_bar, 
ctname="constraint_{0}".format(j)) for j in set_P}

# only borrow if player is not owned
for i in set_T:
    for j in set_P:
        opt_model.add_constraint(y_pt[i,j] - lO_pt[i,j] >= 0)

# only lent if palyer is owned:
for i in set_T:
    for j in set_P:
        opt_model.add_constraint(y_pt[i,j] + lI_pt[i,j] <= 0)

# no players are considered above A_bar -------------not perfect constrint
"""opt_model.add_constraint(A_pt[i,j] <= A_bar) """

#budget constraint
constraints3 = {j : opt_model.add_constraint(ct=opt_model.sum((I[i,j]*lI_pt[i,j] - O[i,j]*lO_pt[i,j]) for j in set_P) <= B[i],
ctname="constraint_{0}".format(i))for i in set_T}

#sunset value
# S_T = sum(V[T,j] * y_pt[T,j] for j in set_P)

# sunset value greater than 0
opt_model.add_constraint(sum(V[T,j] * y_pt[T,j] for j in set_P) >= 0)




# objective
objective = opt_model.maximize((1/((1+rho[i])**(i-1)) * V[i,j] * y_pt[i,j] + O[i,j] * lO_pt[i,j] - I[i,j] * lI_pt[i,j] 
- W[i,j] * (y_pt[i,j] + lI_pt[i,j] - lO_pt[i,j])) + 1/((1+rho[T])**(T-1)) * V[T,j])

# solving
sol = opt_model.solve()
opt_model.print_solution()

opt_df = pd.DataFrame.from_dict(y_pt, orient="index", columns = ["variable_object"])
opt_df.index =  pd.MultiIndex.from_tuples(opt_df.index, names=["column_i", "column_j"])
opt_df.reset_index(inplace=True)
opt_df["solution_value"] = opt_df["variable_object"].apply(lambda item: item.solution_value)

opt_df.drop(columns=["variable_object"], inplace=True)
opt_df.to_csv("./optimization_solution.csv")