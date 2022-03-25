rm(list=ls())
# Probability distribution of growth rates when hosting is introduced
library(purrr)
set.seed(110)


n_sims = 1e3
year = 10
g_h = 0.05
inflation1 = seq(0.01, 0.04, by = 0.005)
growth_rate1 <- inflation1 + 0.004
sens_values <- data.frame(matrix(ncol=10, nrow = length(growth_rate1)))
colnames(sens_values) <- c('year_1', 'year_2', 'year_3','year_4','year_5','year_6','year_7', 'year_8','year_9','year_10')
count = 1


for (i in growth_rate1) {
  years = matrix(1:year, nrow = n_sims, ncol = year, byrow = T)
  # 1/5 of hosting in either year 6,7,8,9,or 10
  hosting_year = matrix(floor(rgeom(n_sims, 0.2)+6), nrow = n_sims, ncol = year)
  growth_matrix = ifelse(years < hosting_year, 0, g_h)
  
  discount_matrix <- growth_matrix + (1+i)
  accumulation_matrix <- t(apply(discount_matrix, 1, cumprod))
  final_1 <- data.frame(accumulation_matrix)
  names(final_1) <- c('year_1', 'year_2', 'year_3','year_4','year_5','year_6','year_7', 'year_8','year_9','year_10')
  trial_mean <- colMeans(final_1)
  sens_values[count, ] <- trial_mean
  count = count + 1
}

#present value GDP per capita ranges
disc <- 5:10
GDPpc <- sens_values$year_10 *(1+i)^(-5)*(1+0.02)^(-5) 
GDP_proj <- sens_values[1, ]*(1+0.02)^(-disc) 
