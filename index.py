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
#print(survey_df["Gender"].value_counts())
 
import numpy as np
survey_df.where(~(survey_df.Gender.str.contains(";", na=False)), np.nan, inplace=True) 

"""We've now cleaned up and prepared the dataset for analysis. Let's 
take a look at sample of roaws from the data frame
"""
#print(survey_df.sample(10))
#print(survey_df.describe())  

"""
Exploration Analysis and Visualization 

Before we can ask interesting questions about the survey responses, it would help 
to understand what the deographics i.e. country, age, gender, education level, employment 
etc of the respondents look at. It's important to explore these variables in order to 
understand how representative the surveyu is of the worldwide programming community as 
as survey of this scale generally tends to have selection bias. 

Let's begin by importing matplotlib and seaborn
""" 
import matplotlib
import matplotlib.pyplot as plt 
import seaborn as sns 

sns.set_style("darkgrid")  
matplotlib.rcParams["font.size"] = 14 
matplotlib.rcParams["figure.figsize"] = (9, 5)  
matplotlib.rcParams["figure.facecolor"] = "#00000000" 

"""Country 
Let's look at the number of countries from which there are responses in the survey, 
and plot the 10 countries with the highest number of responses.  
"""  
res = survey_df.Country.nunique()

"""We can identify the countries with the highest number of respondents 
using the values_counts method.
"""
top_countries = survey_df.Country.value_counts().head(15) 

"""We can visualize this information using a bar chart"""
""" plt.figure(figsize=(12, 6)) 
plt.xticks(rotation=75) 
plt.title(schema.Country) 
sns.barplot(x=top_countries.index, y=top_countries)  """

"""
It appears that a disproportionately high number of respondents are from USA & India - 
which one might expect since these countries have the highest populations (Apart from China), 
and since the Survey is in English, which is the common language used by professionals 
in US, India and UK.
""" 


"""Age  
The distribution of the age of respondents is another important factor to look
at, and we can use a histogram to visualize it.
"""  
""" plt.figure(figsize=(12, 6)) 
plt.title(schema.Age) 
plt.xlabel("Age")
plt.ylabel("Number of respondents") 
plt.hist(survey_df.Age, bins=np.arange(10, 80, 5), color="purple") """ 

"""
It appears that a large percentage of respondents are in the age range 
of 20-40, which is somewhat representative of the programming community in 
general, as a lot of young people have taken up computer as their field of study 
or profession in the last 20 years. 
"""

"""Gender 
Let's look at the Distribution of responses for the Gender. It's a well 
known fact that women and non-binary genders are underrepresented in the 
programming community, so we might expect to see a skewed distribution here. 
""" 
gender_counts = survey_df.Gender.value_counts()  
#gender_counts = survey_df.Gender.value_counts(dropna=False) 

"""
A pie chart would be a good way to visualize the distribution 
""" 
""" plt.figure(figsize=(12, 6)) 
plt.title(schema.Gender)
plt.pie(gender_counts, labels=gender_counts.index, autopct="%1.1f%%")  """

"""Only about 8% of survey respondents who have answered the question 
identify as women or non=binary. The number is lower than the overall 
percentage of women & binary gender in the programming community - which is 
estimated to to be around 12%  
"""

"""Education Level  
Formal education in computer science is oftne considered an important requirement 
of becoming a programmer. Let's see if this is indeed the cases, especially since 
there are many free resources & tutorials online to learn programming. We'll 
use a horizontal bar plot to compare education levels of respondents. 
""" 
""" plt.figure(figsize=(12, 6))
sns.countplot(y=survey_df.EdLevel) 
plt.xticks(rotation=75)
plt.title(schema["EdLevel"]) 
plt.ylabel(None)  """

"""It appears that well over half of the respondents hold a bachelor's  
or master's degree, so most programmers definitely seem to have some college
education, although it's not clear from this graph alone if they hold a 
degree in computer science. 
"""

""""
Undergraduate Major
Let's also plot undergraduate majors, but this time, we'll 
convert the numbers into percentages and sort by precentage valaues to make it 
easier to visualize the order. 
""" 
""" plt.figure(figsize=(12, 6))
undergrad_pct = survey_df.UndergradMajor.value_counts()  * 100 / survey_df.UndergradMajor.count() 
sns.barplot(x = undergrad_pct, y=undergrad_pct.index) 
plt.ylabel(None) 
plt.xlabel("Percentage") """

