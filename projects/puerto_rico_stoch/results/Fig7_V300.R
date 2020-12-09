library("ggplot2") # Requires version 2.2.0
library(dplyr)
library(gridExtra)
library(grid)
library(lubridate)
library(reshape2)

dir_plots = "C:\\Users\\benne\\PycharmProjects\\temoatools\\projects\\puerto_rico_stoch\\results"

#===================================================================
# Case-based results
#===================================================================

# Set directory
setwd(dir_plots)

# Load data
df1 <- read.csv("costs_yearly_toPlot.csv")
df2 <- read.csv("emissions_yearly_toPlot.csv")

# Remove "solve" scenario (scenario run without stochastics)
df1<-df1[!(df1$s=="solve"),]
df2<-df2[!(df2$s=="solve"),]

# Remove without storms
df1 <- df1[ !(df1$prob_type=='None'), ]
df2 <- df2[ !(df2$prob_type=='None'), ]

# Remove historical cases with RPS
df1 <- df1[ !(df1$prob_type=='Historical' & df1$carbon_tax=='IRP'), ]
df2 <- df2[ !(df2$prob_type=='Historical' & df2$carbon_tax=='IRP'), ]

# Remove historical cases with Tax
df1 <- df1[ !(df1$prob_type=='Historical' & df1$carbon_tax=='Tax'), ]
df2 <- df2[ !(df2$prob_type=='Historical' & df2$carbon_tax=='Tax'), ]

# Rename scenarios
rename <- c("Business-as-usual"="Business-as-usual",
            "Centralized"="Centralised - hybrid",
            "Centralized - Natural Gas"="Centralised - natural gas",
           'Distributed'="Distributed - hybrid",
           'Distributed - Natural Gas'="Distributed - natural gas",
           'All'='All technologies')
df1 <- transform(df1, Scenario = rename[as.character(Scenario)])
df2 <- transform(df2, Scenario = rename[as.character(Scenario)])

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
rename <- c("No IRP"="'No policy'",
            "IRP"="'RPS'",
            "Tax"="'US$'~100~t^-1~CO[2]")
df1 <- transform(df1, carbon_tax = rename[as.character(carbon_tax)])
df2 <- transform(df2, carbon_tax = rename[as.character(carbon_tax)])

# Create new subplot labels - infra
rename <- c("Current"="Overhead power lines",
            'Hardened'="Buried power lines",
            'All'="Overhead power lines")
df1 <- transform(df1, infra = rename[as.character(infra)])
df2 <- transform(df2, infra = rename[as.character(infra)])

# Reorder carbon tax
levels <-  c("'No policy'","'RPS'",
             "'US$'~100~t^-1~CO[2]")
df1$carbon_tax <- factor(df1$carbon_tax, levels = levels)
df2$carbon_tax <- factor(df2$carbon_tax, levels = levels)

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
cbPalette <- c("#E69F00", "#000000",  "#009E73", "#0072B2", "#D55E00", "#CC79A7", "#56B4E9", "#F0E442") # Selected colors

# Summarise to create line plots
df_smry1 <- df1a %>% # the names of the new data frame and the data frame to be summarised
  group_by(.dots=c("prob_type", "carbon_tax","Case", "Year")) %>%   # the grouping variable
  summarise(mean = mean(Value),  # calculates the mean
            min = min(Value), # calculates the minimum
            max = max(Value),# calculates the maximum
            sd=sd(Value)) # calculates the standard deviation

# # Summarise to create line plots
# df_smry5 <- df5 %>% # the names of the new data frame and the data frame to be summarised
#   group_by(.dots=c("prob_type", "carbon_tax","Scenario", "Year")) %>%   # the grouping variable
#   summarise(mean = mean(Value),  # calculates the mean
#             min = min(Value), # calculates the minimum
#             max = max(Value),# calculates the maximum
#             sd=sd(Value)) # calculates the standard deviation

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
        axis.text.x=element_blank(), 
        panel.background = element_rect(fill = NA, colour ="black"),
        panel.border = element_rect(linetype="solid", fill=NA),
        strip.background = element_rect(colour = NA, fill = NA))#+ylim(0.075,0.225)

plot2 <-
  ggplot(df_smry2,aes(x=Year, y=mean, ymin=min, ymax=max, fill=Case, group=Case, color=Case))+
  facet_grid(~prob_type + carbon_tax, labeller = labeller(.multi_line = FALSE))+
  geom_line(size=1,position=position_dodge(width=dodge))+
  geom_ribbon(alpha=0.15, colour = NA,position=position_dodge(width=dodge))+
  geom_point(position=position_dodge(width=dodge))+
  scale_color_manual(values=cbPalette, guide = guide_legend(nrow = 2, label.hjust = 0))+
  scale_fill_manual(values=cbPalette, guide = guide_legend(nrow = 2, label.hjust = 0))+
  labs(x='Year', y=expression(paste("Emissions (Mton CO"[2],")"))) +
  theme(legend.position="bottom", legend.title = element_blank(),
        axis.text.x = element_text(angle = 90,vjust=0.5), 
        strip.text = element_blank(), 
        panel.background = element_rect(fill = NA, colour ="black"),
        panel.border = element_rect(linetype="solid", fill=NA),
        strip.background = element_rect(colour = NA, fill = NA))

grid.newpage()
grid.draw(rbind(ggplotGrob(plot1), ggplotGrob(plot2), size = "first"))

ggsave('Fig7_V300.png', device="png",
       width=7.4, height=6.0, units="in",dpi=1000,
       plot = grid.draw(rbind(ggplotGrob(plot1), ggplotGrob(plot2), size = "first")))

ggsave('Fig7_V300.pdf', device="pdf",
       width=7.4, height=6.0, units="in",dpi=1000,
       plot = grid.draw(rbind(ggplotGrob(plot1), ggplotGrob(plot2), size = "first")))

# Analyze Results for SI

# Table for SI
df_smry1_sub <- select(df_smry1,-c("min","max","sd"))

# Move to long format
data_long <- melt(df_smry1_sub, id.vars=c("prob_type","carbon_tax", "Case", "Year"))

# Move to wide format
data_wide <- dcast(data_long, prob_type + carbon_tax + Case + variable ~ Year, value.var="value")
write.csv(data_wide, "SI_Table16.csv")


# -----------------------------------
# Save SourceData for Journal
# -----------------------------------
# Remove sd
df_smry1 <- select(df_smry1,-c("sd"))
df_smry2 <- select(df_smry2,-c("sd"))
# Add Column to hold output type
df_smry1$Quantity ='Cost of electricity (US$ kWh^-1)'
df_smry2$Quantity ='Emissions (Mton CO2)'
sourcedata <- rbind(df_smry1,df_smry2)
# Combine
write.csv(sourcedata, "Bennett_SourceData_Fig7.csv")


