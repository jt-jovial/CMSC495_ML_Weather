"""
Created by: Keri Lloyd
Date Created: April 15, 2022
Edited by: Amanda Wheland
Date Edited: April 16, 2022
Edited by: Keri Lloyd
Date Edited: April 21, 2022
Class: CMSC 495 7381
Purpose: This program is part of a larger Machine Learning group project. Methods edited for merging with front end.
"""

import random
import numpy as np
import pandas as pd
from sklearn import tree
from sklearn.neighbors import KNeighborsClassifier

# Read in data
df = pd.read_csv("static/Fairbanks.csv", header=[0])

# Replace T (trace) values with 0.01 to indicate a trace amount
df['Precipitation'] = df['Precipitation'].replace('T', 0.01)
df['New Snow'] = df['New Snow'].replace('T', 0.01)
df['Snow Depth'] = df['Snow Depth'].replace('T', 0.01)

# Cast Precipitation, New Snow, and Snow Depth to float64 (they were initially objects)
df['Precipitation'] = df['Precipitation'].apply(np.float64)
df['New Snow'] = df['New Snow'].apply(np.float64)
df['Snow Depth'] = df['Snow Depth'].apply(np.float64)

# Initialize factor for test_program(). Only needed if testing without frontend
factor = 0

def season_predict(temp):
    """ Season selection, used for Temperature method for Menu option 1 """
    # Assign features (X) and target (y)
    X = df[['Average']]
    y = df['Season']

    # K-Nearest Neighbors model, 72% accuracy
    knn = KNeighborsClassifier(n_neighbors=12)
    # Fit the data to the model, then predict using given temperature
    knn.fit(X.values, y)
    season = knn.predict([[temp]])
    # Seasons: 0 == Winter, 1 == Spring, 2 == Summer, 3 == Fall
    # remove brackets from season
    for i in season:
        season = i
    return season
    

# Season will come from season_predict()
def temperature(temp, season, daylight, hours=None):
    """ Temperature method for Menu option 1 """
    if season == 0:
        # Isolate winter to narrow down the target month
        df_season = df.loc[df['Season'] == 0]
        m_range = (210, 720)  # Winter daylight hour range in minutes
        # Range in hours for input request - 3.5-12.0
    elif season == 1:
        # Isolate spring to narrow down the target month
        df_season = df.loc[df['Season'] == 1]
        m_range = (720, 1140)  # Spring daylight hour range in minutes
        # Range in hours for input request - 12.0-19.0
    elif season == 2:
        # Isolate summer to narrow down the target month
        df_season = df.loc[df['Season'] == 2]
        m_range = (840, 1320)  # Summer daylight hour range in minutes
        # Range in hours for input request - 14.0-22.0
    elif season == 3:
        # Isolate fall to narrow down the target month
        df_season = df.loc[df['Season'] == 3]
        m_range = (420, 840)  # Fall daylight hour range in minutes
        # Range in hours for input request - 7.0-14.0

    # If the user has a preference of number of daylight hours, their hours will be converted to minutes
    if daylight == 1: # User has preference
        minutes = hours * 60 # Need to add validation based on seasonal m_range in frontend      
    elif daylight == 2: # User has no preference
        minutes = random.randint(m_range[0], m_range[1]+1)
        
    # Assign features (x) and target (y)
    X = df_season[['Average', 'Daylight']]
    y = df_season['Month']

    # Decision Tree model, 84% accuracy
    dtree = tree.DecisionTreeClassifier()
    # Fit the data to the model, then predict using given temperature and daylight in minutes
    dtree.fit(X.values, y)
    month_predict = dtree.predict([[temp, minutes]])
    # Remove brackets from month
    for i in month_predict:
        month_predict = i
    return month_predict


def snowfall(snow, daylight, hours=None):
    """ Snowfall method for Menu option 2 """
    # If the user has a preference of number of daylight hours, their hours will be converted to minutes
    if daylight == 1: # User has preference
        minutes = hours * 60 # Need to add validation in frontend; hours must be between 3.5-18.5   
    elif daylight == 2: # User has no preference
        minutes = random.randint(210, 1110)

    # Assign features (X) and target (y)
    X = df[['Snow Depth', 'Daylight']]
    y = df['Month']
    # Decision Tree model, 95% accuracy
    dtree = tree.DecisionTreeClassifier()
    # Fit the data to the model, then predict using given snowfall amount and daylight in minutes
    dtree.fit(X.values, y)
    month_predict = dtree.predict([[snow, minutes]])
    # Remove brackets from month
    for i in month_predict:
        month_predict = i
    return month_predict


