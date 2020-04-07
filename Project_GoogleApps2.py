#Libraries
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#Initialization of the working directory
os.chdir(r'C:\Users\EliseIronhack\0323_2020DATAPAR\Labs\module_1\Pipelines-Project\google-playstore-apps') #fill with absolute path of the folder
wd = os.getcwd()

user_choice = str(input("Apps or Categories? ")).lower()

#This choice is used later in the manipulation & vizualisation functions
if user_choice == 'categories' :
    whichcolumn = str(input("Top 10 Categories based on Reviews, Rating or Installs ? ")).title()
    lst_col = ['Reviews', 'Rating', 'Installs']
    #Check if the selection is correct
    if whichcolumn not in lst_col : 
        raise ValueError("Uncorrect selection. Please select between Reviews, Rating, Installs.")
        
def acquisition() :
    """
    
    Reads a CSV file as a pandas dataframe
    Returns a dataframe
    -------
    df : dataframe containing datas imported from the csv file

    """
    
    df = pd.read_csv('Google-Playstore-32K.csv')
    return df


def cleaning(df):
    """
    
    Cleans the dataframe
    Rename columns
    Manage data types
    Modify & delete rows of missing values (according to the integrity of the remaining data)
    Remove useless column
    Manage date/time format
    
    Parameters
    ----------
    df : dataframe containing datas imported from the csv file

    Returns
    -------
    df : cleaned dataframe

    """
    
    #Rename columns with simpler names
    df = df.rename(columns={'App Name' : 'AppName', "Last Updated" : "LastUpdated", "Minimum Version" : "MinVers", "Latest Version" : "LatVers"})
    
    #Modify data types and manage strings
    df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
    df['Price'] = df['Price'].str.replace("$","")
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    df['Installs'] = df['Installs'].str.replace("+","").str.replace(",","")
    
    df['Installs'] = pd.to_numeric(df['Installs'], errors='coerce').fillna(0).astype(np.int64)
    df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce').fillna(0).astype(np.int64)
    df['AppName'] = df['AppName'].str.replace("?","").str.replace("-","").str.replace(",","").str.replace("�","").str.strip("  ").str.title()
    df['AppName'].replace('', np.nan, inplace=True)
    
    #Manage a mismatch between the values and columns (App : ELEerJapenese)
    df.iloc[6941, 1] = 'EDUCATION'
    df.iloc[6941, 2] = 4.705075264
    df.iloc[6941, 3] = 1458
    df.iloc[6941, 4] = 100000
    df.iloc[6941, 5]= '9.5M'
    df.iloc[6941, 6] = 0
    df.iloc[6941, 7] = 'Everyone'
    df.iloc[6941, 8] = '4/2/19'
    df.iloc[6941, 9] = '4.4 and up'
    df.iloc[6941, 10] = '9.0.3'

    #Remove row with uncoherent values
    df.drop(13504,0,inplace=True)
    
    #Remove columns
    df.drop(columns=['Content Rating'])


    #Remove rows when missing values in following columns : Rating, LatVers, AppName
    df.dropna(subset=['Rating'], inplace=True)
    df.dropna(subset=['LatVers'], inplace=True)
    df.dropna(subset=['AppName'], inplace=True)
    
    #Replace missing/nan values with 0 in the column Price (free apps)
    df['Price'].replace(np.nan, '0', inplace=True)
    
    #String Operation for the column 'Category'
    df['Category'] = df['Category'].str.title().str.replace("_", " ").str.replace("And", "&")
    
    #Manage date format
    df['LastUpdated'] = df['LastUpdated'].str.replace("January","1/").str.replace(",", "/").str.replace(" ", "")
    df['LastUpdated'] = df['LastUpdated'].str.replace("February","2/")
    df['LastUpdated'] = df['LastUpdated'].str.replace("March","3/")
    df['LastUpdated'] = df['LastUpdated'].str.replace("April","4/")
    df['LastUpdated'] = df['LastUpdated'].str.replace("May","5/")
    df['LastUpdated'] = df['LastUpdated'].str.replace("June","6/")
    df['LastUpdated'] = df['LastUpdated'].str.replace("July","7/")
    df['LastUpdated'] = df['LastUpdated'].str.replace("August","8/")
    df['LastUpdated'] = df['LastUpdated'].str.replace("September","9/")
    df['LastUpdated'] = df['LastUpdated'].str.replace("October","10/")
    df['LastUpdated'] = df['LastUpdated'].str.replace("November","11/")
    df['LastUpdated'] = df['LastUpdated'].str.replace("December","12/")
    df['LastUpdated'] = df['LastUpdated'].str.replace("2019","19")
    df['LastUpdated'] = df['LastUpdated'].str.replace("2018","18")
    df['LastUpdated'] = df['LastUpdated'].str.replace("2017","17")
    df['LastUpdated'] = df['LastUpdated'].str.replace("2016","16")
    df['LastUpdated'] = df['LastUpdated'].str.replace("2015","15")
    df['LastUpdated'] = df['LastUpdated'].str.replace("2014","14")
    df['LastUpdated'] = df['LastUpdated'].str.replace("2013","13")
    df['LastUpdated'] = df['LastUpdated'].str.replace("2012","12")
    df['LastUpdated'] = df['LastUpdated'].str.replace("2011","11")
    df['LastUpdated'] = df['LastUpdated'].str.replace("2010","10")
    df['LastUpdated'] = pd.to_datetime(df['LastUpdated'], format = "%m/%d/%y")
    
    return df

