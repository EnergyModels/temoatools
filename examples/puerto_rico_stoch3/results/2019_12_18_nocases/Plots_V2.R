library("ggplot2")
library(dplyr)

# Set working directory
setwd("C:\\Users\\jab6ft\\PycharmProjects\\temoatools\\examples\\puerto_rico_stoch3\\results\\2019_12_18_nocases")

#----------------
# Costs
#----------------
# Load data
dfc <- read.csv("costs_yearly_toPlot.csv")
# Remove "solve" scenario (scenario run without stochastics)
dfc<-dfc[!(dfc$s=="solve"),]
# Rename years
rename <- c("2016"="2016-20",
            "2021"="2021-25",
            '2026'="2026-30",
            '2031'="2031-35",
            '2036'="2036-40")
dfc <- transform(dfc, Year = rename[as.character(Year)])
# Rename prob_type
rename <- c("Historical"="'Historical storm frequency'",
            "Climate Change"="'Increased storm frequency'")
dfc <- transform(dfc, prob_type = rename[as.character(prob_type)])
# Rename carbon_tax
rename <- c("No Tax"="'No tax'",
            "Tax"="'US$'~100~t^-1~CO[2]")
dfc <- transform(dfc, carbon_tax = rename[as.character(carbon_tax)])
# Create new case labels (and rename column)
names(dfc)[names(dfc) == 'case'] <- 'Case'
rename <- c("Historical-all-No Tax"="Historical frequency + no tax",
            "Climate Change-all-No Tax"="Increased frequency + no tax",
            'Historical-all-Tax'="Historical frequency + tax",
            'Climate Change-all-Tax'="Increased frequency + tax")
dfc <- transform(dfc, Case = rename[as.character(Case)])
# Change subplot order
dfc$prob_type <- factor(dfc$prob_type,
                        levels = c("'Historical storm frequency'","'Increased storm frequency'"))
dfc$carbon_tax <- factor(dfc$carbon_tax,
                         levels = c("'No tax'","'US$'~100~t^-1~CO[2]"))
