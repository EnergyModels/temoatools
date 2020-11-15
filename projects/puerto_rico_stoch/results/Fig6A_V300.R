library("ggplot2")
library(dplyr)
library(gridExtra)
library(grid)
library(lubridate)
library(tidyr)

dir_plots = "C:\\Users\\benne\\PycharmProjects\\temoatools\\projects\\puerto_rico_stoch\\results"

#===================================================================
# Case-based results
#===================================================================

# Set directory
setwd(dir_plots)

# Load data
df1 <- read.csv("costs_yearly_toPlot.csv")
# df2 <- read.csv("emissions_yearly_toPlot.csv")

# Remove scenarios that do not use all technologies
df1<-df1[(df1$Scenario=="All"),]
# df2<-df2[(df2$Scenario=="All"),]

# Remove 'No IRP' and 'New IRP'
# df1<-df1[!(df1$carbon_tax=='No IRP'),]
# df2<-df2[!(df2$carbon_tax=='No IRP'),]

# Remove "solve" scenario (scenario run without stochastics)
df1<-df1[!(df1$s=="solve"),]
# df2<-df2[!(df2$s=="solve"),]

# Rename years
rename <- c("2016"="2016-20",
            "2021"="2021-25",
            '2026'="2026-30",
            '2031'="2031-35",
            '2036'="2036-40")
df1 <- transform(df1, Year = rename[as.character(Year)])
# df2 <- transform(df2, Year = rename[as.character(Year)])

# Rename prob_type
rename <- c("None"="'No storms'",
            "Historical"="'Historical storm frequency'",
            "Climate Change"="'Increased storm frequency'")
df1 <- transform(df1, prob_type = rename[as.character(prob_type)])
# df2 <- transform(df2, prob_type = rename[as.character(prob_type)])

# Rename carbon_tax
rename <- c("No IRP"="'No policy'",
            "IRP"="'RPS'",
            "Tax"="'US$'~100~t^-1~CO[2]")
df1 <- transform(df1, carbon_tax = rename[as.character(carbon_tax)])
# df2 <- transform(df2, carbon_tax = rename[as.character(carbon_tax)])

# Create new case labels (and rename column)
names(df1)[names(df1) == 'case'] <- 'Case'
# names(df2)[names(df2) == 'case'] <- 'Case'

rename <- c("'No policy - No storms'",
            "None-All-IRP"="'RPS - No storms'",
            "None-All-Tax"="'US$'~100~t^-1~CO[2]'- No storms'",
            "Historical-All-No IRP"="'No policy - Historical storm frequency'",
            "Historical-All-IRP"="'RPS - Historical storm frequency'",
            "Historical-All-Tax"="'US$'~100~t^-1~CO[2]'- Historical storm frequency'",
            "Climate Change-All-No IRP"="'No policy - Increased storm frequency'",
            "Climate Change-All-IRP"="'RPS - Increased storm frequency'",
            "Climate Change-All-Tax"="'US$'~100~t^-1~CO[2]' - Increased storm frequency'")
df <- transform(df, Case = rename[as.character(Case)])

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
df1$Case <- factor(df1$Case, levels = levels)

# Change subplot order
df1$prob_type <- factor(df1$prob_type,
                        levels = c("'No storms'","'Historical storm frequency'","'Increased storm frequency'"))
# df2$prob_type <- factor(df2$prob_type,
                        # levels = c("'No storms'","'Historical storm frequency'","'Increased storm frequency'"))

# df1$carbon_tax <- factor(df1$carbon_tax,
                         # levels = c("'No RPS'","'RPS'"))
# df2$carbon_tax <- factor(df2$carbon_tax,
                         # levels = c("'No RPS'","'RPS'"))

# The palette with black: http://www.cookbook-r.com/Graphs/Colors_(ggplot2)/
cbPalette <- c( "#E69F00", "#56B4E9", "#009E73", "#D55E00", "#CC79A7", "#0072B2")

# The palette with black: http://www.cookbook-r.com/Graphs/Colors_(ggplot2)/
cbPalette <- c( "#E69F00", "#56B4E9", "#009E73", "#D55E00", "#CC79A7", "#0072B2","#D55E00", "#CC79A7", "#0072B2")
# cbPalette <- c(  "#56B4E9", "#0072B2", "#009E73", "#CC79A7", "#E69F00", "#D55E00",)

#cbPalette <- c(  
#  "#D55E00",
#  "#0072B2","#CC79A7" )

cbPalette <- c(    "#E69F00",
  "#D55E00",
  "#56B4E9", 
  "#0072B2",
  "#000000", 
  "#999999")


cbPalette <-c('#252525', '#6baed6', '#fb6a4a', 
              '#31a354', '#3182bd', '#de2d26',
              '#006d2c','#08519c', '#a50f15')

# Plot
ggplot(df1,aes(x=Year,y=Value, fill=Case))+
  geom_boxplot(outlier.size = 0.2) +
  facet_grid(carbon_tax ~ prob_type, labeller = label_parsed)+
  labs(x='', y=expression(paste("Cost of electricity (US$ kWh"^-1,")"))) +
  theme(legend.position="none",axis.text.x =  element_text(angle = 90,vjust=0.5), 
        panel.background = element_rect(fill = NA, colour ="black"),
        panel.border = element_rect(linetype="solid", fill=NA),
        strip.background = element_rect(colour = NA, fill = NA)) +
  scale_fill_manual(values=cbPalette)


ggsave('Fig6A_V300.png', device="png",
       width=6.0, height=5.0, units="in",dpi=1000)

# Analyze Results
groupings = c("Year","Case")
df_smry_all <- df1 %>% 
  group_by(.dots=groupings)%>%
  summarise(min = min(Value),    # calculates the minimum
            mean = mean(Value),    # calculates the minimum
            max = max(Value))    # calculates the maximum
write.csv(df_smry_all, "cost_summary.csv")

# Table for SI
# Move to long format
data_long <- melt(df_smry_all, id.vars=c("Case","Year"))

# Move to wide format
data_wide <- dcast(data_long, Case + variable ~ Year, value.var="value")
write.csv(data_wide, "SI_Table1.csv")

