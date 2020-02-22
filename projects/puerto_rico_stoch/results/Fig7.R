library("ggplot2")
library(dplyr)
library(gridExtra)
library(grid)
library(lubridate)

dir_plots = "C:\\Users\\jab6ft\\PycharmProjects\\temoatools\\examples\\puerto_rico_stoch3\\results"
dir_nocases = "C:\\Users\\jab6ft\\PycharmProjects\\temoatools\\examples\\puerto_rico_stoch3\\results\\2019_12_18_nocases"
dir_cases = "C:\\Users\\jab6ft\\PycharmProjects\\temoatools\\examples\\puerto_rico_stoch3\\results\\2019_12_18_cases"

#===================================================================
# Case-based results
#===================================================================

# Set directory to load data
setwd(dir_cases)

# Load data
df1 <- read.csv("costs_yearly_toPlot.csv")
df2 <- read.csv("emissions_yearly_toPlot.csv")

# Set directory for plotting
setwd(dir_plots)

# Rename scenarios
rename <- c("Business-as-usual"="Business-as-usual",
            "Centralized - Hybrid"="Centralised - hybrid",
            'Centralized - Natural Gas'="Centralised - natural gas",
            'Distributed - Hybrid'="Distributed - hybrid",
            'Distributed - Natural Gas'="Distributed - natural gas",
            'Mixed - Hybrid'='Mixed - hybrid', 
            'All'='All technologies')
df1 <- transform(df1, Scenario = rename[as.character(Scenario)])
df2 <- transform(df2, Scenario = rename[as.character(Scenario)])

# Remove Mixed - hybrid case
df1 <- df1[ which(df1$Scenario!='Mixed - hybrid'),]
df2 <- df2[ which(df2$Scenario!='Mixed - hybrid'),]

# Rename years
rename <- c("2016"="2016-20",
            "2021"="2021-25",
            '2026'="2026-30",
            '2031'="2031-35",
            '2036'="2036-40")
df1 <- transform(df1, Year = rename[as.character(Year)])
df2 <- transform(df2, Year = rename[as.character(Year)])

# Create new subplot labels - prob_type
rename <- c("Historical"="'Historical storm frequency'",
            "Climate Change"="'Increased storm frequency'")
df1 <- transform(df1, prob_type = rename[as.character(prob_type)])
df2 <- transform(df2, prob_type = rename[as.character(prob_type)])

# Create new subplot labels - carbon_tax
rename <- c("No Tax"="'No tax'",
            "Tax"="'US$'~100~t^-1~CO[2]")
df1 <- transform(df1, carbon_tax = rename[as.character(carbon_tax)])
df2 <- transform(df2, carbon_tax = rename[as.character(carbon_tax)])

# Create new subplot labels - infra
rename <- c("Current"="Overhead power lines",
            'Hardened'="Buried power lines",
            'All'="Overhead power lines")
df1 <- transform(df1, infra = rename[as.character(infra)])
df2 <- transform(df2, infra = rename[as.character(infra)])

# Reorder infra
levels <- c("Overhead power lines", 
            "Buried power lines")
df1$infra <- factor(df1$infra, levels = levels)
df2$infra <- factor(df2$infra, levels = levels)

# Reorder prob_type
levels <- c("'Historical storm frequency'", 
            "'Increased storm frequency'")
df1$prob_type <- factor(df1$prob_type,levels = levels)
df2$prob_type <- factor(df2$prob_type,levels = levels)

# Rename Scenario column
names(df1)[names(df1) == 'Scenario'] <- 'Case'
names(df2)[names(df2) == 'Scenario'] <- 'Case'

# Slice dataframe for to separate based on infra
df1a <- df1[ which(df1$infra=='Overhead power lines'),]
df2a <- df2[ which(df2$infra=='Overhead power lines'),]

df1b <- df1[ which(df1$infra=='Buried power lines'),]
df2b <- df2[ which(df2$infra=='Buried power lines'),]

# The palette with black: http://www.cookbook-r.com/Graphs/Colors_(ggplot2)/
# cbPalette <- c("#E69F00", "#000000", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7") # Full palette
cbPalette <- c("#E69F00", "#000000",  "#009E73", "#0072B2", "#D55E00", "#CC79A7") # Selected colors

# Summarise to create line plots
df_smry1 <- df1a %>% # the names of the new data frame and the data frame to be summarised
  group_by(.dots=c("prob_type", "carbon_tax","Case", "Year")) %>%   # the grouping variable
  summarise(mean = mean(Value),  # calculates the mean
            min = min(Value), # calculates the minimum
            max = max(Value),# calculates the maximum
            sd=sd(Value)) # calculates the standard deviation

df_smry2 <- df2a %>% 
  group_by(.dots=c("prob_type", "carbon_tax","Case", "Year")) %>%  
  summarise(mean = mean(Value),  
            min = min(Value), 
            max = max(Value),
            sd=sd(Value)) 

# Shaded line plots
dodge = 0.2
plot1 <- ggplot(df_smry1,aes(x=Year, y=mean, ymin=min, ymax=max, fill=Case, group=Case, color=Case))+
  facet_grid(~prob_type + carbon_tax, labeller = label_parsed)+
  geom_line(size=1,position=position_dodge(width=dodge))+
  geom_ribbon(alpha=0.15, colour = NA,position=position_dodge(width=dodge))+
  geom_point(position=position_dodge(width=dodge))+
  scale_color_manual(values=cbPalette, guide = guide_legend(nrow = 2, label.hjust = 0))+
  scale_fill_manual(values=cbPalette, guide = guide_legend(nrow = 2, label.hjust = 0))+
  labs(x='', y=expression(paste("Cost of electricity (US$ kWh"^-1,")"))) +
  theme(legend.position="none", legend.title = element_blank(),
        axis.text.x=element_blank())

plot2 <-ggplot(df_smry2,aes(x=Year, y=mean, ymin=min, ymax=max, fill=Case, group=Case, color=Case))+
  facet_grid(~prob_type + carbon_tax, labeller = label_parsed)+
  geom_line(size=1,position=position_dodge(width=dodge))+
  geom_ribbon(alpha=0.15, colour = NA,position=position_dodge(width=dodge))+
  geom_point(position=position_dodge(width=dodge))+
  scale_color_manual(values=cbPalette, guide = guide_legend(nrow = 2, label.hjust = 0))+
  scale_fill_manual(values=cbPalette, guide = guide_legend(nrow = 2, label.hjust = 0))+
  labs(x='Year', y=expression(paste("Emissions (Mton CO"[2],")"))) +
  theme(legend.position="bottom", legend.title = element_blank(),
        axis.text.x = element_text(angle = 90,vjust=0.5), strip.background = element_blank(),
        strip.text.x = element_blank())

grid.newpage()
grid.draw(rbind(ggplotGrob(plot1), ggplotGrob(plot2), size = "first"))

ggsave('case_based_results.png', device="png",
       width=7.4, height=7.0, units="in",dpi=1000,
       plot = grid.draw(rbind(ggplotGrob(plot1), ggplotGrob(plot2), size = "first")))

