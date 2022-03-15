data = read.csv('./rarita-football-club/code-market-value/player.csv',stringsAsFactors=T)
data = data[-1]
data = data[-1]

str(data)
summary(data)

hist(data$mv)
fitdistrplus::descdist(data$mv, boot = 1000)

glm1 <- glm(Salary ~ Age +I(Age^2) +Salary.2020, data = data, family = Gamma(link="log"))
plot(fitted.values(glm1), residuals(glm1, type = "deviance") )
plot(fitted.values(glm1), glm1$y)
abline(0,1)

summary(glm1)

