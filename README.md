# RainfallForecast

## Leveraging Earth Observation Data for Informed Agricultural Decision-Making

RainfallForecast is a Django-based web application designed to empower farmers and agricultural experts with insightful, real-time data. By utilizing Earth observation data, the platform helps users make better decisions for crop management, resource allocation, and land monitoring.

### Installation Guide

To get started with RainfallForecast, ensure you have the following prerequisites:

1. **Python** (version 3.x recommended)
2. **Django** (latest version)

Follow these steps to set up the project:

1. Clone the repository:
   ```bash
   git clone <repository-link>


## RainfallForecast

### High-Level Summary

RainfallForecast is a web application designed to assist farmers in making informed decisions about planting and harvesting schedules. By visualizing agricultural data based on user-selected areas, RainfallForecast addresses the challenges farmers face, such as unpredictable weather patterns, extreme weather conditions, and the transfer of knowledge to new generations.

Traditionally, farmers have relied on experience and intuition, but RainfallForecast leverages easily accessible data to provide a user-friendly interface. It is designed to be intuitive, even for users with limited computational skills, enabling access to valuable insights from scientific and governmental sources.

### Key Features

- **Real-Time Data Visualization**: Agricultural data, including weather trends, is visualized on a map for a specific region selected by the user.
- **Average Daily Rainfall**: The current stage of development incorporates rainfall data from **ClimateSERV**, using historical data from the past two years.
- **User-Friendly Interface**: RainfallForecast integrates a simple, easy-to-use mapping tool for farmers to delineate regions and predict rainfall.

### How It Works

1. Upon loading the website, users are prompted to grant permission for accessing their GPS location.
2. An integrated map displaying the user’s surrounding area will load, allowing users to delineate a specific region of interest by drawing a polygon on the map and specifying a date.
3. RainfallForecast retrieves and analyzes the average daily rainfall data for the designated area over the past two years.
4. The application then furnishes a prediction of rainfall probability for the selected date, with results visualized by color-coding the drawn polygon. Different colors represent varying levels of rainfall probability, making the data easy to understand.

RainfallForecast provides an accessible way for farmers to incorporate scientific data into their decision-making processes, offering an invaluable tool for managing the unpredictable challenges of agriculture.

More info: documentation-pdf
