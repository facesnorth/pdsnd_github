import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("\nWould you like to see data for Chicago, New York City or Washington? ").lower()
        if city not in ('chicago', 'new york city', 'washington'):
            print("\nPlease, check your spelling.\n")
            continue
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("\nWould you like to filter the data by month? Choose: January, February, March, April, May, June or type all: ").lower()
        if month not in( 'january','february','march', 'april', 'may', 'june', 'all' ):
            print("\nPlease, check your spelling.\n")
            continue
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("\nWould you like to filter data by the day? Choose: Saturday, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday or type all: ").lower()
        if day not in ('saturday','sunday','monday','tuesday','wednesday','thursday','friday','all'):
            print("\nPlease, check your spelling.\n")
            continue
        else:
            break

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    # get datetime format from 'Start Time'
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # make month and dayofweek columns from 'Start Time'
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['start_hour'] = df['Start Time'].dt.hour

    # if month is specified
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df["month"] == month]

    # if day of week is specified
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...')
    start_time = time.time()

    # display the most common month
    most_common_month = df["month"].mode()[0]
    print("\nThe most common month to rent: ", most_common_month)

    # display the most common day of week
    most_common_day= df["day_of_week"].mode()[0]
    print("\nThe most common day to rent: ", most_common_day)

    # display the most common start hour
    df["hour"] = df["Start Time"].dt.hour
    most_common_start_hour = df["hour"].mode()[0]
    print("\nThe most common starting hour: ", most_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating the most popular stations and trip...')
    start_time = time.time()

    #  Most common start station
    start_sta = df["Start Station"].mode()[0]
    print("\nThe most commonly used start station: ", start_sta)

    # Most common end station
    end_sta = df["End Station"].mode()[0]
    print("\nThe most commonly used end station: ", end_sta)

    # Most frequent start / end station combo
    common_sta = (df["Start Station"] + " to " + df["End Station"]).mode()[0]
    print("\nThe most frequent combination of start and end stations: ", common_sta)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('.'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...')
    start_time = time.time()

    # display total travel time
    tot_trav_time = df["Trip Duration"].sum()
    print("\nThe total travel time in days: ", tot_trav_time/(60*60*24))
    print("\nThe total travel time in hours: ", int(sum((df['Trip Duration'])/60)/60))

    # display mean travel time
    mean_trav_time = df["Trip Duration"].mean()
    print("\nThe mean travel time in mins: ", mean_trav_time/60)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...')
    start_time = time.time()

    # Display counts of user types
    user_types = df.groupby(['User Type'])['User Type'].count()
    print("\nTypes of users: ", user_types) 
    
    # Display counts of gender
    try:
        gender = df.groupby(['Gender'])['Gender'].count()
        print("\nNumber of each gender: ", gender)
    except KeyError:
        print("\nGender data unavailable for Washington.")

    # Display earliest, most recent, and most common year of birth
    try:
        earliest = int(df['Birth Year'].min())
        print("\nThe earliest birth year: ", earliest)
    except KeyError:
        print("\nBirth year data unavailable for Washington.")

    try:
        most_recent = int(df['Birth Year'].max())
        print("\nThe most recent birth year:", most_recent)
    except KeyError:
        print("\nBirth year data unavailable for Washington.")

    try:
        most_common = int(df['Birth Year'].mode()[0])
        print("\nThe most common birth year: ", most_common)
    except KeyError:
        print("\nBirth year data unavailable for Washington.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Raw data upon request."""
    x = 0
    while True:
        i = input("Would you like to see the raw data?  Yes or no: ")
        if i.lower() == 'yes':
            print(df[x:x+5])
            x = x+5
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no: \n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()