def daylight_hours(hours, choice=3):
    """ Daylight hours method for Menu option 3 """
    minutes = hours * 60      
    # Once minutes are calculated, a season can be determined
    # Winter: 210-419, Fall/Winter: 420-719, Fall/Spring: 720-840, Spring/Summer: 841-1140, Summer: 1140-1320
    # Winter: min < 420, Summer: 1140 < min <= 1320
    # Fall/Winter: 420 <= min < 720, Fall/Spring: 720 <= min <= 840, Spring/Summer: 840 < min <= 1140
    if minutes < 420:
        season = 0  # Winter automatically chosen (less than 7 hours)
    elif 420 <= minutes < 720:  # This range falls between 2 seasons (7-12 hours, Fall/WInter)
        if choice == 1:
            season = 3  # Fall
        elif choice == 2:
            season = 0  # Winter
        elif choice == 3:
            season = np.random.choice([3, 0])  # Will randomly choose between 3 and 0
    elif 720 <= minutes <= 840:  # This range falls between 2 seasons (12-14 hours, Spring/Fall)
        if choice == 1:
            season = 1  # Spring
        elif choice == 2:
            season = 3  # Fall
        elif choice == 3:
            season = np.random.choice([1, 3])  # Will randomly choose between 1 and 3
    elif 840 < minutes <= 1140:  # This range falls between 2 seasons (14-19 hours, Spring/Summer)
        if choice == 1:
            season = 1  # Spring
        elif choice == 2:
            season = 2  # Summer
        elif choice == 3:
            season = np.random.choice([1, 2])  # Will randomly choose between 1 and 2
    elif 1140 < minutes <= 1320:
        season = 2  # Summer automatically chosen (19-22 hours)
        
    # Assign features (X) and target (y)
    X = df[['Season', 'Daylight']]
    y = df['Month']
    # Decision Tree model, 95% accuracy
    dtree = tree.DecisionTreeClassifier()
    # Fit the data to the model, then predict using given season and daylight in minutes
    dtree.fit(X.values, y)
    month_predict = dtree.predict([[season, minutes]])
    # Remove brackets from month
    for i in month_predict:
        month_predict = i
    return month_predict


def northern_lights(daylight, snowfall_pref, hours=None, snow=None):
    """ Northern Lights method for Menu option 4 """
    print('The best time to see the Northern Lights in Fairbanks, AK is between August and April!')
    # Isolate dataframe to months between August and April
    df_nl = df.loc[df['Month'].isin([8, 9, 10, 11, 12, 1, 2, 3, 4])]

    # If the user has a preference of number of daylight hours, their hours will be converted to minutes
    if daylight == 1: # User has preference
        minutes = hours * 60 # Need to add validation in frontend; hours must be between 3.5-16.5  
    elif daylight == 2: # User has no preference
        minutes = random.randint(210, 990)

    # if snowfall_pref == 1, the user entered a value for snow that will be accepted
    # if snowfall_pref == 2, a random snow depth will be generated between 0-24 inches
    if snowfall_pref == 2:
        snow = random.randint(0, 24)

    # Assign features (X) and target (y)
    X = df_nl[['Snow Depth', 'Daylight']]
    y = df_nl['Month']
    # Decision Tree model, 95% accuracy
    dtree = tree.DecisionTreeClassifier()
    # Fit the data to the model, then predict using given season and daylight in minutes
    dtree.fit(X.values, y)
    month_predict = dtree.predict([[snow, minutes]])
    # Remove brackets from month
    for i in month_predict:
        month_predict = i
    return month_predict


def test_program(factor):
    """ While loop for backend testing of Main Menu """
    # Months dictionary for testing without frontend:
    months = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August',
          9: 'September', 10: 'October', 11: 'November', 12: 'December'} 
    # Variables for testing without frontend:
    temp = 50
    daylight = 1
    hours = 16
    snow = 2
    snowfall_pref = 2 
    while factor != 5:
        print('What is the most important factor to you when visiting Fairbanks, AK?')
        print('1. Temperature\n2. Snowfall\n3. Number of Daylight hours\n4. See the Northern Lights\n5. Exit')
        # Try/except block to ensure input is only an integer between 1-5
        try:
            factor = int(input('Enter 1-4 or 5 to exit: '))
            # Temperature is chosen as priority 
            if factor == 1:
                # Run the temperature model method
                season = season_predict(temp)
                print(season)
                month = temperature(temp, season, daylight, hours)
            elif factor == 2:
                # Run the snowfall model method
                month = snowfall(snow, daylight, hours)
            elif factor == 3:
                # Run the daylight_hours model method
                month = daylight_hours(hours)
            elif factor == 4:
                # Run the northern_Lights model method
                month = northern_lights(daylight, snowfall_pref, hours)
            elif factor == 5:
                exit()
            else:
                # If any number besides 1-5 is entered, the user will receive this error message
                print('Invalid input. You must choose an integer between 1-5.\n')
                continue
        except (ValueError, EOFError):
            # If anything besides an integer is entered, the user will receive this message
            print('Invalid Input. Entry must be an integer.\n')
            continue
        # Print the target month for the user
        print('\nYou should visit Fairbanks, AK in', months[month], 'based on your selection.\n')

    
