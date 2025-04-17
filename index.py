"""EXPLORATORY DATA ANALYSIS - A CASES STUDY>""" 
import opendatasets as od  
import pandas as pd
#od.download("stackoverflow-developer-survey-2020") 
"""The dataset contains 4 files
* README_2020.txt - containing information about the dataset 
* survey_results_schema.csv - containing the list of questions (and 
code for each question)
* survey_results_public.csv - the full list of responses to the questions

Let's load the csv files using the Pandas library. We'll use the name 
survey_raw_df for the data frame, to indicate that this is unprocessed data which 
we might clean, filter and modify to prepare a data frame that's ready 
for data analysis.
""" 
survey_raw_df = pd.read_csv("stackoverflow-developer-survey-2020/survey_results_public.csv") 

"""The dataset contains over 64,000 responses to 60 questions (although many 
questions are optional). The responses have been anonymized and there's no 
personally identifiable information available to us - although each respondent has 
been assigned a randomized respondent ID. 

Let's view the list of columns"""
#print(survey_raw_df.columns)

"""It appears that short codes are used as column names. 

We can refer to the schema file to see the full text of each question. The schema file 
contains only two columns: Column and QurstionText, so we can load it as 
Pandas Series with Column as the index of the series nad QuestionText as the value. 
"""
schema_fname = "stackoverflow-developer-survey-2020/survey_results_schema.csv"
schema_raw = pd.read_csv(schema_fname, index_col="Column").QuestionText 
#print(schema_raw) 

"""We can now use schema_raw to retrieve the full question text for any column 
in surevy_raw_df 
"""
print(schema_raw["YearsCodePro"])