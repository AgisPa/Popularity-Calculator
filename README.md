# Popularity-Calculator
This is an automated AI tool that produces and evaluates popularity related data regarding inputed terms of interest.

# Popularity-Calculator

## Overview

Popularity-Calculator is an AI tool designed to produce and evaluate data regarding a term of interest over an abstract time frame. The tool utilizes the web browsing package called Selenium in conjunction with the OpenAI API for information retrieval and evaluation.

## Prerequisites

Before running the Popularity-Calculator, ensure that you have the following components installed:

- **Selenium**: Popularity-Calculator uses Selenium for web scraping. Install the WebDriver for your internet browser. (e.g., ChromeDriver)
- **OpenAI API**: Acquire your OpenAI API key and replace the placeholder in the code with your actual key.
- **Python Packages**: Install required Python packages using the provided `requirements.txt` file.

## Usage

To run the main function of the Popularity-Calculator, input the term of interest and your personal OpenAI API key. Additionally, the algorithm can be further tuned using the following parameters:

- **Number of Terms**: Set the number of terms searched for regarding the term of interest.
- **Start Time Altering Parameter**: Adjust the starting row for the analysis.
- **Trust Parameter**: Account for the percentage of guidelines used for the evaluation process.
- **Time Increment Parameter**: Split the time frame into segments according to its value.

## AI Guidelines

The Popularity-Calculator employs a set of evaluation criteria when interacting with the GPT-3.5-turbo model. These criteria include factors such as relevance, clarity, accuracy, objectivity, and others. The trust parameter influences the percentage of guidelines considered during the evaluation.

## Time Frame Data

A separate `.csv` file named `TimeFrame.csv` is included in the package. This file stores the time frame data required for analysis.

## Code Structure

The code is divided into two separate files:

1. **AI_popularity_calculator.py**: Contains the main functionality for retrieving and evaluating data.
2. **Google_Search.py**: Handles Google searches and extraction of popular site titles.

## Additional Notes

- Ensure that the appropriate WebDriver for your internet browser is installed for Selenium to function correctly.
- The program utilizes the Python package `pandas` to save the resulting data into a `.csv` folder in the local repository.