"""
It turns out 40% of programmers holding a college degree have a field of study 
other than computer sciene - which is very encouraging. This seems to suggest that 
what while college education is helpful in general, you do not need to pursue 
a major in computer science to become a successful programmer. 
""" 


"""Employment
Freelancing or contract work is a common choice among programmers, so 
it would be interesting to compare the breakdown between full-time, 
part-time and freelance work. Let's visualize the data from Employment 
column"""
""" plt.figure(figsize=(12, 9)) 
(survey_df.Employment.value_counts(normalize=True, ascending=True) * 100).plot(kind="barh", color="g") 
plt.title(schema.Employment) 
plt.xlabel("Percentage")  """

"""It appears that close to 10% of respondents are employed part time 
or as freelancers. 
"""

"""The DevTtype field contains information about the roles held by 
respondents. Since it allows multiple answers, the column contains lists 
of values seperated by ";", which makes it a bit harder to analyze directly. 
"""
print(schema.DevType) 
print(survey_df.DevType.value_counts()) 

"""
Let's define a helper function which turns a column containing lists of values 
(like survey_df.fevType) into a data frame with one column for each possible 
option""" 

def split_multicolumn(col_series: pd.Series): 
    result_df = col_series.to_frame()  
    options = [] 

    # Iterate over the column 

    for idx, value in col_series[col_series.notnull()].items(): 
        # Breake each value into list of options 
        for option in value.split(";"): 
            # Add the option as a column to result 
            if not option in result_df.columns:
                options.append(option) 
                result_df[option] = False  
            # Mark the value in the option columns as True 
            result_df.at[idx, option] = True  
    return result_df[options] 

dev_type_df = split_multicolumn(survey_df.DevType) 

"""The dev_type_df has one column for each option that can be selected as 
a response. if a selected respondent has the option in the column it is True 
otherwise it is False. 

We ca now use the column-wise totals to identify the most common roles 
""" 
dev_type_totals = dev_type_df.sum().sort_values(ascending=False) 
print(dev_type_totals) 

"""As one might expect, the most common roles include "Developer"  
in the name. 
"""

"""Asking and Answering Questions 
""" 

"""
Q.Which were the most popular programming languages in 2020? 

To answer this, we can use the LanguageWorkedWith column. Similar to DevType, 
respondents were allowed to choose multiple options
""" 
print(survey_df.LanguageWorkedWith) 

"""First, we'll split this column into a data frame containing a column each 
of each language listed in the options. 
""" 
languages_worked_df = split_multicolumn(survey_df.LanguageWorkedWith) 


"""it appears that a total of 25 languages were included among the options. 
Let's aggregate them to identify the percentage of respondents who 
selected each langauge
"""
languages_worked_percentages = languages_worked_df.mean().sort_values(ascending=False)  

"""We can plot this information using a horizontl bar chart""" 
plt.figure(figsize=(12, 12)) 
sns.barplot(x=languages_worked_percentages, y=languages_worked_percentages.index)
plt.title("Langues used in the past year") 
plt.xlabel("Count") 

"""Perhaps not surprisingly, JavaScript & HTML/CSS comes out on top 
as web development is one of the most sought skills today and it's also 
happens to be one of the easiest to get started with. SQL is necessary for working 
with relational databases, so it's no surprise that most programmers work with 
SQL on a regular basis. For other forms of development, Python seems to be the 
popular choice, beting out Java, which was the industry standard for server 
and application development for over 2 decades.
""" 

"""Which languages are most people interested to learn over the next 
year? 

For this we can use the LanguageDesireNextYear column with similar 
processing as the previous one.
"""  
languages_interested_df = split_multicolumn(survey_df.LanguageDesireNextYear) 
languages_interested_percentages = languages_interested_df.mean().sort_values(ascending=False)
plt.figure(figsize=(12, 12)) 
sns.barplot(x=languages_interested_percentages, y=languages_interested_percentages.index)
plt.title("Langues people are interested in learning over the next year.") 
plt.xlabel("Count")  

plt.show()