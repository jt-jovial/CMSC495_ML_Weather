"""
Created by: Keri Lloyd
Date Created: April 15, 2022
Edited by: Amanda Wheland
Date Edited: April 16, 2022
Class: CMSC 495 7381
Purpose: This program is part of a larger Machine Learning group project - currently used as proof of concept.
"""

import random
import numpy as np
import pandas as pd
from sklearn import tree
from sklearn.neighbors import KNeighborsClassifier

# Read in data
df = pd.read_csv("Fairbanks.csv", header=[0])

# Replace T (trace) values with 0.01 to indicate a trace amount
df['Precipitation'] = df['Precipitation'].replace('T', 0.01)
df['New Snow'] = df['New Snow'].replace('T', 0.01)
df['Snow Depth'] = df['Snow Depth'].replace('T', 0.01)

# Cast Precipitation, New Snow, and Snow Depth to float64 (they were initially objects)
df['Precipitation'] = df['Precipitation'].apply(np.float64)
df['New Snow'] = df['New Snow'].apply(np.float64)
df['Snow Depth'] = df['Snow Depth'].apply(np.float64)

# Initialize factor to begin while loop 
factor = 0
# Months dictionary
months = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August',
          9: 'September', 10: 'October', 11: 'November', 12: 'December'}


def temperature():
    """ Temperature method for Menu option 1 """
    while True:
        try:
            # Request temperature from user
            temp = int(input("Please enter your preferred temperature as an integer "
                             "(between -20 and 85 degrees Fahrenheit): "))
            if -20 <= temp <= 85:
                break
            else:
                # If user enters any number besides -20-85, this error message will display
                print('Invalid input. Entry must be an integer between -20-85.')
                continue
        except (ValueError, EOFError):
            # If anything besides an integer is entered, the user will receive this message
            print('Invalid Input. Entry must be an integer.')
            continue

    # Assign features (X) and target (y)
    X = df[['Average']]
    y = df['Season']

    # K-Nearest Neighbors model, 72% accuracy
    knn = KNeighborsClassifier(n_neighbors=12)
    # Fit the data to the model, then predict using given temperature
    knn.fit(X.values, y)
    season = knn.predict([[temp]])
    # Seasons: 0 == Winter, 1 == Spring, 2 == Summer, 3 == Fall
    if season == 0:
        # Isolate winter to narrow down the target month
        df_season = df.loc[df['Season'] == 0]
        m_range = (210, 720)  # Winter daylight hour range in minutes
        h_range = '3.5 - 12.0'  # Range in hours for input request
    elif season == 1:
        # Isolate spring to narrow down the target month
        df_season = df.loc[df['Season'] == 1]
        m_range = (720, 1140)  # Spring daylight hour range in minutes
        h_range = '12.0 - 19.0'  # Range in hours for input request
    elif season == 2:
        # Isolate summer to narrow down the target month
        df_season = df.loc[df['Season'] == 2]
        m_range = (840, 1320)  # Summer daylight hour range in minutes
        h_range = '14.0 - 22.0'  # Range in hours for input request
    elif season == 3:
        # Isolate fall to narrow down the target month
        df_season = df.loc[df['Season'] == 3]
        m_range = (420, 840)  # Fall daylight hour range in minutes
        h_range = '7.0 - 14.0'  # Range in hours for input request

    while True:
        try:
            # Request daylight hour preference from user
            daylight = int(input('Do you have a preference for the number of daylight hours? (1 for yes, 2 for no): '))
            if daylight == 1:
                hours = float(input('How many daylight hours would you prefer (choose between ' + h_range + ' ): '))
                minutes = hours * 60
                # determine if the user entered hours within the correct range
                if minutes in range(m_range[0], m_range[1] + 1):
                    break
                else:
                    # If user enters any number that does not fit in the specified range,
                    # this error message will display
                    print('Invalid input. Entry must be between ' + h_range + '.')
                    continue
            elif daylight == 2:
                minutes = random.randint(m_range[0], m_range[1]+1)
                break
            else:
                # Verify and sanitize user input
                print("Invalid input. Please try again.")
        except (ValueError, EOFError):
            # If anything besides a number is entered, the user will receive this message
            print('Invalid Input. Entry must be a number.')
            continue

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


