<img src="https://bit.ly/2VnXWr2" alt="Ironhack Logo" width="100"/>

# Data Pipeline - Google Apps 
*Elise*

*Data Analytics Bootcamp, Paris, March 2020*

## Content
- [Pipeline Description](#pipeline-description)
- [Feedback](#feedback)
- [Links](#links)

## Pipeline Description

1. Data Collection & Acquisition

The original dataset contains informations on 32000 apps from the Google Play App Store, such as : 
  - Name of the App
  - Category
  - Rating
  - Reviews
  - Installs
  - Size
  - Price
  - Content Rating
  - Last Updated
  - Minimum Version
  - Latest Version

The program imports the dataset from the .csv file into a pandasdataframe for a better manipulation in the following steps. 

2. Data Cleaning

This step was elaborated from the different problems encountered during the process, turns out as : 
  - Rename the columns with simpler names
  - Manage the different types of values contained in the dataframe
  - Manage & correct the values 
        (simpler name, uppercase, lowercain, special characters) 
  - Modify a specific row (mismatch between values and columns)
  - Remove rows with nan values in the following columns : Rating, AppName, LatVers
  - Modify the format of date

*In case of missing values, when enough informations were provided, the application wasn't removed from the database but corrected. In a case of lack of informations, or an essential information mssing (AppName for example), the application and its informations were removed from the database.

3. Data Manipulation

2 manipulations can be performed on the dataframe : 

- "Apps" - Apps ranked based on the reviews and rates :

The user will chose a category from the list of category available. Then, the user will chose a number corresponding to the number of ranked app he want to see. If the user chose '10', the top ten of the apps (reviews and rates) of the selected category will be returned. 
      
      
 - "Categories"  - Top 10 Categories based on the installs, reviews or rating :
 
This choice will aggregate and sort the values of installs per Category to generate a Top 10 of Category based on the installs, reviews or rating. 
      
4. Data Vizualisation

Generate a barchart based on the results of the previous manipulation described above. The graph, saved in a folder "Output" (created if doesn't exist), will contain a Top 10 of Categories based on the installs, reviews or rating or a Top Apps of the specified category (depending of the choices made). 

## Feedback
1. Obstacles encoutered

The hardest part of the datacleaning would be the first step and the first decision to be made : from where do I begin ? The following problems and errors will be the clues for the design of the process. When the columns have appropriate names, when the data types has been managed, the main issue is the missing values. Some errors of mismatched values between columns (Numbers of reviews in the wrong column) can be corrected when there is enough informations. However, when there is a lack of essential informations (for example no app name), the app and its informations were removed from the dataset. The limit between "correcting" and "removing" is therefore arbitrary at this step of the work.  

2. Lessons learned

Pandas is a really complete tool to clean and manipulate large datasets, it offers a lot of possibilities to manage and correct errors. 

The steps of the cleaning should be well-organised and splited, mainly when rows are removed and the shape of the dataframe shape changes. The modification of the shape should stay in mind when manipulating. 

Checking for errors in case of inputs was made by testing the possibilities. "What if I put a integer if I wanted a string value ?" for example. Therefore, it is needed to manage the type of input wanted (what type? is there a range for the value? a limit ?). Improvments could be made in the case of the list of category and the input (the specified category should be strictly similar to the category suggested, if not, a error will be raised). 


## Links

- [Repository](https://github.com/esilesvn/Pipeline_Project)
- [Slides](https://docs.google.com/presentation/d/1cxV6CXly19G53kUpPogYzULguAA2ONOO84Y1_7zgKxk/edit?usp=sharing)


