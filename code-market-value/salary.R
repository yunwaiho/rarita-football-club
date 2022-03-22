player = read.csv('./rarita-football-club/data/player-data/player_salary.csv',stringsAsFactors=F)

# change positions to factors
player[, c(9,6,7,8)] = lapply(player[, c(6,7,8,9)], factor)
# project salary growth rate rather than salary
# player$Salary = player$Salary/player$Salary.2020

str(player)
summary(player)

glm1 <- glm(Salary ~Age-Player -Squad, data = player, family = Gamma(link="log"))
#plot(fitted.values(glm1), residuals(glm1, type = "deviance") )
#plot(fitted.values(glm1), glm1$y)
#abline(0,1)

# From the results, it seems like age doesn't really affect growth rate,
# so we are going to assume constant growth rate for salary 
# (this also will include a constant assumption of inflation rate)

# We have also tried fitting actual salary, log(salary), sqrt(salary) but 
# they all predicted unreasonable values (such as infinity)
summary(glm1)

##############

salaryGrowth = read.csv('./rarita-football-club/data/player-data/salary_growth.csv',stringsAsFactors=F)

salaryGrowth
results = data.frame(player$Player, player$Squad, player$Salary) 
results
names(results) = c('Player', 'Squad', 'Salary.2021')

# code for predict 10 year salary with models

# playerFuture = player
# playerFuture$Salary.2020 = playerFuture$Salary
# playerFuture = playerFuture[, -4]
# playerFuture
# for (i in 1:10) {
#   playerFuture$Age = playerFuture$Age + 1
#   newSalary = exp(predict(glm1, playerFuture))
#   newSalary[playerFuture$Age >= 42] = 0
#   playerFuture$Salary.2020 = newSalary
#   newSalary =newSalary*results[,2+i]
#   results = cbind(results, newSalary)
#   names(results)[names(results) == 'newSalary'] = paste('Salary',as.character(2021+i))
#   results
# }
# 
# results[,-c(1,2)]

# code for predicting 10 yr salary with constant growth assumption


for (i in 1:10) {
  player$Age = player$Age + 1
  
  age = player$Age + 1 - 16
  salaryGrowth[1, 2]
  
  newSalary = player$Salary * salaryGrowth[age, 2]
  results = cbind(results, newSalary)
  names(results)[names(results) == 'newSalary'] = paste('Salary',as.character(2021+i))
  results
}
results
# rounding to 2dp
results[, -c(1,2)] = lapply(results[, -c(1,2)], round, 2)
write.csv(results, "playersalary.csv", quote = F)

