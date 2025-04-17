"""EXPLORATORY DATA ANALYSIS - A CASES STUDY>""" 
import opendatasets as od  
import pandas as pd
#od.download("stackoverflow-developer-survey-2020") 
"""The dataset contains 4 files
* README_2020.txt - containing information about the dataset 
* survey_results_schema.csv - containing the list of questions (and 
code for each question)
* survey_results_public.csv - the full list of responses to the questions
* so_survey_2020.pdf - the list of questions

Let's load the csv files using the Pandas library. We'll use the name 
survey_raw_df for the data frame, to indicate that this is unprocessed data which 
we might clean, filter and modify to prepare a data frame that's ready 
for data analysis.
""" 
survey_raw_df = pd.read_csv("stackoverflow-developer-survey-2020/survey_results_public.csv")
print(survey_raw_df.shape)