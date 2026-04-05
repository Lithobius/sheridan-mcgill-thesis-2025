#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    https://shiny.posit.co/
#

library(shiny)
library(tidyverse)
# palette
library(PNWColors)
## match map with 14 levels if by region
pal<-  pnw_palette("Bay", 14, type = "continuous")

library(here)
datashiny <- here('nextseq_2022', 'data')


# set up data
nextseq_only <- read.csv(here(datashiny, 'nextseq_only.csv'))


# set up regions and sites
regions <- read_csv(here(datashiny, '20240619_peco_region-name-plotting-2022.csv')) %>%
  filter(site_code %in% nextseq_only$site_code)

region_order <- regions %>%
  select(region_lat_name, region_name, region_label, avg_region_lat) %>% 
  distinct() %>%
  arrange(-avg_region_lat)

site_order <- regions %>%
  select(site_code, decimal_latitude) %>%
  arrange(decimal_latitude) %>%
  rownames_to_column('lat_order')

# fish ranges
new_range <- read_csv(here(datashiny, 'fishrange.csv'))

# obis-gbif ranges
obisrange <- read_csv(here(datashiny, '20240708_species-site_obis-ranges.csv')) %>%
  rename(found_taxa = scientific_name) %>%
  pivot_longer(cols = !found_taxa,
               names_to = 'site_code',
               values_to = 'obis_range')

# identified issues
further_north <- c("Girella nigricans", "Embiotoca jacksoni", "Mugil cephalus", 
                   "Leuresthes tenuis", "Seriola lalandi", "Anchoa delicatissima")

further_south <- c("Ophiodon elongatus", "Liparis cyclopus", "Oncorhynchus keta", 
                   "Oncorhynchus tshawytscha", "Artedius lateralis", 
                   "Lumpenus sagitta", "Lepidogobius lepidus", 
                   "Hydrolagus colliei")

further_north_bad <- c("Girella nigricans", "Embiotoca jacksoni", "Mugil cephalus", 
                       "Leuresthes tenuis", "Anchoa delicatissima")

further_south_bad <- c("Oncorhynchus tshawytscha",
                       "Lumpenus sagitta")

northsouth_pal <- c('bad' = 'black',
                    'north' = 'grey70',
                    'south' = 'grey70')


# set up data to plot
threshold_data <- nextseq_only %>%
  select(sample_id, asv, found_taxa, common_name, reads_raw, region_name, site_code) %>%
  distinct() %>%
  # by asv
  group_by(asv) %>%
  mutate(asvreads_max = max(reads_raw)) %>%
  ungroup() %>%
  mutate(asvpercent_max = (reads_raw/asvreads_max) * 100) %>%
  group_by(found_taxa, sample_id) %>%
  mutate(reads_site = sum(reads_raw)) %>%
  ungroup() %>%
  # by species
  group_by(found_taxa) %>%
  mutate(spreads_max = max(reads_raw)) %>%
  ungroup() %>%
  mutate(sppercent_max = (reads_site / spreads_max) * 100) %>%
  # solid cutoffs
  mutate(total_percent = (reads_raw / max(reads_raw) * 100)) %>%
  # ranges
  left_join(obisrange) %>%
  mutate(further_south_obis = case_when(obis_range == 'South of range' ~ "bad")) %>%
  mutate(further_north_obis = case_when(obis_range == 'North of range' ~ "bad")) %>%
  group_by(site_code, found_taxa) %>%
  ungroup() %>%
  mutate(further_south = case_when(found_taxa %in% further_south_bad ~ "bad",
                                   found_taxa %in% further_south ~ 'south')) %>%
  mutate(further_north = case_when(found_taxa %in% further_north_bad ~ "bad",
                                   found_taxa %in% further_north ~ 'north')) %>%
  group_by(site_code, found_taxa) %>%
  mutate(further_south = case_when(any(further_south %in% c('bad')) ~ 'bad',
                                   any(further_south %in% c('south')) ~ 'south')) %>%
  mutate(further_north = case_when(any(further_north %in% c('bad')) ~ 'bad',
                                   any(further_north %in% c('north')) ~ 'north')) %>%
  ungroup()

fish_order <- new_range %>% 
  filter(found_taxa %in% threshold_data$found_taxa) %>%
  left_join(threshold_data) %>%
  select(found_taxa, common_name, taxa_mean) %>%
  distinct() %>%
  arrange(taxa_mean) %>%
  rownames_to_column('fish_order')