# The palette with black: http://www.cookbook-r.com/Graphs/Colors_(ggplot2)/
cbPalette <- c("#000000", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7")
# Plot
ggplot(dfc,aes(x=Year,y=Value, fill=Case))+
  geom_boxplot(outlier.size = 0.2) +
  labs(x='Year', y=expression(paste("Cost of electricity (US$ kWh"^-1,")"))) +
  theme(legend.position="right") +  scale_fill_manual(values=cbPalette)
ggsave('costs_yearly_v1.png', device="png",
       width=7.4, height=5.0, units="in",dpi=1000)

ggplot(dfc,aes(x=Year,y=Value))+
  geom_boxplot(outlier.size = 0.2) +
  facet_grid(carbon_tax ~ prob_type, labeller = label_parsed)+
  labs(x='Year', y=expression(paste("Cost of electricity (US$ kWh"^-1,")"))) +
  theme(legend.position="right") +  scale_fill_manual(values=cbPalette)
ggsave('costs_yearly_v2.png', device="png",
       width=7.4, height=5.0, units="in",dpi=1000)

#----------------
# Emissions
#----------------
# Load data
dfe <- read.csv("emissions_yearly_toPlot.csv")
# Remove "solve" scenario (scenario run without stochastics)
dfe<-dfe[!(dfe$s=="solve"),]
# Rename years
rename <- c("2016"="2016-20",
            "2021"="2021-25",
            '2026'="2026-30",
            '2031'="2031-35",
            '2036'="2036-40")
dfe <- transform(dfe, Year = rename[as.character(Year)])
# Rename prob_type
rename <- c("Historical"="'Historical storm frequency'",
            "Climate Change"="'Increased storm frequency'")
dfe <- transform(dfe, prob_type = rename[as.character(prob_type)])
# Rename carbon_tax
rename <- c("No Tax"="'No tax'",
            "Tax"="'US$'~100~t^-1~CO[2]")
dfe <- transform(dfe, carbon_tax = rename[as.character(carbon_tax)])
# Create new case labels (and rename column)
names(dfe)[names(dfe) == 'case'] <- 'Case'
rename <- c("Historical-all-No Tax"="Historical frequency + no tax",
            "Climate Change-all-No Tax"="Increased frequency + no tax",
            'Historical-all-Tax'="Historical frequency + tax",
            'Climate Change-all-Tax'="Increased frequency + tax")
dfe <- transform(dfe, Case = rename[as.character(Case)])
# Change subplot order
dfc$prob_type <- factor(dfe$prob_type,
                        levels = c("'Historical storm frequency'","'Increased storm frequency'"))
dfc$carbon_tax <- factor(dfe$carbon_tax,
                         levels = c("'No tax'","'US$'~100~t^-1~CO[2]"))
# Change subplot order
dfe$prob_type <- factor(dfe$prob_type,
                        levels = c("'Historical storm frequency'","'Increased storm frequency'"))
dfe$carbon_tax <- factor(dfe$carbon_tax,
                         levels = c("'No tax'","'US$'~100~t^-1~CO[2]"))
# The palette with black: http://www.cookbook-r.com/Graphs/Colors_(ggplot2)/
cbPalette <- c("#000000", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7")
# Plot
ggplot(dfe,aes(x=Year,y=Value, fill=Case))+
  geom_boxplot(outlier.size = 0.2) +
  labs(x='Year', y=expression(paste("Emissions (Mton CO"[2],")"))) +
  theme(legend.position="right") +  scale_fill_manual(values=cbPalette)
ggsave('emissions_yearly_v1.png', device="png",
       width=7.4, height=5.0, units="in",dpi=1000)

ggplot(dfe,aes(x=Year,y=Value))+
  geom_boxplot(outlier.size = 0.2) +
  facet_grid(carbon_tax ~ prob_type, labeller = label_parsed)+
  labs(x='Year', y=expression(paste("Emissions (Mton CO"[2],")"))) +
  theme(legend.position="right") +  scale_fill_manual(values=cbPalette)
ggsave('emissions_yearly_v2.png', device="png",
       width=7.4, height=5.0, units="in",dpi=1000)

#----------------
# Activity by fuel
#----------------
# Load data
df1 <- read.csv("activity_by_fuel_toPlot.csv")
# Remove "solve" scenario (scenario run without stochastics)
df1<-df1[!(df1$s=="solve"),]
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
# Rename Type column
names(df1)[names(df1) == 'Type'] <- 'Technology'
# Rename Technology
rename <- c("ELC_CENTRAL"="Battery",
            "ELC_DIST"="Battery",
            "BIO"="Other renew.",
            "COAL_TAXED"="Coal",
            "DSL_TAXED"="Petroleum",
            "HYDRO"="Other renew.",
            "MSW_LF_TAXED"="Other renew.",
            'NATGAS_TAXED'="Natural gas",
            'OIL_TAXED'="Petroleum",
            "SOLAR"="Solar",
            "WIND"="Wind")
df1 <- transform(df1, Technology = rename[as.character(Technology)])
# Combine same technologies within each scenario (s)
df1_regrp <- df1 %>% # the names of the new data frame and the data frame to be summarised
  group_by(.dots=c("Scenario","s","Technology","Year","case","prob_type","infra",
                   "carbon_tax","infra_and_carbon_tax", "entry"))%>%
  summarise(Value=sum(Value))
# Change subplot order
df1_regrp$prob_type <- factor(df1_regrp$prob_type,
                              levels = c("'Historical storm frequency'","'Increased storm frequency'"))
df1_regrp$carbon_tax <- factor(df1_regrp$carbon_tax,
                               levels = c("'No tax'","'US$'~100~t^-1~CO[2]"))
# http://www.stat.columbia.edu/~tzheng/files/Rcolor.pdf
#custom_palette <- c("darkorange","dimgray","darkorange4","dodgerblue","black","gold","forestgreen")
custom_palette <- c("#E69F00","dimgray","darkorange4","#56B4E9","#000000","#F0E442","#009E73")

# Plot
ggplot(df1_regrp,aes(x=Technology,y=Value,fill=Technology))+
  geom_boxplot(outlier.size = 0.2) + facet_grid(Year~ carbon_tax + prob_type, labeller = label_parsed)+
  labs(x='', y=expression(paste("Activity (TWh y"^-1,")"))) +
  theme(legend.position="bottom",axis.text.x=element_blank(),
        axis.ticks.x=element_blank()) +  scale_fill_manual(values=custom_palette)
# Solve
ggsave('activity_by_fuel.png', device="png",
       width=7.4, height=4.0, units="in",dpi=1000)

#----------------
# Activity Plots - Hardening
#----------------

# Load data
df2 <- read.csv("activity_by_tech_toPlot.csv")
# Remove "solve" scenario (scenario run without stochastics)
df2<-df2[!(df2$s=="solve"),]
# Rename years
rename <- c("2016"="2016-20",
            "2021"="2021-25",
            '2026'="2026-30",
            '2031'="2031-35",
            '2036'="2036-40")
df2 <- transform(df2, Year = rename[as.character(Year)])
# Rename prob_type
rename <- c("Historical"="'Historical storm frequency'",
            "Climate Change"="'Increased storm frequency'")
df2 <- transform(df2, prob_type = rename[as.character(prob_type)])
# Rename carbon_tax
rename <- c("No Tax"="'No tax'",
            "Tax"="'US$'~100~t^-1~CO[2]")
df2 <- transform(df2, carbon_tax = rename[as.character(carbon_tax)])
# Rename Type column
names(df2)[names(df2) == 'Type'] <- 'Technology'
# Rename Technology
rename <- c("DIST_COND"="Distribution - overhead",
            "DIST_TWR"="exclude",
            "DSL_TAX"="exclude",
            "EC_BATT"="exclude",
            "EC_BIO"="exclude",
            "EC_COAL"="exclude",
            "EC_DSL_CC"="exclude",
            "EC_NG_CC"="exclude",
            "EC_NG_OC"="exclude",
            "EC_OIL_CC"="exclude",
            "EC_SOLPV"="exclude",
            "EC_WIND"="exclude",
            "ED_BATT"="exclude",
            "ED_BIO"="exclude",
            "ED_NG_CC"="exclude",
            "ED_NG_OC"="exclude",
            "ED_SOLPV"="exclude",
            "ED_WIND"="exclude",
            "EX_COAL"="exclude",
            "EX_DSL_CC"="exclude",
            "EX_DSL_SIMP"="exclude",
            "EX_HYDRO"="exclude",
            "EX_MSW_LF"="exclude",
            "EX_NG_CC"="exclude",
            "EX_OIL_TYPE1"="exclude",
            "EX_OIL_TYPE2"="exclude",
            "EX_OIL_TYPE3"="exclude",
            "EX_SOLPV"="exclude",
            "EX_WIND"="exclude",
            "IMPBIO"="exclude",
            "IMPCOAL"="exclude",
            "IMPDSL"="exclude",
            "IMPHYDRO"="exclude",
            "IMPMSW_LF"="exclude",
            "IMPNATGAS"="exclude",
            "IMPOIL"="exclude",
            "IMPSOLAR"="exclude",
            "IMPWIND"="exclude",
            "LOCAL"="exclude",
            "MSW_LF_TAX"="exclude",
            "NATGAS_TAX"="exclude",
            "OIL_TAX"="exclude",
            "SUB"="exclude",
            "TRANS"="Transmission - overhead",
            "UGND_DIST"="Distribution - buried",
            "UGND_TRANS"="Transmission - buried")
df2 <- transform(df2, Technology = rename[as.character(Technology)])
# Slice dataframe to keep technologies of interest
df2a <- df2[ which(df2$Technology !='exclude'),]
# Change subplot order
df2a$prob_type <- factor(df2a$prob_type,
                         levels = c("'Historical storm frequency'","'Increased storm frequency'"))
df2a$carbon_tax <- factor(df2a$carbon_tax,
                          levels = c("'No tax'","'US$'~100~t^-1~CO[2]"))
# The palette with black: http://www.cookbook-r.com/Graphs/Colors_(ggplot2)/
cbPalette <- c("#000000", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7")
# http://www.stat.columbia.edu/~tzheng/files/Rcolor.pdf
#custom_palette <- c("darkorange","dimgray","darkorange4","dodgerblue","black","gold","forestgreen")
custom_palette <- c("#E69F00","dimgray","darkorange4","#56B4E9","#000000","#F0E442","#009E73")

# Plot
ggplot(df2a,aes(x=Technology,y=Value,fill=Technology))+
  geom_boxplot(outlier.size = 0.2) + facet_grid(Year~ carbon_tax + prob_type, labeller = label_parsed)+
  labs(x='', y=expression(paste("Activity (TWh y"^-1,")"))) +
  theme(legend.position="bottom",axis.text.x=element_blank(),
        axis.ticks.x=element_blank()) +  scale_fill_manual(values=cbPalette)
# Solve
ggsave('activity_hardening.png', device="png",
       width=7.4, height=5.0, units="in",dpi=1000)


#----------------
# Activity Plots - Centralized vs. distributed
#----------------

# Load data
df3 <- read.csv("activity_by_tech_toPlot.csv")
# Remove "solve" scenario (scenario run without stochastics)
df3<-df3[!(df3$s=="solve"),]
# Rename years
rename <- c("2016"="2016-20",
            "2021"="2021-25",
            '2026'="2026-30",
            '2031'="2031-35",
            '2036'="2036-40")
df3 <- transform(df3, Year = rename[as.character(Year)])
# Rename prob_type
rename <- c("Historical"="'Historical storm frequency'",
            "Climate Change"="'Increased storm frequency'")
df3 <- transform(df3, prob_type = rename[as.character(prob_type)])
# Rename carbon_tax
rename <- c("No Tax"="'No tax'",
            "Tax"="'US$'~100~t^-1~CO[2]")
df3 <- transform(df3, carbon_tax = rename[as.character(carbon_tax)])
# Rename Type column
names(df3)[names(df3) == 'Type'] <- 'Technology'
# Rename Technology
rename <- c("EX_COAL"="Centralised - fossil",
            "EX_DSL_CC"="Centralised - fossil",
            "EX_DSL_SIMP"="Centralised - fossil",
            "EX_NG_CC"="Centralised - fossil",
            "EX_OIL_TYPE1"="Centralised - fossil",
            "EX_OIL_TYPE2"="Centralised - fossil",
            "EX_OIL_TYPE3"="Centralised - fossil",
            "EC_COAL"="Centralised - fossil",
            "EC_DSL_CC"="Centralised - fossil",
            "EC_NG_CC"="Centralised - fossil",
            "EC_NG_OC"="Centralised - fossil",
            "EC_OIL_CC"="Centralised - fossil",
            "ED_NG_CC"="Distributed - fossil",
            "ED_NG_OC"="Distributed - fossil",
            "EX_HYDRO"="Centralised - renewable",
            "EX_MSW_LF"="Centralised - renewable",
            "EX_SOLPV"="Centralised - renewable",
            "EX_WIND"="Centralised - renewable",
            "EC_BIO"="Centralised - renewable",
            "EC_SOLPV"="Centralised - renewable",
            "EC_WIND"="Centralised - renewable",
            "ED_BIO"="Distributed - renewable",
            "ED_SOLPV"="Distributed - renewable",
            "ED_WIND"="Distributed - renewable",
            "EC_BATT"="exclude",
            "ED_BATT"="exclude",
            "DIST_COND"="exclude",
            "DIST_TWR"="exclude",
            "DSL_TAX"="exclude",
            "IMPBIO"="exclude",
            "IMPCOAL"="exclude",
            "IMPDSL"="exclude",
            "IMPHYDRO"="exclude",
            "IMPMSW_LF"="exclude",
            "IMPNATGAS"="exclude",
            "IMPOIL"="exclude",
            "IMPSOLAR"="exclude",
            "IMPWIND"="exclude",
            "LOCAL"="exclude",
            "MSW_LF_TAX"="exclude",
            "NATGAS_TAX"="exclude",
            "OIL_TAX"="exclude",
            "SUB"="exclude",
            "TRANS"="exclude",
            "UGND_DIST"="exclude",
            "UGND_TRANS"="exclude")
df3 <- transform(df3, Technology = rename[as.character(Technology)])
# Slice dataframe to keep technologies of interest
df3a <- df3[ which(df3$Technology !='exclude'),]
# Combine same technologies within each scenario (s)
df3_regrp <- df3a %>% # the names of the new data frame and the data frame to be summarised
  group_by(.dots=c("Scenario","s","Technology","Year","case","prob_type","infra",
                   "carbon_tax","infra_and_carbon_tax", "entry"))%>%
  summarise(Value=sum(Value))
# Change subplot order
df3_regrp$prob_type <- factor(df3_regrp$prob_type,
                              levels = c("'Historical storm frequency'","'Increased storm frequency'"))
df3_regrp$carbon_tax <- factor(df3_regrp$carbon_tax,
                               levels = c("'No tax'","'US$'~100~t^-1~CO[2]"))

# Plot
ggplot(df3_regrp,aes(x=Technology,y=Value,fill=Technology))+
  geom_boxplot(outlier.size = 0.2) + facet_grid(Year~ carbon_tax + prob_type, labeller = label_parsed)+
  labs(x='', y=expression(paste("Activity (TWh y"^-1,")"))) +
  theme(legend.position="bottom",axis.text.x=element_blank(),
        axis.ticks.x=element_blank()) +  scale_fill_manual(values=cbPalette)
# Solve
ggsave('activity_architecture.png', device="png",
       width=7.4, height=5.0, units="in",dpi=1000)
