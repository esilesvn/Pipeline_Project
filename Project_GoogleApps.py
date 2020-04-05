import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

os.chdir(r'')

user_choice = str(input("Category or All? ")).lower()

def acquisition() :
    df = pd.read_csv('Google-Playstore-32K.csv')
    return df

def cleaning(df):
    
    #Renommer des colonnes avec des noms plus simples
    df = df.rename(columns={'App Name' : 'AppName', "Last Updated" : "LastUpdated", "Minimum Version" : "MinVers", "Latest Version" : "LatVers"})
    
    #Modification du type de valeurs et manipulation des caractères spéciaux
    df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
    df['Price'] = df['Price'].str.replace("$","")
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    df['Installs'] = df['Installs'].str.replace("+","").str.replace(",","")
    
    df['Installs'] = pd.to_numeric(df['Installs'], errors='coerce').fillna(0).astype(np.int64)
    df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce').fillna(0).astype(np.int64)
    df['AppName'] = df['AppName'].str.replace("?","").str.replace("-","").str.replace(",","").str.replace("�","").str.strip("  ").str.title()
    df['AppName'].replace('', np.nan, inplace=True)
    
    #Modification de la ligne correspondant ELEerJapenese
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

    #Suppression ligne avec valeurs inconnues
    df.drop(13504,0,inplace=True)
    
    #Suppression colonne
    df.drop(columns=['Content Rating'])

    #Suppression des valeurs nulles dans les colonnes Rating & LatVers
    df.dropna(subset=['Rating'], inplace=True)
    df.dropna(subset=['LatVers'], inplace=True)
    df.dropna(subset=['AppName'], inplace=True)
    
    #Valeurs Naan dans la colonne Price (app gratuite)
    df['Price'].replace(np.nan, '0', inplace=True)
    
    #Modification de la colonne Category
    df['Category'] = df['Category'].str.title().str.replace("_", " ").str.replace("And", "&")
    
    #Modification du format de la date
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
    

    global user_choice
    
    if user_choice == 'category' :
        
        #Will filter per Categories
        lst = df['Category'].unique().tolist()
        print("\r\n".join(lst))
        cat = str(input('Select a category in the list above:  ')).title()
        if cat not in lst : 
            raise ValueError("Selection does not exist")

        else :    
            datapercat = df[df.Category == cat]
            print(f'{datapercat.shape[0]} apps indexed in the {cat.lower()} category')
            rank = int(input("How many ranks displayed : "))
            if type(rank) != int : 
                raise ValueError("Integers only")
            elif rank > datapercat.shape[0] :
                print(f"The value should be equal or inferior to {datapercat.shape[0]} !")
            else :
                datapercat = df[df.Category == cat]
                bestrate = (datapercat.Rating >= 4)
                top10_df = datapercat.sort_values('Reviews', ascending = False).loc[bestrate].head(rank)
                count = 0
                print(f"Top 10 Apps of the {cat} category (based on rates & reviews):")
                for i in top10_df.AppName :
                    count += 1
                    print(count,"-", i)
                
            
    elif user_choice == "all" : 
        #Les pourcentages de install par category
        grouped = df.groupby('Category')['Installs'].agg('mean').reset_index()
        final = grouped.sort_values('Installs', ascending = False).head(10) #get the top 10
        
        return final

    else :
        print('Please, choose between "category" or "all".')
        
def viz(final):
    
    global user_choice
    
    if user_choice == 'all' :
        sns.set() #just to make the plot beautiful 
        fig,ax = plt.subplots(figsize=(20,10)) #hauteur 15 / largeur 8
        barchart = sns.barplot(data=final, x='Category', y='Installs') #i precise that my data is the dataframe
        plt.title('Top 10 Categories of App on Google App per installs')
    
        return barchart


if __name__ == '__main__':
    data=acquisition()
    filtered = cleaning(data)
    results = manipulation(filtered)
    viz(results)