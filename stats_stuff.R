#options(max.print=1000000)
library('ggplot2')
library('forcats')
library('reshape2')

create_data <- function(file_path){
  referees <- read.csv(file_path)
  referees[,1:108] <- lapply(referees[, 1:108], function(x) as.logical(x))
  referees$Total.Fouls <- referees$Home.Team.Fouls + referees$Away.Team.Fouls
  referees$Bias <- referees$Home.Team.Fouls < referees$Away.Team.Fouls
  
  return(referees)
}


make_linear_model <- function(data){
  if(missing(data)){
    referees <- create_data('Referees2015.csv')
  }
  else{
    referees <- data
  }
  xnam <- paste("`X",1:77,"`", sep="")
  formula_str <- paste(lapply(xnam, function(x) paste(x,xnam, sep="*", collapse="+")), collapse = "+")
  plzwrk <- as.formula(paste("`Total.Fouls` ~", formula_str))
  
  linear_mod <- lm(data=referees,formula=plzwrk)
  return(linear_mod)
}


fouls <- read.csv('normalizedHomeFouls.csv')

averages <- fouls[1,1:5]
fouls <- fouls[2:nrow(fouls),1:5]

colnames(fouls) <- c('Referee', 'Average.Home', 'Average.Away', 'Individual.Home', 'Individual.Away')
#  fouls <- fouls[fouls$Fouls_Called > 1,]

average_fouls <- fouls[,1:3]
average_fouls <- melt(average_fouls)

average_foul_plot <- ggplot(data = average_fouls,aes(x=reorder(Referee, -value), y=value, fill=variable)) +
  geom_col(width=0.6, position = position_dodge(width = 0.7))+
  scale_fill_manual(breaks = c("Home", "Away"), values = c("grey50", "tomato3"))+
  labs(x="Referee", y="Fouls Called", title="Average Foul Calls Per Referee", fill="Team")+
  theme(axis.text.x = element_text(angle=90))
average_foul_plot


png("img/AverageFouls.png", width=1000, height=400)
plot(average_foul_plot)
dev.off()


levels(fouls$Team) <- reorder(fouls$Team, -fouls$Fouls)




fouls <- melt(fouls)
head(fouls[2:nrow(fouls),1:3])

#reorder(Referee, -Home.Fouls)

foul_plot <- ggplot(data = fouls,aes(x=reorder(Referee, -value), y=value, fill=variable)) +
  geom_col(position="dodge")+
  scale_fill_manual(breaks = c("Home", "Away"), values = c("grey40", "red4"))+
  labs(x="Referee", y="Fouls Called", title="How Many Fouls Each Referee Calls in the NBA", fill="Team")+
  theme(axis.text.x = element_text(angle=90))
foul_plot













#ref2015 <- create_data('Referees2015.csv')
#ref2015$isTrain <- runif(nrow(ref2015)) < 0.75

#train <- ref2015[ref2015$isTrain,]
#test <- ref2015[!ref2015$isTrain,]

lm = make_linear_model()
ref2016 <- create_data('Referees2016.csv')
#ref2017 <- create_data('Referees.csv')


predictions <- predict(lm, ref2016)
residuals <- ref2016$Total.Fouls - predictions
mean(residuals)

summary(predictions)



mean(abs(referees$Total.Fouls - mean(referees$Total.Fouls)))















#Not Yash's
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

library(readr)
techfouls2015 <- read_csv("techfouls2015.csv", col_names = FALSE, col_types = cols(X1 = col_factor(levels = c("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "60", "61", "62", "63", "64", "65", "66", "67", "68", "69", "70", "71", "72", "73", "74", "75", "76", "77"))))
atlantic <- c('Celtics','Raptors','76ers','Knicks','Nets')
central <- c('Cavaliers','Pacers','Bucks','Pistons','Bulls')
southeast <- c('Heat','Wizards','Hornets','Hawks','Magic')
northwest <- c('Timberwolves','Thunder','Trail Blazers','Nuggets','Jazz')
pacific <- c('Warriors','Clippers','Suns','Lakers','Kings')
southwest <- c('Rockets','Spurs','Pelicans','Grizzlies','Mavericks')


techfouls2015 <- techfouls2015[order(techfouls2015$X2,techfouls2015$X1),]
View(techfouls2015)
ggplot(techfouls2015[techfouls2015$X3 %in% atlantic,], aes(x=X1,y=X2,fill=reorder(X3, -X2))) +  geom_col()
ggplot(techfouls2015[techfouls2015$X3 %in% central,], aes(x=X1,y=X2,fill=reorder(X3, -X2))) +  geom_col()
ggplot(techfouls2015[techfouls2015$X3 %in% southeast,], aes(x=X1,y=X2,fill=reorder(X3, -X2))) +  geom_col()
ggplot(techfouls2015[techfouls2015$X3 %in% northwest,], aes(x=X1,y=X2,fill=reorder(X3, -X2))) +  geom_col()
ggplot(techfouls2015[techfouls2015$X3 %in% pacific,], aes(x=X1,y=X2,fill=reorder(X3, -X2))) +  geom_col()
ggplot(techfouls2015[techfouls2015$X3 %in% southwest,], aes(x=X1,y=X2,fill=reorder(X3, -X2))) +  geom_col()

