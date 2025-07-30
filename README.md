# CTA Database Navigator

## Overview  
This Python terminal app lets users explore and analyze the CTA L train daily ridership data. Built as a CS 341 project at the University of Illinois Chicago, it provides commands to query ridership stats and station info from the CTA database.

## Getting Started  
Use the numbered menu options to run different analyses, such as finding stations by name, checking ridership percentages, viewing yearly/monthly data, comparing stations, and mapping nearby stops.

## Requirements  
- **SQLite3** for database queries  
- **Matplotlib** for plotting graphs and visualizations  

## Key Features  
- Search stations by partial names  
- View ridership breakdown by day type  
- List stops by line and direction  
- Analyze yearly and monthly ridership trends with optional plots  
- Compare daily ridership of two stations  
- Locate stations within a mile radius on a map  

## Database  
This app connects to the  `CTA2_L_daily_ridership.db` SQLite database to fetch data. 
Database file link: https://drive.google.com/file/d/1LlVIpJ-m1bfYTGnJRyVu-HZac-xoh0ho/view

## Notes  
- Coordinates should be within Chicago limits when searching nearby stations.  
- Many commands support data visualization using Matplotlib.

