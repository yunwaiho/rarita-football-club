library(tidyverse)


rm(list=ls())
player = read.csv('player.csv',stringsAsFactors=T)
salary_2020 = read.csv('salary_2020.csv',stringsAsFactors=T)
salary_2021 = read.csv('salary_2021.csv',stringsAsFactors=T)

joint <- merge(salary_2020, salary_2021, by = c("Player.Name", "Squad", "Country"))
keep <- c("Player.Name","Position.y", "Annualized.Salary.x", "Annualized.Salary.y")
clean.data <- joint[keep]

names(clean.data)[names(clean.data) == "Annualized.Salary.x"] <- "Salary2020"
names(clean.data)[names(clean.data) == "Annualized.Salary.y"] <- "Salary2021"

clean.data$Position.y <- substr(clean.data$Position.y, 1, 2)

final.data <- merge(clean.data, player, by.x = "Player.Name", by.y = "Player")
keep <- c("Player.Name","Position.y", "Salary2020", "Salary2021", "Age")
final.data <- final.data[keep]

my_data <- as_tibble(final.data)
my_data %>% distinct(Player.Name, Position.y, Salary2020, Salary2021, Age, .keep_all = T)
my_data

str(data)
summary(data)

GK_data <- my_data[my_data$Position.y == 'GK',]
GK_data <- my_data[my_data$Position.y == 'FW',]
GK_data <- my_data[my_data$Position.y == 'MF',]
GK_data <- my_data[my_data$Position.y == 'DF',]

glm1 <- glm(Salary2021 ~ Age +I(Age^2) +Salary2020, data = GK_data, family = Gamma(link="log"))
plot(fitted.values(glm1), residuals(glm1, type = "deviance") )
plot(fitted.values(glm1), glm1$y)
abline(0,1)

summary(glm1)

glm2 <- glm(Salary2021 ~ Age +I(Age^2) +Salary2020, data = FW_data, family = Gamma(link="log"))
plot(fitted.values(glm1), residuals(glm1, type = "deviance") )
plot(fitted.values(glm1), glm1$y)
abline(0,1)

summary(glm1)

glm3 <- glm(Salary2021 ~ Age +I(Age^2) +Salary2020, data = MF_data, family = Gamma(link="log"))
plot(fitted.values(glm1), residuals(glm1, type = "deviance") )
plot(fitted.values(glm1), glm1$y)
abline(0,1)

summary(glm1)

glm4 <- glm(Salary2021 ~ Age +I(Age^2) +Salary2020, data = DF_data, family = Gamma(link="log"))
plot(fitted.values(glm1), residuals(glm1, type = "deviance") )
plot(fitted.values(glm1), glm1$y)
abline(0,1)

summary(glm1)

