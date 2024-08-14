# Bike Sharing Data Analysis - Dicoding Submission

This repository contains the project files for the Bike Sharing Data Analysis, completed as part of a submission to the "Belajar Analisis Data dengan Python" course. The project focuses on analyzing bike sharing data to uncover trends and insights that can inform decision-making for bike rental businesses.

## Table of Contents
- [Overview](#overview)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Technologies Used](#technologies-used)

## Overview
This project involves data analysis and visualization of bike rental data. It includes data wrangling, exploratory data analysis (EDA), and visualizations to examine the patterns in bike usage based on various factors such as weather conditions, seasons, and day type. The project was developed using Python and several libraries including Pandas, Matplotlib, Seaborn, and Streamlit.

## Project Structure
- `data/`: Contains the raw CSV files used for analysis.
- `dashboard/`: Includes the Streamlit dashboard files for interactive data visualization.
- `notebook.ipynb`: Jupyter Notebook with detailed data analysis steps.
- `README.md`: Project documentation.
- `requirements.txt`: List of dependencies required to run the project.
- `url.txt`: Contains the link for the Streamlit dashboard.

## Installation
To run this project locally, follow these steps:

1. Clone the repository:
   ```sh
   git clone https://github.com/Azerif/bikesharing-dicoding.git
   ```
2. Navigate to the project directory:
   ```sh
   cd bikesharing-dicoding
   ```
3. Install the required packages:
   ```sh
   pip install -r requirements.txt
   ```

## Usage
1. **Data Wrangling**: The data is loaded using Pandas, and cleaning operations such as dropping unnecessary columns, renaming columns, and handling missing values are performed.

2. **Exploratory Data Analysis (EDA)**: The EDA includes grouping and aggregation operations, correlation analysis, and visualizations to explore bike rental patterns.

3. **Running the Dashboard**: 
   - To launch the Streamlit dashboard, run:
     ```sh
     streamlit run ./dashboard/dashboard.py
     ```
   - You can also launch the Streamlit dashboard with url in your default web browser
     ```sh
     azrianrifq-bikesharing-dataanalysis.streamlit.app
     ``` 
   - The dashboard will open in your default web browser, allowing you to interact with the visualizations and insights derived from the data.
     
## Preview
![preview](https://github.com/user-attachments/assets/c2e4f990-4892-428d-a06c-df719c164ff4)


## Technologies Used
- **Python**: Core programming language.
- **Pandas**: Data manipulation and analysis.
- **Matplotlib**: Data visualization.
- **Seaborn**: Statistical data visualization.
- **Streamlit**: Creating the interactive web app for the dashboard.
