library("ggplot2")
library(dplyr)

# Set working directory
# setwd("C:\\Users\\benne\\Box Sync\\Software\\R\\PR_Final") # Home computer
setwd("C:\\Users\\jab6ft\\PycharmProjects\\temoatools\\examples\\puerto_rico_stoch3\\results\\2019_12_18_cases") # Work computer

# Load data
df1 <- read.csv("costs_yearly_toPlot.csv")

# Rename scenarios
rename <- c("Business-as-usual"="Business-as-usual",
            "Centralized - Hybrid"="Centralised - hybrid",
            'Centralized - Natural Gas'="Centralised - natural gas",
            'Distributed - Hybrid'="Distributed - hybrid",
            'Distributed - Natural Gas'="Distributed - natural gas")
df1 <- transform(df1, Scenario = rename[as.character(Scenario)])

# Rename years
rename <- c("2016"="2016-20",
            "2021"="2021-25",
            '2026'="2026-30",
            '2031'="2031-35",
            '2036'="2036-40")
df1 <- transform(df1, Year = rename[as.character(Year)])

# Create new subplot labels
rename <- c("Historical-Current-No Tax"="Historical frequency + overhead",
            "Climate Change-Current-No Tax"="Increased frequency + overhead",
            'Historical-Hardened-No Tax'="Historical frequency + buried",
            'Climate Change-Hardened-No Tax'="Increased frequency + buried",
            'Historical-Current-Tax'="Historical frequency + overhead", 
            'Climate Change-Current-Tax'="Increased frequency + overhead", 
            'Historical-Hardened-Tax'="Historical frequency + buried",
            'Climate Change-Hardened-Tax'="Increased frequency + buried")
df1 <- transform(df1, case2 = rename[as.character(case)])

# Create new subplot labels - part 2
rename <- c("Historical"="Historical storm frequency",
            "Climate Change"="Increased storm frequency")
df1 <- transform(df1, prob_type = rename[as.character(prob_type)])

# Create new subplot labels - part 3
rename <- c("Current"="Overhead power lines",
            'Hardened'="Buried power lines")
df1 <- transform(df1, infra = rename[as.character(infra)])

# Change subplot order
df1$case2 <- factor(df1$case2,
                       levels = c("Historical frequency + overhead", 
                                  "Increased frequency + overhead", 
                                  "Historical frequency + buried", 
                                  "Increased frequency + buried"))

df1$infra <- factor(df1$infra,
                    levels = c("Overhead power lines", 
                               "Buried power lines"))

df1$prob_type <- factor(df1$prob_type,
                    levels = c("Historical storm frequency", 
                               "Increased storm frequency"))

# Rename Scenario column
names(df1)[names(df1) == 'Scenario'] <- 'Case'

# Slice dataframe for a plot without and with a carbon tax
df1a <- df1[ which(df1$carbon_tax=='No Tax'),]
df1b <- df1[ which(df1$carbon_tax=='Tax'),]