def manipulation(df): 
    """
    
    User's choice will guide the data manipulation
    Apps: 
        Will filter the Top 10 Apps of the specified category based on reviews & rating
    Categories : 
        Will return a graph of the Top 10 Category based on installs 
    
    Parameters
    ----------
    df : cleaned dataframe

    Raises
    ------
    ValueError
        1. Specified category must be in the list of proposition (Copy/Paste to be sure)
        2. Displayed ranks must be an integer
        3. Displayed ranks cannot be higher than the total number of apps indexed
        
    Returns
    -------
    final : Results according to user's choice

    """

    global user_choice
    global whichcolumn
    
    if user_choice == 'apps' :
        
        #Will filter per Categories
        lst = df['Category'].unique().tolist()
        #Print a list of the categories
        print("\r\n".join(lst))
        cat = str(input('Select a category in the list above:  ')).title()
        
        
    
        #Checks if the category selected exists in the dataframe
        if cat not in lst : 
            raise ValueError("Selection does not exist")

        else :    
            
            datapercat = df[df.Category == cat]
            #Returns the numbers of Apps in the specified Category
            print(f'{datapercat.shape[0]} apps indexed in the {cat.lower()} category')
            
            #Asks for the number of ranks to be returned
            rank = int(input("How many ranks displayed : "))
            #Checks if the value selected is an integer and if the number is in the right interval of existing values
            if type(rank) != int : 
                raise ValueError("Integers only")
            elif rank > datapercat.shape[0] :
                print(f"The value should be equal or inferior to {datapercat.shape[0]} !")
            else :
                
                bestrate = (datapercat.Rating >= 4) #Best Apps : we chose to filter the apps with a rating superior to 4 (on 5)
                final = datapercat.sort_values('Reviews', ascending = False).loc[bestrate].head(rank) #Will sort the selection based on  the number of reviews
                count = 0
                print(f"Top 10 Apps of the {cat} category (based on rates & reviews):")
                for i in final.AppName :
                    count += 1
                    print(count,"-", i) #Returns the [specified number] Top Apps in the category
           
                return final
            
    elif user_choice == "categories" : 
        #Groups - 3 choices : Rating, Reviews, Installs
        
        #Groups the [Specified variable] by Categories - Aggregation based on mean
        grouped = df.groupby('Category')[whichcolumn].agg('mean').reset_index()
        #Sorts values and returns the 10 firsts
        final = grouped.sort_values(whichcolumn, ascending = False).head(10) #get the top 10
        
        return final

    else :
        print('Please, choose between "apps" or "categories".')
        
def viz(final):
    """
    
    If user's choice is categories, will produce a barchart of the Top 10 Categories of App on Google App per Installs'
    If user's choice is apps, will produce a brachart of the Top Apps in the specified category'
    Parameters
    ----------
    final : grouped and sorted values

    Returns
    -------
    barchart : 
        Top 10 Categories of App on Google App by installs, reviews or rating
        Top 10 Apps in the specified category

    """
    global user_choice
    global whichcolumn
    
    
    if user_choice == 'categories' :
        sns.set() 
        fig,ax = plt.subplots(figsize=(20,10)) 
        barchart = sns.barplot(data=final, x='Category', y=whichcolumn) 
        plt.title(f'Top 10 Categories of App on Google App by {whichcolumn.lower()}')
    
        return barchart
    
    elif user_choice == 'apps' :
        cat = ''.join(final.Category.unique())
        sns.set() 
        fig,ax = plt.subplots(figsize=(25,10)) 
        barchart = sns.barplot(data=final, x='AppName', y='Reviews') 
        plt.title(f'Top 10 Apps on Google App for the {cat.lower()} category')
        
        return barchart

def save_viz(plot):
    """
    

    Will save the barchart produced in a 'Output' folder (create it if does not exist)
    ----------
    plot : barchart of Top 10 Categories of App on Google App by installs, reviews or rating

    Returns
    -------
    None.

    """
    global user_choice
    global whichcolumn
    
    if user_choice == 'categories' :
        fig = plot.get_figure()
        foldername = 'output'
        
        #Checks if the path (Output Folder already exists)
        if not os.path.exists(os.path.join(wd, foldername)):  
            os.mkdir(os.path.join(wd, foldername))
        
        output_path = os.path.join(wd, foldername)
        fig.savefig(output_path + f'/Top 10 Categories of App on Google App by {whichcolumn.lower()}.png')


    elif user_choice == 'apps' :
        fig = plot.get_figure()
        foldername = 'output'
        
        #Checks if the path (Output Folder already exists)
        if not os.path.exists(os.path.join(wd, foldername)):  
            os.mkdir(os.path.join(wd, foldername))
        
        output_path = os.path.join(wd, foldername)
        fig.savefig(output_path + f'/Top 10 Categories of App on Google App per category.png')
        
        
#EXECUTION
if __name__ == '__main__':
    data=acquisition()
    filtered = cleaning(data)
    results = manipulation(filtered)
    visual = viz(results)
    save_viz(visual)