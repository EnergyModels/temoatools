library("ggplot2")
library(dplyr)
library(gridExtra)
library(RColorBrewer)

dir_plots = "C:\\Users\\benne\\PycharmProjects\\temoatools\\projects\\puerto_rico_stoch\\results"

#===================================================================
# All technologies (no cases)
#===================================================================

# Set directory
setwd(dir_plots)

# Load data:
df2 <- read.csv("capacity_by_tech_toAnalyze.csv")

#----------------
# Process data
#----------------

# Rename Year column values and factor
rename <- c("2016"="2016-20",
            "2021"="2021-25",
            '2026'="2026-30",
            '2031'="2031-35",
            '2036'="2036-40")
df2 <- transform(df2, Year = rename[as.character(Year)])
df2$Year <- factor(df2$Year)

# Rename Type column
names(df2)[names(df2) == 'fuelOrTech'] <- 'Technology'

# ---------
# Category
# ---------
df2$Category <- df2$Technology
# Rename Category - df2
rename <- c("DIST_COND"="T&D",
            "DIST_TWR"="T&D",
            "DSL_TAX"="exclude",
            "EC_BATT"="Centralised",
            "EC_BIO"="Centralised",
            "EC_COAL"="Centralised",
            "EC_DSL_CC"="Centralised",
            "EC_NG_CC"="Centralised",
            "EC_NG_OC"="Centralised",
            "EC_OIL_CC"="Centralised",
            "EC_SOLPV"="Centralised",
            "EC_WIND"="Centralised",
            "ED_BATT"="Distributed",
            "ED_BIO"="Distributed",
            "ED_NG_CC"="Distributed",
            "ED_NG_OC"="Distributed",
            "ED_SOLPV"="Distributed",
            "ED_WIND"="Distributed",
            "EX_COAL"="Existing",
            "EX_DSL_CC"="Existing",
            "EX_DSL_SIMP"="Existing",
            "EX_HYDRO"="Centralised",
            "EX_MSW_LF"="Existing",
            "EX_NG_CC"="Existing",
            "EX_OIL_TYPE1"="Existing",
            "EX_OIL_TYPE2"="Existing",
            "EX_OIL_TYPE3"="Existing",
            "EX_SOLPV"="Existing",
            "EX_WIND"="Existing",
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
            "SUB"="T&D",
            "TRANS"="T&D",
            "UGND_DIST"="T&D",
            "UGND_TRANS"="T&D")
df2 <- transform(df2, Category = rename[as.character(Category)])

# ---------
# Rename Technology - df2
# ---------
rename <- c("DIST_COND"="Distribution overhead power lines",
            "DIST_TWR"="Distribution towers",
            "DSL_TAX"="exclude",
            "EC_BATT"="Battery storage",
            "EC_BIO"="Biomass power plant",
            "EC_COAL"="Coal power plant",
            "EC_DSL_CC"="Diesel combined cycle power plant",
            "EC_NG_CC"="Natural gas combined cycle power plant",
            "EC_NG_OC"="Natural gas open cycle power plant",
            "EC_OIL_CC"="Oil combined cycle power plant",
            "EC_SOLPV"="Solar power plant",
            "EC_WIND"="Wind power plant",
            "ED_BATT"="Battery storage",
            "ED_BIO"="Biomass power plant",
            "ED_NG_CC"="Natural gas combined cycle power plant",
            "ED_NG_OC"="Natural gas open cycle power plant",
            "ED_SOLPV"="Solar power plant",
            "ED_WIND"="Wind power plant",
            "EX_COAL"="Coal power plant",
            "EX_DSL_CC"="Diesel combined cycle power plant",
            "EX_DSL_SIMP"="Diesel simple cycle biomass power plant",
            "EX_HYDRO"="Hydroelectric power plant",
            "EX_MSW_LF"="Landfill gas power plant",
            "EX_NG_CC"="Natural gas combined cycle power plant",
            "EX_OIL_TYPE1"="Oil type 1 power plant",
            "EX_OIL_TYPE2"="Oil type 2 power plant",
            "EX_OIL_TYPE3"="OIl type 3 power plant",
            "EX_SOLPV"="Solar power plant",
            "EX_WIND"="Wind power plant",
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
            "SUB"="Substations",
            "TRANS"="Transmission overhead power lines",
            "UGND_DIST"="Distribution buried power lines",
            "UGND_TRANS"="Transmission buried power lines")
df2 <- transform(df2, Technology = rename[as.character(Technology)])

# Slice dataframes to keep Categories of interest
df2 <- df2[ which(df2$Category !='exclude'),]


# make sure Technology and Category columns are factors
df2$Technology <- factor(df2$Technology)
df2$Category <- factor(df2$Category)

# Remove all non-zero entries
df3 <-subset(df2,Value!=0)

# Convert from GW to MW
df3$Value <- df3$Value*1000

#--------------------------
# Summary by all periods
#--------------------------
# Combine same technologies
groupings = c("Category","Technology")
df_smry_all <- df3 %>% 
  group_by(.dots=groupings)%>%
  summarise(min = min(Value),    # calculates the minimum
            max = max(Value))    # calculates the maximum

write.csv(df_smry_all, "new_capacity_summary_all.csv")

#--------------------------
# Summary by year
#--------------------------

# Combine same technologies
groupings = c("Category","Technology", "Year", "database")
df_smry_Year <- df3 %>%
  group_by(.dots=groupings)%>%
  summarise(min = min(Value),    # calculates the minimum
            max = max(Value))    # calculates the maximum

write.csv(df_smry_Year, "new_capacity_summary_year.csv")

#--------------------------
# Boxplot - All
#--------------------------

ggplot(df3, aes(x=Technology,y=Value,fill=Technology)) + geom_boxplot()+
  facet_grid("Year")+theme(legend.position="none",axis.text.x =  element_text(angle = 45,vjust=1.0))+coord_flip()+
  labs(y='New or reparied capacity (MW)')


ggsave('new_capacity_summary_all.png', device="png",
       width=6.0, height=5.0, units="in",dpi=500)


#--------------------------
# Boxplot - T_0
#--------------------------
df4 <-subset(df3,database=="T_0.sqlite")
ggplot(df4, aes(x=Technology,y=Value,fill=Technology)) + geom_boxplot()+
  facet_grid("Year")+theme(legend.position="none",axis.text.x =  element_text(angle = 45,vjust=1.0))+coord_flip()+
  labs(y='New or reparied capacity (MW)')


ggsave('new_capacity_summary_T0.png', device="png",
       width=6.0, height=5.0, units="in",dpi=500)