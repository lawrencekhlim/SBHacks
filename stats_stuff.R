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
fouls <- fouls[2:nrow(fouls),]
  
colnames(fouls) <- c('Referee', 'Average.Home', 'Average.Away', 'Individual.Home', 'Individual.Away', 'Average.Differences')
#  fouls <- fouls[fouls$Fouls_Called > 1,]
  


make_foul_plot <- function(fouls, title_text, colors){
  if(missing(colors)){
    home_color <- "black"
    away_color <- "red"
  }
  else{
    home_color <- colors[1]
    away_color <- colors[2]
  }
  
  
  plot_data <- melt(fouls)
  team_type <- as.character(unique(plot_data$variable))
  
  foul_plot <- ggplot(data = plot_data,aes(x=reorder(Referee, -value), y=value, color=variable)) +
    geom_point()+
    scale_color_manual(breaks = c(team_type[1], team_type[2]), values = c(home_color, away_color))+
    labs(x="Referee", y="Fouls Called", title=title_text, color="Type")+
    theme(axis.text.x = element_text(angle=90))
  
  return(foul_plot)
}


make_average_foul_plot <- function(){
  
  average_fouls <- fouls[,1:3]
  average_foul_plot <- make_foul_plot(average_fouls, "Average Foul Calls While Referee Active")
  
  average_foul_plot <- average_foul_plot +
    annotate("segment", y=averages[[2]], yend=averages[[2]],x='Zach Zarba', xend='Ron Garretson', color=home_color)+ #home average
    annotate("text", x='Curtis Blair', y=averages[[2]]-0.3, label="Average Foul Calls for Home",color=home_color, fontface=2)+
    annotate("segment", y=averages[[3]], yend=averages[[3]],x='Zach Zarba', xend='Ron Garretson', color=away_color)+ #away average
    annotate("text", x='Dedric Taylor', y=averages[[3]]+0.3, label="Average Foul Calls for Away", color=away_color, fontface=2)
  
  return(average_foul_plot)
}

make_individual_foul_plot <- function(){
  
  individual_fouls <- fouls[,c(1,4,5)]
  individual_foul_plot <- make_foul_plot(individual_fouls, "Fouls Called Per Referee")
  
  individual_foul_plot <- individual_foul_plot +
    annotate("segment", y=averages[[4]], yend=averages[[4]],x='Zach Zarba', xend='Ron Garretson', color=home_color)+ #home average
    annotate("text", x='Rodney Mott', y=averages[[4]]-0.3, label="Average Foul Calls for Home",color=home_color, fontface=2)+
    annotate("segment", y=averages[[5]], yend=averages[[5]],x='Zach Zarba', xend='Ron Garretson', color=away_color)+ #away average
    annotate("text", x='Brian Forte', y=averages[[5]]+0.6, label="Average Foul Calls for Away", color=away_color, fontface=2)+
    theme(legend.position = 'none')
  
  return(individual_foul_plot)
}

plot_to_image <- function(file_path, desired_plot){
  png(file_path, width=800, height=400)
  plot(desired_plot)
  dev.off()
}
plot_to_image("img/FoulDifferences.png", make_difference_plots())
plot_to_image("img/AverageFouls.png", make_average_foul_plot())
plot_to_image("img/IndividualFouls.png", make_individual_foul_plot())


make_difference_plots <- function(){
  fouls$Average.Differences <- fouls$Average.Home-fouls$Average.Away
  fouls$Individual.Differences <- fouls$Individual.Home-fouls$Individual.Away
  differences <- fouls[,c(1,6,7)]
  
  difference_plot <- make_foul_plot(differences, "Difference Between Home and Away Fouls", c("orangered2", "blue"))
  
  return(difference_plot)
}




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
techfouls <- read_csv("techfouls2015-2017.csv", col_names = FALSE)
colnames(techfouls)<-c("Ref","TF","Teams")
atlantic <- c('Atlantic','Celtics','Raptors','76ers','Knicks','Nets')
central <- c('central','Cavaliers','Pacers','Bucks','Pistons','Bulls')
southeast <- c('Southeast','Heat','Wizards','Hornets','Hawks','Magic')
northwest <- c('Northwest','Timberwolves','Thunder','Trail Blazers','Nuggets','Jazz')
pacific <- c('Pacific','Warriors','Clippers','Suns','Lakers','Kings')
southwest <- c('Southwest','Rockets','Spurs','Pelicans','Grizzlies','Mavericks')


View(techfouls)

l <- list()
l[[1]] <- atlantic
l[[2]] <- central
l[[3]] <- southeast
l[[4]] <- northwest
l[[5]] <- pacific
l[[6]] <- southwest

lapply(l, function(div){
  #png(paste("img/techfouls-",div[1],".png",sep=""), width=1000, height=400)
  ggplot(techfouls[techfouls$Teams %in% div,], aes(x=Ref,y=TF,fill=Teams)) +  geom_col()+theme(axis.text.x = element_text(angle=90))+labs(x="Referees",y="technical fouls",title=div[1])
  })
wtf <- read_csv("techfouls2015-7.csv",col_names = FALSE)
colnames(wtf)<-c("Ref","TF","Games.Refd","Weighted.TF","Teams")

lapply(l, function(div){
  ggplot(wtf[wtf$Teams %in% div,], aes(x=reorder(Ref,-Weighted.TF),y=Weighted.TF,fill=Teams)) +  geom_col()+theme(axis.text.x = element_text(angle=90))+labs(x="Referees",y="average technical fouls",title=div[1])
})