def snowfall():
    """ Snowfall method for Menu option 2 """
    while True:
        try:
            # Request snowfall amount from user in inches
            snow = int(input("How much accumulated inches of snow would you like to see? (0-24): "))
            if 0 <= snow <= 24:
                break
            else:
                # If user enters any number besides 0-24, this error message will display
                print('Invalid input. Entry must be between 0-24.')
                continue
        except (ValueError, EOFError):
            # If anything besides an integer is entered, the user will receive this message
            print('Invalid Input. Entry must be an integer.')
            continue

    while True:
        try:
            # Request daylight hour preference from user
            daylight = int(input('Do you have a preference for the number of daylight hours? (1 for yes, 2 for no): '))
            if daylight == 1:
                hours = float(input('How many daylight hours would you prefer (choose between 3.5-18.5): '))
                if 3.5 <= hours <= 18.5:
                    minutes = hours * 60
                    break
                else:
                    # If user enters any number besides 3.5-18.5, this error message will display
                    print('Invalid input. Entry must be between 3.5-18.5')
                    continue
            elif daylight == 2:
                minutes = random.randint(210, 1110)
                break
            else:
                # If user enters any integer besides 1 or 2, this error message will display
                print("Invalid input. Please try again.")
        except (ValueError, EOFError):
            # If anything besides a number is entered, the user will receive this message
            print('Invalid Input. Entry must be a number.')
            continue

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


def daylight_hours():
    """ Daylight hour's method for Menu option 3 """
    while True:
        try:
            # Request the number of daylight hours preferred
            daylight = float(input('How many daylight hours would you prefer? (3.5-22): '))
            if 3.5 <= daylight <= 22:
                # Change hours to minutes (the daylight data is in minutes)
                minutes = daylight * 60
            else:
                # If user enters any number besides 3.5-22, this error message will display
                print('Invalid input. Entry must be between 3.5-22.')
                continue
            # Once minutes are calculated, a season can be determined
            # Winter: 210-419, Fall/Winter: 420-719, Fall/Spring: 720-840, Spring/Summer: 841-1140, Summer: 1140-1320
            # Winter: min < 420, Summer: 1140 < min <= 1320
            # Fall/Winter: 420 <= min < 720, Fall/Spring: 720 <= min <= 840, Spring/Summer: 840 < min <= 1140
            if minutes < 420:
                season = 0  # Winter automatically chosen (less than 7 hours)
                break
            elif 420 <= minutes < 720:  # This range falls between 2 seasons (7-12 hours, Fall/WInter)
                while True:
                    # Request if user has a seasonal preference
                    choice = int(
                        input('Would you prefer to visit in the Fall (1), or Winter (2), or No preference (3)?: '))
                    if choice == 1:
                        season = 3  # Fall
                        break
                    elif choice == 2:
                        season = 0  # Winter
                        break
                    elif choice == 3:
                        season = np.random.choice([3, 0])  # Will randomly choose between 3 and 0
                        break
                    else:
                        # If the user enters an integer besides 1-3, this error message will display
                        print('Invalid input Please try again.')
                        continue
                break
            elif 720 <= minutes <= 840:  # This range falls between 2 seasons (12-14 hours, Spring/Fall)
                while True:
                    # Request if user has a seasonal preference
                    choice = int(
                        input('Would you prefer to visit in the Spring (1), or Fall (2), or No preference (3)?: '))
                    if choice == 1:
                        season = 1  # Spring
                        break
                    elif choice == 2:
                        season = 3  # Fall
                        break
                    elif choice == 3:
                        season = np.random.choice([1, 3])  # Will randomly choose between 1 and 3
                        break
                    else:
                        # If the user enters an integer besides 1-3, this error message will display
                        print('Invalid input. Please try again.')
                        continue
                break
            elif 840 < minutes <= 1140:  # This range falls between 2 seasons (14-19 hours, Spring/Summer)
                while True:
                    # Request if user has a seasonal preference
                    choice = int(
                        input('Would you prefer to visit in the Spring (1), or Summer (2), or No preference (3)?: '))
                    if choice == 1:
                        season = 1  # Spring
                        break
                    elif choice == 2:
                        season = 2  # Summer
                        break
                    elif choice == 3:
                        season = np.random.choice([1, 2])  # Will randomly choose between 1 and 2
                        break
                    else:
                        # If the user enters an integer besides 1-3, this error message will display
                        print('Invalid input. Please try again.')
                        continue
                break
            elif 1140 < minutes <= 1320:
                season = 2  # Summer automatically chosen (19-22 hours)
                break
            else:
                # This is unlikely as the input is validated before the multiplication takes place.
                print('Something went wrong.')
                continue
        except (ValueError, EOFError):
            # If anything besides a number is entered, the user will receive this message
            print('Invalid Input. Entry must be a number.')
            continue

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