# Define UI for application that draws a histogram
ui <- fluidPage(
  
  # Application title
  titlePanel("PECO 2022 NextSeq filtering options"),
  
  # Sidebar with a slider input for number of bins 
  sidebarLayout(
    sidebarPanel(
      selectInput("subperc", "Choose how to remove:",
                  c("Read subtraction" = "subtract",
                    "Remove by grouped proportion" = "percent")
      ),
      conditionalPanel( condition = "input.subperc == 'subtract'",
                        radioButtons("rb_subfilt", "Choose how level to filter:",
                                     c("ASV read subtraction" = "reads_raw",
                                       "Species read subtraction" = "reads_site")),
                        sliderInput("subreads", "Number of reads to remove:",
                                    min = 1,
                                    max = 200,
                                    value = 100)
      ),
      conditionalPanel( condition = "input.subperc == 'percent'",
                        radioButtons("rb_percfilt", "Choose how level to filter:",
                                     c("Entire run" = "total_percent",
                                       "Within-species" = "sppercent_max",
                                       "Within-ASV" = "asvpercent_max")),
                        sliderInput("percreads",
                                    "Remove if reads are below X percent of group maximum. X = ",
                                    min = .000001,
                                    max = .5,
                                    step = .000005,
                                    value = .25)
      )
      
    ),
    
    
    # Show a plot of the generated distribution
    mainPanel(
      plotOutput("distPlot")
    )
  ),
  hr(),
  print("Triangles indicate whether the species is found futher north (up) or further south (down) than expected. Colored by PECO region.")
)

# Define server logic required to draw the bubble plot
server <- function(input, output) {
  
  readvalue <- reactive({
    # set this value based on whether it is subtracting or percentage
    if (input$subperc == "subtract") {input$subreads} else {input$percreads}
  })
  
  plotdata <- reactive({
    if (input$subperc == "subtract"){
      threshold_data %>%
        filter(.data[[input$rb_subfilt]] > readvalue()) %>%
        select(found_taxa, common_name, region_name, site_code, 
               further_south_obis, further_north_obis, input$rb_subfilt)}
    else {
      threshold_data %>%
        filter(.data[[input$rb_percfilt]] > readvalue()) %>%
        select(found_taxa, common_name, region_name, site_code, 
               further_south_obis, further_north_obis, input$rb_percfilt)}
  })
  
  output$distPlot <- renderPlot({
    ggplot(plotdata()) +
      geom_point(aes(x = factor(found_taxa, levels = fish_order$found_taxa), 
                     y = factor(site_code, levels = site_order$site_code),
                     #size = input$rb_asvsp,
                     color = region_name),
                 alpha = .8) +
      scale_color_manual(values = pal,
                         limits = region_order$region_name,
                         labels = region_order$region_label, 
                         name = "Region")+
      ggnewscale::new_scale_color() +
      geom_point(data = plotdata() %>% drop_na(further_north_obis),
                 aes(x = factor(found_taxa, levels = fish_order$found_taxa), 
                     y = factor(site_code, levels = site_order$site_code),
                     color = as.factor(further_north_obis)),
                 shape = 2,
                 size = 3) +
      geom_point(data = plotdata() %>% drop_na(further_south_obis),
                 aes(x = factor(found_taxa, levels = fish_order$found_taxa), 
                     y = factor(site_code, levels = site_order$site_code),
                     color = as.factor(further_south_obis)),
                 shape = 6,
                 size = 3) +
      scale_color_manual(values = northsouth_pal) +
      # coord_cartesian is what lets us add the labels later
      coord_cartesian(clip = 'off') +
      labs(y = "Sites") +
      theme_bw() +
      #scale_size(guide = 'none') +
      #scale_alpha(guide = 'none') +
      scale_x_discrete(limits = factor(fish_order$found_taxa), 
                       labels = fish_order$common_name) +
      theme(#axis.title.y = element_blank(),
        axis.text.y = element_blank(),
        axis.title.x = element_blank(),
        legend.position = 'none',
        axis.text.x = element_text(angle = 60, hjust = 1),
        plot.margin = unit(c(1,1,1,2), 'lines'),
        panel.grid.major.x = element_line(color = 'grey90'),
        panel.grid.minor.y = element_blank(),
        panel.grid.major.y = element_line(color = 'grey90'),
        #panel.grid.major.y = element_blank(),
        #panel.grid = element_blank(),
        axis.ticks.y = element_blank())
  })
}

# Run the application 
shinyApp(ui = ui, server = server)