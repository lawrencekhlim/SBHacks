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


mod1 <- lm(players$Points~players$Assists+players$Won+players$FTA+players$FTM+players$Seconds_Played)
summary(mod1)
aov(mod1)
anova(mod1)