def northern_lights():
    """ Northern Lights method for Menu option 4 """
    print('The best time to see the Northern Lights in Fairbanks, AK is between August and April!')
    # Isolate dataframe to months between August and April
    df_nl = df.loc[df['Month'].isin([8, 9, 10, 11, 12, 1, 2, 3, 4])]

    while True:
        try:
            # Request if user has a daylight preference 
            daylight = int(input('Do you have a preference for the number of daylight hours? (1 for yes, 2 for no): '))
            if daylight == 1:
                # Request daylight hour preference from user
                hours = float(input('How many daylight hours would you prefer (choose between 3.5-16.5): '))
                if 3.5 <= hours <= 16.5:
                    minutes = hours * 60
                    break
                else:
                    print('Invalid input. Entry must be between 3.5-16.5')
                    continue
            elif daylight == 2:
                minutes = random.randint(210, 1000)
                break
            else:
                # Verify and sanitize user input
                print("Invalid input. Please try again.")
        except (ValueError, EOFError):
            # If anything besides a number is entered, the user will receive this message
            print('Invalid Input. Entry must be an number.')
            continue

    while True:
        try:
            # Request if user has a preference on amount of accumulated snow
            snowfall_pref = int(input("Do you have a preference for the amount of accumulated snow? "
                                      "(1 for yes, 2 for no): "))
            if snowfall_pref == 1:
                # Request snowfall amount from user in inches
                snow = int(input("How much accumulated inches of snow would you like to see? (0-24): "))
                if 0 <= snow <= 24:
                    break
                else:
                    print('Invalid input. Entry must be between 0-24.')
                    continue
            elif snowfall_pref == 2:
                snow = random.randint(0, 24)
                break
            else:
                print('Invalid input. Please try again')
        except (ValueError, EOFError):
            # If anything besides an integer is entered, the user will receive this message
            print('Invalid Input. Entry must be an integer.')
            continue

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


# How program begins
while factor != 5:
    ''' While loop for Main Menu '''
    # Print statements are used just for proof of concept while experimenting. 
    # Code will be merged with front end webpage development and user will enter input through webpage
    print('What is the most important factor to you when visiting Fairbanks, AK?')
    print('1. Temperature\n2. Snowfall\n3. Number of Daylight hours\n4. See the Northern Lights\n5. Exit')
    # Try/except block to ensure input is only an integer between 1-5
    try:
        factor = int(input('Enter 1-4 or 5 to exit: '))
        # Temperature is chosen as priority 
        if factor == 1:
            # Run the temperature model method
            month = temperature()
        elif factor == 2:
            # Run the snowfall model method
            month = snowfall()
        elif factor == 3:
            # Run the daylight_hours model method
            month = daylight_hours()
        elif factor == 4:
            # Run the northern_Lights model method
            month = northern_lights()
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
    print("\nYou should visit Fairbanks, AK in", months[month], "based on your selection.\n")
    
