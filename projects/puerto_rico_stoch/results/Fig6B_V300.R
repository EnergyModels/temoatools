library("ggplot2")
library(dplyr)
library(gridExtra)
library(grid)
library(lubridate)

dir_plots = "C:\\Users\\benne\\PycharmProjects\\temoatools\\projects\\puerto_rico_stoch\\results"

#===================================================================
# Case-based results
#===================================================================

# Set directory
setwd(dir_plots)

# Load data
# df1 <- read.csv("costs_yearly_toPlot.csv")
df2 <- read.csv("emissions_yearly_toPlot.csv")

# Remove scenarios that do not use all technologies
# df1<-df1[(df1$Scenario=="All"),]
df2<-df2[(df2$Scenario=="All"),]

# Remove 'No IRP' and 'New IRP'
# df1<-df1[!(df1$carbon_tax=='No IRP'),]
# df2<-df2[!(df2$carbon_tax=='No IRP'),]

# Remove unnamed columns
drops <- c(names(df2)[3],names(df2)[4],names(df2)[5])
df2 <- df2[ , !(names(df2) %in% drops)]

# Remove No stormss and Increased storm frequency cases
df2<-df2[(df2$prob_type=="Historical"),]

# Remove "solve" scenario (scenario run without stochastics)
# df1<-df1[!(df1$s=="solve"),]
df2<-df2[!(df2$s=="solve"),]

# Rename years
rename <- c("2016"="2016-20",
            "2021"="2021-25",
            '2026'="2026-30",
            '2031'="2031-35",
            '2036'="2036-40")
# df1 <- transform(df1, Year = rename[as.character(Year)])
df2 <- transform(df2, Year = rename[as.character(Year)])

# Rename prob_type
rename <- c("None"="'No storms'",
            "Historical"="'Historical storm frequency'",
            "Climate Change"="'Increased storm frequency'")
# df1 <- transform(df1, prob_type = rename[as.character(prob_type)])
df2 <- transform(df2, prob_type = rename[as.character(prob_type)])

# Rename carbon_tax
rename <- c("No IRP"="'No policy'",
            "IRP"="'RPS'",
            "Tax"="'US$'~100~t^-1~CO[2]")
# df1 <- transform(df1, carbon_tax = rename[as.character(carbon_tax)])
df2 <- transform(df2, carbon_tax = rename[as.character(carbon_tax)])

# Create new case labels (and rename column)
# names(df1)[names(df1) == 'case'] <- 'Case'
names(df2)[names(df2) == 'case'] <- 'Case'

# Change subplot order - Case
levels <- c("None-All-No IRP",
            "None-All-IRP",
            "None-All-Tax",
            "Historical-All-No IRP",
            "Historical-All-IRP",
            "Historical-All-Tax",
            "Climate Change-All-No IRP",
            "Climate Change-All-IRP",
            "Climate Change-All-Tax")
df2$Case <- factor(df2$Case, levels = levels)

# Change subplot order
# df1$prob_type <- factor(df1$prob_type,
                        # levels = c("'No storms'","'Historical storm frequency'","'Increased storm frequency'"))
df2$prob_type <- factor(df2$prob_type,
                         levels = c("'No storms'","'Historical storm frequency'","'Increased storm frequency'"))

#df1$carbon_tax <- factor(df1$carbon_tax,
#                         levels = c("'No RPS'","'RPS'"))
df2$carbon_tax <- factor(df2$carbon_tax,
                         levels = c("'No policy'","'RPS'","'US$'~100~t^-1~CO[2]"))

# The palette with black: http://www.cookbook-r.com/Graphs/Colors_(ggplot2)/
cbPalette <- c( "#E69F00", "#56B4E9", "#009E73", "#D55E00", "#CC79A7", "#0072B2")

# The palette with black: http://www.cookbook-r.com/Graphs/Colors_(ggplot2)/
cbPalette <- c( "#E69F00", "#56B4E9", "#009E73", "#D55E00", "#CC79A7", "#0072B2","#D55E00", "#CC79A7", "#0072B2")
# cbPalette <- c(  "#56B4E9", "#0072B2", "#009E73", "#CC79A7", "#E69F00", "#D55E00",)

#cbPalette <- c(  
#  "#D55E00",
#  "#0072B2","#CC79A7" )

cbPalette <-c('#252525', '#6baed6', '#fb6a4a', 
              '#31a354', '#3182bd', '#de2d26',
              '#006d2c','#08519c', '#a50f15')

cbPalette <-c('#252525', '#6baed6', '#fb6a4a', 
              '#31a354', '#3182bd', '#de2d26',
              '#006d2c','#08519c', '#a50f15')


# Plot
ggplot(df2,aes(x=Year,y=Value, fill=Case))+
  geom_boxplot(outlier.size = 0.2) +
  facet_grid(carbon_tax ~ prob_type, labeller = label_parsed)+
  labs(x='', y=expression(paste("Emissions (Mton CO"[2],")"))) +
  theme(legend.position="none",axis.text.x =  element_text(angle = 90,vjust=0.5), 
        panel.background = element_rect(fill = NA, colour ="black"),
        panel.border = element_rect(linetype="solid", fill=NA),
        strip.background = element_rect(colour = NA, fill = NA)) +
  scale_fill_manual(values=cbPalette)


ggsave('Fig6B_V300.png', device="png",
       width=2.5, height=5.0, units="in",dpi=1000)
