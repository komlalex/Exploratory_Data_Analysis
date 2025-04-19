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
#print(schema_raw["YearsCodePro"]) 

"""We've now loaded the dataset, and we're ready to move on to the next step 
of processing & cleaning the data for our analysis. 
"""


"""Data Preparation &  Cleaning 
While the survey responses contain a wealth of information, we'll limit our analysis to 
the following area:
* Demographics of the survey respondents & the global programming community 
* Distribution of programming skills, experiences and preferences  
* Employment-related information, prefeences & opinions
"""
selected_columns = [
    # Demographics
    "Country", 
    "Age", 
    "Gender", 
    "EdLevel", 
    "UndergradMajor", 
    # Programming experience 
    "Hobbyist",
    "Age1stCode", 
    "YearsCode",  
    "YearsCodePro", 
    "LanguageWorkedWith", 
    "LanguageDesireNextYear", 
    "NEWLearn", 
    "NEWStuck", 
    # Employment 
    "Employment", 
    "DevType", 
    "WorkWeekHrs", 
    "JobSat", 
    "JobFactors", 
    "NEWOvertime", 
    "NEWEdImpt"
] 

#print(len(selected_columns))  

"""
Let's extract a copy of the data from these columns into a new data frame survey_df, 
which we can continue to modify further without further affecting 
the original data frame.
""" 
survey_df = survey_raw_df[selected_columns].copy() 
schema = schema_raw[selected_columns] 

"""let's view some basic information about the data frame""" 
#print(survey_df.shape)
#print(survey_df.info()) 
#print(schema.shape) 

"""Most columns have the data type object, either because they contain values of different 
types, or they contain empty values, which are represented using NaN. 
It appears that every column contains empty values, since Non-Null count for every column is lower 
than the total number of rows (64461). We'll need to deal with empty values and manually adjust the 
data type of each column on a case-by-case basis. 

Only two columns were detected as numeric (Age and WorkWeekHrs), even though there are a few 
other columns which have mostly numeric values. To make our analysis easier, let's 
convert some other columns into numeric data types, while ignoring any non-numeric 
value (they get converted to NaNs) 
""" 
survey_df["Age1stCode"] = pd.to_numeric(survey_df.Age1stCode, errors="coerce") 
survey_df["YearsCode"] = pd.to_numeric(survey_df.YearsCode, errors="coerce")
survey_df["YearsCodePro"] = pd.to_numeric(survey_df.YearsCodePro, errors="coerce")  

"""let's view some basic statistics about the numeric columns"""
#print(survey_df.describe()) 

"""There seems to be a problem with the age column, as the minimum values is 1 and the 
max value is 279. This a common issue with surveys: responses may contain invalid values due to 
accidental or intentional erros while responding. A simple fix would be to ignore the rows 
where the value in the age column is higher than 100 years or lower than 10 years as 
invalid survey responses. This can be done using the .drop method. 
""" 
survey_df.drop(survey_df[survey_df.Age < 10].index, inplace= True)
survey_df.drop(survey_df[survey_df.Age > 100].index, inplace=True) 

"""
The same holds true for WorkWeekHrs. Let's ignore entries where the value for 
the column is higher than 140 hours (~20 hours per day) 
""" 
survey_df.drop(survey_df[survey_df.WorkWeekHrs > 140].index, inplace=True) 

""" 
The gender columns allows picking options, but to simplify our analysis, we'll 
remove values containing more than one option
""" 
print(survey_df["Gender"].value_counts())
 
import numpy as np
survey_df.where(~(survey_df.Gender.str.contains(";", na=False)), np.nan, inplace=True) 

"""We've now cleaned up and prepared the dataset for analysis. Let's 
take a look at sample of roaws from the data frame
"""
print(survey_df.sample())
#print(survey_df.describe()) 