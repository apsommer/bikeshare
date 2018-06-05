#
# Andrew Sommer
# June 5, 2018
# Udacity Data Analyst Nanodegree
# Term 1 - Project 2 - Explore US Bikeshare Data
#

from datetime import datetime as dt
import subprocess
import time
import pandas as pd
import numpy as np

# master dictionary with provided csv files
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# user inputs are made directly to the terminal
def get_filters():

    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nThis program analyzes US bikeshare data provided by Motivate at https://www.motivateco.com/. Three cities are considered over the first six months of 2017. The user can filter the resulting statistics by city, month, and day.')

    # get user inputs for city, month, and day ... convert to lowercase strings
    print('\nEnter the city name (Chicago, New York City, Washington):')
    city = str(input("\n\t")).lower()

    print('\nEnter the month name (all, January, February, ... June):')
    month = str(input("\n\t")).lower()

    print('\nEnter day of week (all, Monday, Tuesday, ... Sunday):')
    day = str(input("\n\t")).lower()

    # valid inputs
    city_list = ['chicago', 'new york city', 'washington']
    month_list = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    day_list = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    # check for valid user input (city)
    while city not in city_list:

        print('\n\t*Please enter a valid city name (Chicago, New York City, Washington): ')
        city = str(input("\n\t\t")).lower()

    # check for valid user input (month)
    while month not in month_list:

        print('\n\t*Please enter a valid month name (all, January, February, ... June):')
        month = str(input("\n\t\t")).lower()

    # check for valid user input (day)
    while day not in day_list:

        print('\n\t*Please enter a valid day of week (all, Monday, Tuesday, ... Sunday):')
        day = str(input("\n\t\t")).lower()

    terminal_width = int(subprocess.check_output(['tput', 'cols'])) # returns the character width of the current terminal, this makes a nice dividing line for presentation in the terminal

    print('_'*terminal_width)

    return city, month, day

