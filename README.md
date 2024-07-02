# Product Price Monitor

## Overview

The Product Price Monitor is a web scraping project that utilizes the BeautifulSoup library to extract product information from a specified link. The primary goal is to monitor product prices and send email alerts when the current price drops below a desired threshold. Additionally, the project includes features to store price drop data in both CSV files and an SQL database.

## Features

1. **Web Scraping with BeautifulSoup**:
   The project uses BeautifulSoup for parsing HTML and extracting relevant data, including Product Title, Price, and Availability from the provided link.

2. **Email Alerts**:
   The code checks if the current price is less than the desired price, and if so, it sends out email alerts using the 'smtplib' library.

3. **Data Extraction with 'requests'**:
   The 'requests' library is employed to extract data from the specified link, providing the necessary information for monitoring product prices.

4. **Price Drop Storage - CSV**:
   If a price drop occurs, the data is stored in a CSV file using the 'csv' library. This facilitates easy tracking and analysis of historical price changes.

5. **Price Drop Storage - SQL**:
   In addition to CSV storage, the project features functionality to store price drop data in an SQL database. This is achieved by importing the 'pymysql' library.

6. **Scheduled Execution**:
   The code is designed to run at regular intervals (every 5 minutes), ensuring continuous monitoring of product prices. This scheduling is implemented using the 'time' library.

## Prerequisites

Before running the code, make sure to install the necessary Python libraries by executing the following command:


## Configuration

1. Update the `link` variable in the code with the URL of the product you want to monitor.
2. Configure email settings such as SMTP server, sender/receiver email addresses, etc., in the code.
3. Adjust the desired price threshold according to your preferences.

## Usage

To run the script:

The script will execute at regular intervals, checking for price drops and sending email alerts when applicable. Price drop data will be stored both in CSV files and an SQL database for further analysis.

Feel free to customize the code to suit your specific needs and enhance the project based on additional features you may require.
