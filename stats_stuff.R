options(max.print=1000000)
referees <- read.csv("Referees.csv")
referees[,1:78] <- lapply(referees[, 1:78], function(x) as.logical(x))
referees$Total.Fouls <- referees$Home.Team.Fouls + referees$Away.Team.Fouls
referees$Bias <- referees$Home.Team.Fouls < referees$Away.Team.Fouls

make_linear_model <- function(){
  xnam <- paste("`X",1:77,"`", sep="")
  formula_str <- paste(lapply(xnam, function(x) paste(x,xnam, sep="*", collapse="+")), collapse = "+")
  plzwrk <- as.formula(paste("`Home.Team.Fouls` ~", formula_str))
  plzwrk
  
  linear_mod <- lm(data=referees,formula=plzwrk)
  return(linear_mod)
}
lm_mod_hf<-make_linear_model()
summary(lm_mod_hf)

make_linear_model2 <- function(){
  xnam <- paste("`X",1:77,"`", sep="")
  formula_str <- paste(lapply(xnam, function(x) paste(x,xnam, sep="*", collapse="+")), collapse = "+")
  plzwrk <- as.formula(paste("`Away.Team.Fouls` ~", formula_str))
  plzwrk
  
  linear_mod <- lm(data=referees,formula=plzwrk)
  return(linear_mod)
}
lm_mod_af<-make_linear_model2()
summary(lm_mod_af)

make_linear_model3<- function(){
  xnam <- paste("`X",1:77,"`", sep="")
  formula_str <- paste(lapply(xnam, function(x) paste(x,xnam, sep="*", collapse="+")), collapse = "+")
  plzwrk <- as.formula(paste("`Total.Fouls` ~", formula_str))
  plzwrk
  
  linear_mod <- lm(data=referees,formula=plzwrk)
  return(linear_mod)
}
lm_mod_tf<-make_linear_model3()
summary(lm_mod_tf)
anova(lm_mod_tf)

library(ggplot2)
ggplot(bias,aes(y = bias,x = seasons)) + geom_point() + 
  geom_smooth(method="lm",formula = y~x, se=F) +
  labs(x = "season", y = "bias",title="Scatterplot: Seasons for ref vs. Bias")
mod1 <- lm(players$Points~players$Assists+players$Rebounds+players$Assists+players$Blocks)
summary(mod1)
ggplot(bias,aes(y = fouls_home,x = seasons)) + geom_point() + 
  geom_smooth(method="lm",formula = y~x, se=F) +
  labs(title="Scatterplot:")
ggplot(bias,aes(x = seasons,y = fouls_away)) + geom_point() + 
  geom_smooth(method="lm",formula = y~x, se=F) +
  labs(title="Scatterplot:")

summary(lm(bias$fouls_away~bias$bias))


mod1 <- lm(players$Points~players$Assists+players$Won+players$FTA+players$FTM+players$Seconds_Played)
summary(mod1)
aov(mod1)
anova(mod1)

#referees[] <- lapply(referees, function(x) as.logical(x))
mod <- lm(bias$bias~bias$seasons)
summary(mod)
library(ggplot2)
ggplot(bias,aes(y = bias,x = seasons)) + geom_point() + 
  geom_smooth(method="lm",formula = y~x, se=F) +
  labs(x = "season", y = "bias",title="Scatterplot: Seasons for ref vs. Bias")
mod1 <- lm(players$Points~players$Assists+players$Rebounds+players$Assists+players$Blocks)
summary(mod1)
ggplot(bias,aes(y = fouls_home,x = seasons)) + geom_point() + 
  geom_smooth(method="lm",formula = y~x, se=F) +
  labs(title="Scatterplot:")
ggplot(bias,aes(x = seasons,y = fouls_away)) + geom_point() + 
  geom_smooth(method="lm",formula = y~x, se=F) +
  labs(title="Scatterplot:")

summary(lm(bias$fouls_away~bias$bias))


mod1 <- lm(players$Points~players$Assists+players$FTM+players$Seconds_Played)
summary(mod1)
aov(mod1)
anova(mod1)

ggplot(bias,aes(x = X3,y = X6)) + geom_point() + 
  geom_smooth(method="lm",formula = y~x, se=F) +
  labs(title="Scatterplot:")
ggplot(bias,aes(x = X3,y = X7)) + geom_point() + 
  geom_smooth(method="lm",formula = y~x, se=F) +
  labs(title="Scatterplot:")

ggplot(bias,aes(x = bias$`Years Experience`,y = bias$`me Adjusted Fouls`)) + geom_point() + 
  geom_smooth(method="lm",formula = y~x, se=F) +
  labs(title="Scatterplot:")
ggplot(bias,aes(x = bias$`Years Experience`,y = bias$`ay Adjusted Foul`)) + geom_point() + 
  geom_smooth(method="lm",formula = y~x, se=F) +
  labs(title="Scatterplot:")
summary(lm(bias$`ay Adjusted Foul`~bias$`Years Experience`))

modfs <- lm(players$Points~players$FTA+players$Seconds_Played)
summary(modfs)
anova(modfs)