def load_data(city, month, day):

    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """

    # create DataFrame from csv file
    df = pd.read_csv(CITY_DATA[city])

    # offer user chance to see the raw data
    print('\nWould you like to see the raw data? Enter yes or no.')
    display_raw = input('\n\t')
    if display_raw.lower() == 'yes':

        print()
        print(df)
        print()

    # convert the Start Time and End Time columns to datetime objects
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month from Start Time to create new columns
    months_list = ['January', 'February', 'March', 'April', 'May', 'June']
    df['Month'] = df['Start Time'].dt.month - 1 # dt.month returns an integer month as January = 1, February = 2, ...
    df['Month'] = df['Month'].apply(lambda x: months_list[x]) # convert the month integer to string

    # new column for day of week
    df['Day'] = df['Start Time'].dt.weekday_name # returns the week day name as string

    # new column for hour
    hours_list = ["12 AM", "1 AM", "2 AM", "3 AM", "4 AM", "5 AM", "6 AM", "7 AM", "8 AM", "9 AM", "10 AM", "11 AM",
                "12 PM", "1 PM", "2 PM", "3 PM", "4 PM", "5 PM", "6 PM", "7 PM", "8 PM", "9 PM", "10 PM", "11 PM"]
    df['Hour'] = pd.to_datetime(df['Start Time']).dt.hour
    df['Hour'] = df['Hour'].apply(lambda x: hours_list[x]) # convert the hour integer to string with AM or PM appended

    # make new column for start station and end station combinations
    df['Start and End'] = '(Start) ' + df['Start Station'] + ' (End) ' + df['End Station'] # returns a deltaTime object

    # filter by month if applicable
    if month != 'all':

        # filter by month to create the new dataframe
        df = df[df['Month'] == month.title()]

    # filter by day of week if applicable
    if day != 'all':

        # filter by day of week to create the new dataframe
        df = df[df['Day'] == day.title()]

    return df

def time_stats(df):

    """Displays statistics on the most frequent times of travel."""

    terminal_width = int(subprocess.check_output(['tput', 'cols'])) # returns the character width of the current terminal, this makes a nice dividing line for presentation in the terminal

    print('_'*terminal_width)
    print('\nThe most common travel times.\n')

    # display the most common month
    print('\tMonth:', df['Month'].mode()[0])

    # display the most common day of week
    print('\tDay:', df['Day'].mode()[0])

    # display the most common start hour
    print('\tHour:', df['Hour'].mode()[0])

def station_stats(df):

    """Displays statistics on the most popular stations and trip."""

    print('\nThe most common stations.\n')

    # display most commonly used start station
    print('\tStart:', df['Start Station'].mode()[0])

    # display most commonly used end station
    print('\tEnd:', df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    combination = df['Start and End'].value_counts().index[0] # returns sorted Series (decending)
    occurances = df['Start and End'].value_counts().iloc[0] # returns sorted Series (decending)
    print('\tTrip: {} occurances of {}'.format(occurances, combination))

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nTrip durations.')

    # display total travel time
    df['Travel Time'] = df['End Time'] - df['Start Time'] # subtracting two datetimes returns a datetime.timedelta object
    total_time = df['Travel Time'].sum() # datetime.timedelta object, displays as 'X days XX:XX:XX.XXXXXX'
    sec = int(total_time.total_seconds()) # convert to total number of seconds, convert to integer
    days = sec // 86400
    hours = (sec % 86400) // 3600
    min = ((sec % 86400) % 3600) // 60
    sec = ((sec % 86400) % 3600) % 60
    print('\n\tTotal: {} days {} hours {} min {} sec'.format(days, hours, min, sec))

    # display mean travel time
    df['Travel Time'] = df['End Time'] - df['Start Time'] # subtracting two datetimes returns a datetime.timedelta object
    mean_time = df['Travel Time'].mean() # datetime.timedelta object, displays as 'X days XX:XX:XX.XXXXXX'
    sec = int(mean_time.total_seconds()) # convert to total number of seconds, convert to integer
    days = sec // 86400
    hours = (sec % 86400) // 3600
    min = ((sec % 86400) % 3600) // 60
    sec = ((sec % 86400) % 3600) % 60
    print('\tMean: {} days {} hours {} min {} sec'.format(days, hours, min, sec))

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nUser classifications.')

    # Display counts of user types
    print('\n\tType:\n')
    df_User_Type = df['User Type'].value_counts()

    # convert df to string for terminal display (removes footer Name: User Type, dtype: int64). Add a tab character to the newline for presentation.
    print('\t' + df_User_Type.to_string().replace('\n', '\n\t'))

    # Gender may not be a part of the data set (washington.csv)
    try:

        df_Gender_Type = df['Gender'].value_counts()
        # Display counts of gender
        print('\n\tGender:\n')

        # convert df to string for terminal display (removes footer Name: User Type, dtype: int64). Add a tab character to the newline for presentation.
        print('\t' + df_Gender_Type.to_string().replace('\n', '\n\t'))

    # do nothing on the KeyError for Gender
    except Exception:
        pass # continue

    # Birth Year may not be a part of the data set (washington.csv)
    try:

        # Display earliest, most recent, and most common year of birth
        current_year = dt.now().year
        age = current_year - df['Birth Year'].mode()[0]
        print('\n\tMost common age:', int(age))

        age = current_year - df['Birth Year'].min()
        print('\tOldest: ' + str(int(age)))

        age = current_year - df['Birth Year'].max()
        print('\tYoungest: ' + str(int(age)))

        age = current_year - df['Birth Year'].mean()
        print('\tAverage: ' + str(int(age)))

    # do nothing on the KeyError for Birth Year
    except Exception:
        pass # continue

def main():

    # while True is bad practice
    while True:

        # solicit input from the user
        city, month, day = get_filters()

        # clock execution time
        global start_time
        start_time = time.time()

        # build dataframe from provided csv files
        df = load_data(city, month, day)

        # generate and print statistics
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # clock execution time
        end_time = time.time() - start_time
        total_time = round(end_time, 2) # rounds float to specified decimal places
        print("\n... total runtime %s seconds." % total_time)

        # offer chance to restart program from beginning
        print('\n\nWould you like to restart? Enter yes or no.')
        restart = input('\n\t')
        if restart.lower() != 'yes':
            print()
            break

# conditional is True only if this file is run directly, not if this file is imported into another script ... effectively means the functions (outside this conditional) are imported into another script, but the code specific to this file is never executed from that script
if __name__ == "__main__":

    main()

#TODO: Fix the trip durations to give a better output than a default timestamp.
