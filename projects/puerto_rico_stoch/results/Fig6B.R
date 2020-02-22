library("ggplot2")
library(dplyr)

dir_plots = "C:\\Users\\jab6ft\\PycharmProjects\\temoatools\\examples\\puerto_rico_stoch3\\results"
dir_nocases = "C:\\Users\\jab6ft\\PycharmProjects\\temoatools\\examples\\puerto_rico_stoch3\\results\\2019_12_18_nocases"
dir_cases = "C:\\Users\\jab6ft\\PycharmProjects\\temoatools\\examples\\puerto_rico_stoch3\\results\\2019_12_18_cases"

#===================================================================
# All technologies (no cases)
#===================================================================

# Set directory to load data
setwd(dir_nocases)

# Load data
df1 <- read.csv("emissions_yearly_toPlot.csv")

# Set directory for plotting
setwd(dir_plots)

# Remove "solve" scenario (scenario run without stochastics)
df1<-df1[!(dfc$s=="solve"),]

# Rename years
rename <- c("2016"="2016-20",
            "2021"="2021-25",
            '2026'="2026-30",
            '2031'="2031-35",
            '2036'="2036-40")
df1 <- transform(df1, Year = rename[as.character(Year)])

# Rename prob_type
rename <- c("Historical"="'Historical storm frequency'",
            "Climate Change"="'Increased storm frequency'")
df1 <- transform(df1, prob_type = rename[as.character(prob_type)])

# Rename carbon_tax
rename <- c("No Tax"="'No tax'",
            "Tax"="'US$'~100~t^-1~CO[2]")
df1 <- transform(df1, carbon_tax = rename[as.character(carbon_tax)])

# Create new case labels (and rename column)
names(df1)[names(df1) == 'case'] <- 'Case'
rename <- c("Historical-all-No Tax"="Historical frequency + no tax",
            "Climate Change-all-No Tax"="Increased frequency + no tax",
            'Historical-all-Tax'="Historical frequency + tax",
            'Climate Change-all-Tax'="Increased frequency + tax")
df1 <- transform(df1, Case = rename[as.character(Case)])

# Change subplot order
df1$prob_type <- factor(df1$prob_type,
                        levels = c("'Historical storm frequency'","'Increased storm frequency'"))
df1$carbon_tax <- factor(df1$carbon_tax,
                         levels = c("'No tax'","'US$'~100~t^-1~CO[2]"))

# The palette with black: http://www.cookbook-r.com/Graphs/Colors_(ggplot2)/
cbPalette <- c( "#E69F00", "#56B4E9", "#009E73", "#D55E00", "#CC79A7")

# Plot
ggplot(df1,aes(x=Year,y=Value, fill=Case))+
  geom_boxplot(outlier.size = 0.2) +
  facet_grid(carbon_tax ~ prob_type, labeller = label_parsed)+
  labs(x='Year', y=expression(paste("Emissions (Mton CO"[2],")"))) +
  theme(legend.position="none",axis.text.x = element_text(angle = 90,vjust=0.5)) +  scale_fill_manual(values=cbPalette)

ggsave('emissions_yearly.png', device="png",
       width=4.5, height=4.5, units="in",dpi=1000)