# The palette with black: http://www.cookbook-r.com/Graphs/Colors_(ggplot2)/
cbPalette <- c("#000000", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7")

# The palette with grey:
# cbPalette <- c("#999999", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7")



#----------------
# Plot - Without carbon tax
#----------------
ggplot(df1a,aes(x=Case,y=Value,fill=Case))+
  geom_boxplot(outlier.size = 0.2) +
  facet_grid(Year~infra + prob_type, labeller = label_wrap_gen(width=15)) + 
  labs(x='', y=expression(paste("Cost of electricity (US$ kWh"^-1,")"))) +
  theme(legend.position="right",axis.text.x=element_blank(),
          axis.ticks.x=element_blank()) +
  scale_fill_manual(values=cbPalette)#+guides(fill=guide_legend(nrow=2,byrow=TRUE))

ggsave('costs_yearly_no_tax_v2.png', device="png",
       width=7.4, height=5.0, units="in",dpi=1000)

#----------------
# Plot - With carbon tax
#----------------
ggplot(df1b,aes(x=Case,y=Value,fill=Case))+
  geom_boxplot(outlier.size = 0.2) +
  facet_grid(Year~infra + prob_type, labeller = label_wrap_gen(width=15)) + 
  labs(x='', y=expression(paste("Cost of electricity (US$ kWh"^-1,")"))) +
  theme(legend.position="right",axis.text.x=element_blank(),
        axis.ticks.x=element_blank()) +
  scale_fill_manual(values=cbPalette)

ggsave('costs_yearly_tax.png', device="png",
       width=7.4, height=5.0, units="in",dpi=1000)


#=====================================
# Cost + Emissions
#=====================================
df2 <- read.csv("cost_emissions_comb.csv")

# Rename scenarios
rename <- c("Business-as-usual"="Business-as-usual",
            "Centralized - Hybrid"="Centralised - hybrid",
            'Centralized - Natural Gas'="Centralised - natural gas",
            'Distributed - Hybrid'="Distributed - hybrid",
            'Distributed - Natural Gas'="Distributed - natural gas")
df2 <- transform(df2, Scenario = rename[as.character(Scenario)])

# Rename carbon_tax
rename <- c("No Tax"="'No tax'",
            "Tax"="'US$'~100~t^-1~CO[2]")
df2 <- transform(df2, carbon_tax = rename[as.character(carbon_tax)])


rename <- c("Current"="'Overhead lines'",
            "Hardened"="'Buried lines'")
df2 <- transform(df2, infra = rename[as.character(infra)])

# Change subplot order
df2$infra <- factor(df2$infra,
                    levels = c("'Overhead lines'","'Buried lines'"))

# Rename Scenario column
names(df2)[names(df2) == 'Scenario'] <- 'Case'

#----------------
# Version 1 - Scatterplot matrix
#----------------

p1 <- ggplot(df2,aes(x=Emissions,y=Cost,color=Case))+geom_point()+
  facet_grid(carbon_tax~infra, labeller = label_parsed)
p2 <- p1 + labs(x=expression(paste("Emissions (Mt CO"[2],")")), 
                                   y=expression(paste("Cost of electricity (US$ kWh"^-1,")")))
p2 +theme(legend.position="right") +  scale_color_manual(values=cbPalette)

ggsave('costs_emissions_scatter.png', device="png",
       width=7.4, height=5.0, units="in",dpi=1000)

#----------------
# Version 2 - Range matrix
#----------------
df_summary <- df2 %>% # the names of the new data frame and the data frame to be summarised
  group_by(.dots=c("Case","infra","carbon_tax")) %>%   # the grouping variable
  summarise(mean_cost = mean(Cost),  # calculates the mean of each group
            min_cost = min(Cost), # calculates the minimum of each group
            max_cost = max(Cost), # calculates the maximum of each group
            mean_emi = mean(Emissions),  # calculates the mean of each group
            min_emi = min(Emissions), # calculates the minimum of each group
            max_emi = max(Emissions)) # calculates the maximum of each group

write.table(df_summary, "mydata.txt", sep="\t")

ggplot(data = df_summary,aes(x = mean_emi,y = mean_cost, color=Case)) + 
  geom_errorbar(aes(ymin = min_cost,ymax = max_cost),size=1.0,width=0.0) + 
  geom_errorbarh(aes(xmin = min_emi,xmax = max_emi),size=1.0,height=0.0)+
  facet_grid(carbon_tax~infra, labeller = label_wrap_gen(width=15))+ 
  labs(x=expression(paste("Emissions (Mt CO"[2],")")), 
       y=expression(paste("Cost of electricity (US$ kWh"^-1,")")))+
  theme(legend.position="right") +  
  scale_color_manual(values=cbPalette)

ggsave('costs_emissions_range.png', device="png",
       width=7.4, height=6.0, units="in",dpi=1000)

#----------------
# Emissions Plots
#----------------

# Load data
df3 <- read.csv("emissions_yearly_toPlot.csv")

# Rename scenarios
rename <- c("Business-as-usual"="Business-as-usual",
            "Centralized - Hybrid"="Centralised - hybrid",
            'Centralized - Natural Gas'="Centralised - natural gas",
            'Distributed - Hybrid'="Distributed - hybrid",
            'Distributed - Natural Gas'="Distributed - natural gas")
df3 <- transform(df3, Scenario = rename[as.character(Scenario)])

# Rename years
rename <- c("2016"="2016-20",
            "2021"="2021-25",
            '2026'="2026-30",
            '2031'="2031-35",
            '2036'="2036-40")
df3 <- transform(df3, Year = rename[as.character(Year)])

# Create new subplot labels
rename <- c("Historical-Current-No Tax"="Historical + no tax",
            "Climate Change-Current-No Tax"="Climate change + no tax",
            'Historical-Hardened-No Tax'="Historical + no tax",
            'Climate Change-Hardened-No Tax'="Climate change + no tax",
            'Historical-Current-Tax'="Historical + tax", 
            'Climate Change-Current-Tax'="Climate change + tax", 
            'Historical-Hardened-Tax'="Historical + tax",
            'Climate Change-Hardened-Tax'="Climate change + tax")
df3 <- transform(df3, case2 = rename[as.character(case)])

# Change subplot order
df3$case2 <- factor(df3$case2,
                    levels = c("Historical + no tax", "Climate change + no tax", 
                               "Historical + tax", "Climate change + tax"))

# Rename Scenario column
names(df3)[names(df3) == 'Scenario'] <- 'Case'

# Slice dataframe for a plot without and with a carbon tax
df3a <- df3[ which(df3$infra=='Current'),]
df3b <- df3[ which(df3$infra=='Hardened'),]

# The palette with black: http://www.cookbook-r.com/Graphs/Colors_(ggplot2)/
cbPalette <- c("#000000", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7")

# The palette with grey:
# cbPalette <- c("#999999", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7")

#----------------
# Plot - Overhead lines
#----------------
ggplot(df3a,aes(x=Case,y=Value,fill=Case))+
  geom_boxplot(outlier.size = 0.2) +
  facet_grid(Year~case2, labeller = label_wrap_gen(width=15)) + 
  labs(x='', y=expression(paste("Emissions (Mton CO"[2],")"))) +
  theme(legend.position="right",axis.text.x=element_blank(),
        axis.ticks.x=element_blank()) +
  scale_fill_manual(values=cbPalette)#+guides(fill=guide_legend(nrow=2,byrow=TRUE))

ggsave('emissions_yearly_overhead.png', device="png",
       width=7.4, height=5.0, units="in",dpi=1000)

#----------------
# Plot - Buried lines
#----------------
ggplot(df3b,aes(x=Case,y=Value,fill=Case))+
  geom_boxplot(outlier.size = 0.2) +
  facet_grid(Year~case2, labeller = label_wrap_gen(width=15)) + 
  labs(x='', y=expression(paste("Emissions (Mton CO"[2],")"))) +
  theme(legend.position="right",axis.text.x=element_blank(),
        axis.ticks.x=element_blank()) +
  scale_fill_manual(values=cbPalette)

ggsave('emissions_yearly_buried.png', device="png",
       width=7.4, height=5.0, units="in",dpi=1000)

#----------------
# Activity Plots
#----------------

# Load data
df4 <- read.csv("activity_by_fuel_toPlot.csv")

# Rename scenarios
rename <- c("Business-as-usual"="Business-as-usual",
            "Centralized - Hybrid"="Centralised - hybrid",
            'Centralized - Natural Gas'="Centralised - natural gas",
            'Distributed - Hybrid'="Distributed - hybrid",
            'Distributed - Natural Gas'="Distributed - natural gas")
df4 <- transform(df4, Scenario = rename[as.character(Scenario)])

# Remove "solve" scenario (scenario run without stochastics)
df4<-df4[!(df4$s=="solve"),]

# Rename Type2
rename <- c("Battery"="Battery",
            "Biomass"="Other renew.",
            "Coal"="Coal",
            "Diesel"="Petroleum",
            "Hydro"="Other renew.",
            "Landfill Gas"="Other renew.",
            'Natural Gas'="Natural gas",
            'Oil'="Petroleum",
            "Solar"="Solar",
            "Wind"="Wind")
df4 <- transform(df4, Type2 = rename[as.character(Type2)])

df4_regrp <- df4 %>% # the names of the new data frame and the data frame to be summarised
  group_by(.dots=c("Scenario","s","Year","case","prob_type","infra",
                   "carbon_tax","infra_and_carbon_tax","Type2"))%>%
                   summarise(Value=sum(Value))

# Calculate Averages across s values
df4_summary <- df4_regrp %>% # the names of the new data frame and the data frame to be summarised
  group_by(.dots=c("Scenario","Year","infra","carbon_tax","Type2")) %>%   # the grouping variable
  summarise(mean = mean(Value),  # calculates the mean of each group
            min = min(Value), # calculates the minimum of each group
            max = max(Value)) # calculates the maximum of each group

# Slice dataframe for data selected to plot
df4_summary2 <- df4_summary[ which(df4_summary$infra=='Current'),]

# Rename carbon_tax
rename <- c("No Tax"="'No tax'",
            "Tax"="'US$'~100~t^-1~CO[2]")
df4_summary2 <- transform(df4_summary2, carbon_tax = rename[as.character(carbon_tax)])

# Rename years
rename <- c("2016"="2016-20",
            "2021"="2021-25",
            '2026'="2026-30",
            '2031'="2031-35",
            '2036'="2036-40")
df4_summary2 <- transform(df4_summary2, Year = rename[as.character(Year)])

# Rename Type2 column
names(df4_summary2)[names(df4_summary2) == 'Type2'] <- 'Technology'

# http://www.stat.columbia.edu/~tzheng/files/Rcolor.pdf
#custom_palette <- c("darkorange","dimgray","darkorange4","dodgerblue","black","gold","forestgreen")
custom_palette <- c("#E69F00","dimgray","darkorange4","#56B4E9","#000000","#F0E442","#009E73")

# Plot
ggplot(df4_summary2,aes(x=Scenario,y=mean,fill=Technology)) + geom_col()+
  facet_grid(Year~carbon_tax, labeller = label_parsed)+
  labs(x='', y=expression(paste("Activity (TWh y"^-1,")"))) +
  theme(axis.text.x = element_text(angle = 45,hjust=1)) +
  scale_fill_manual(values=custom_palette)

ggsave('activity.png', device="png",
       width=7.4, height=5.0, units="in",dpi=1000)
