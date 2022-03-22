from docplex.mp.model import Model

capacities = {1: 15, 2: 20}
demands = {3: 7, 4: 10, 5: 15}
costs = {(1,3): 2, (1,5):4, (2,4):5, (2,5):3}

# Python ranges will be used to iterate on source, target nodes.
source = range(1, 3) # {1, 2}
target = range(3, 6) # {3,4,5}





tm = Model(name='transportation')



# create flow variables for each couple of nodes
# x(i,j) is the flow going out of node i to node j
x = {(i,j): tm.continuous_var(name='x_{0}_{1}'.format(i,j)) for i in source for j in target}

# each arc comes with a cost. Minimize all costed flows
tm.minimize(tm.sum(x[i,j]*costs.get((i,j), 0) for i in source for j in target))

tm.print_information()



# for each node, total outgoing flow must be smaller than available quantity
for i in source:
    tm.add_constraint(tm.sum(x[i,j] for j in target) <= capacities[i])
    
# for each target node, total ingoing flow must be greater thand demand
for j in target:
    tm.add_constraint(tm.sum(x[i,j] for i in source) >= demands[j])



tm.minimize(tm.sum(x[i,j]*costs.get((i,j), 0)))



tms = tm.solve()
assert tms
tms.display()




im = Model(name='integer_programming')
b = im.binary_var(name='boolean_var')
ijk = im.integer_var(name='int_var')
im.print_information()



lm = Model(name='lp_telephone_production')
desk = lm.continuous_var(name='desk')
cell = lm.continuous_var(name='cell')
# write constraints
# constraint #1: desk production is greater than 100
lm.add_constraint(desk >= 100)

# constraint #2: cell production is greater than 100
lm.add_constraint(cell >= 100)

# constraint #3: assembly time limit
ct_assembly = lm.add_constraint( 0.2 * desk + 0.4 * cell <= 401)

# constraint #4: painting time limit
ct_painting = lm.add_constraint( 0.5 * desk + 0.4 * cell <= 492)
lm.maximize(12.4 * desk + 20.2 * cell)

ls = lm.solve()
lm.print_solution()

im = Model(name='ip_telephone_production')
desk = im.integer_var(name='desk')
cell = im.integer_var(name='cell')
# write constraints
# constraint #1: desk production is greater than 100
im.add_constraint(desk >= 100)

# constraint #2: cell production is greater than 100
im.add_constraint(cell >= 100)

# constraint #3: assembly time limit
im.add_constraint( 0.2 * desk + 0.4 * cell <= 401)

# constraint #4: painting time limit
im.add_constraint( 0.5 * desk + 0.4 * cell <= 492)
im.maximize(12.4 * desk + 20.2 * cell)

si = im.solve()
im.print_solution()