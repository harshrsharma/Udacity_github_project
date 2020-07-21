import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():

    print('Hello! Let\'s explore some US bikeshare data!')
    #This function filters data based on user inputs.
    # TO DO: get user input for city (chicago, new york city, washington).
    filters = ['month', 'day', 'none']
    months = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6}
    days = {'sunday': 0, 'monday': 1, 'tuesday': 2, 'wednesday': 3, 'thursday': 4, 'friday': 5, 'saturday': 6}
    day=-1
    month=-1
    city=''

    while (True):
        city_selected = input('\nWould you like to see data for Chicago, New York City, or Washington?\n')
        if (city_selected.lower() in (CITY_DATA.keys())):
            city = CITY_DATA[city_selected.lower()]
            break

        else:
            print('Sorry, input unrecognized, could you please re-enter.')
            continue

    while(True):
        data_filter = input(
            '\nWould you like to filter data by month, day, or not at all? type none for no time filter.\n')

        if(data_filter.lower() in filters):
    # TO DO: get user input for month (all, january, february, ... , june)
            while (data_filter.lower() == 'month'):
                month_selected = input('\nWhich month - January, Frbruary, March, April, May, or June?\n')

                if(month_selected.lower() in months.keys()):
                    month=months[month_selected.lower()]
                    break

                else:
                    print('Sorry, input unrecognized, could you please re-enter.')
                    continue
    # TO DO: get user input for day of week (monday, tuesday, ... sunday)
            while(data_filter.lower() == 'day'):
                day_selected = input('\nWhich day of the week - Monday, Tuesday, ... , Sunday ?\n')
                if (day_selected.lower() in days.keys()):
                    day = days[day_selected.lower()]
                    break
                else:
                    print('Sorry, input unrecognized, could you please re-enter.')
                    continue

        else:
            print('Sorry, input unrecognized, could you please re-enter.')
            continue
        break
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
    try:
        df = pd.read_csv(city)
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df['End Time'] = pd.to_datetime(df['End Time'])
        df['month_number'] = df['Start Time'].dt.month
        df['day_of_week'] = df['Start Time'].dt.dayofweek
        df['day_of_month'] = df['Start Time'].dt.day
        df['hour'] = df['Start Time'].dt.hour

        if(month != -1):
            df = df[df['month_number'] == month]

        if(day != -1):
            df = df[df['day_of_week'] == day]

    except Exception as e:
        print(e)

    return df


def display_data(df):
    """Ask and display data to user"""
    count = 0
    while(True):
        count += 5
        user_input = input('\nDo you want to see sample data before seeing stats? Respond Yes or No\n')
        if (user_input.lower() in ('yes', 'no')):
            if (user_input.lower() == 'yes'):
                print(df.iloc[:count + 1, :])
                while (True):
                    user_input_more_rows = input('\nDo you want to see more rows? Respond Yes or No\n')
                    if (user_input_more_rows.lower() in ('yes', 'no')):
                        if (user_input_more_rows.lower() == 'yes'):
                            count += 5
                            print(df.iloc[: count + 1, :])
                        else:
                            break
                    else:
                        print('Sorry, input unrecognized, could you please re-enter.')
                        continue
            else:
                break
            if(user_input_more_rows.lower()=='no'):
                break
        else:
            print('Sorry, input unrecognized, could you please re-enter.')
            continue


def time_stats(df,month,day):
    """Displays statistics on the most frequent times of travel."""
    months = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June'}
    days = {0:'Sunday', 1:'Monday', 2:'Tuesday', 3:'Wednesday', 4:'Thursday', 5:'Friday', 6:'Saturday'}

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    if(month == -1): #no need to provide most common month if user chose data by month in input
        common_month = df.groupby(['month_number']).size().sort_values(
            ascending=False).reset_index(name='counts')
        print('Most common month : ', months[common_month['month_number'][0]])


    # TO DO: display the most common day of week
    if (day == -1):  # no need to provide most common day if user chose data by day in input
        common_day = days[df.mode()['day_of_week'][0]]
        print('Most common day : ', common_day)
    # TO DO: display the most common start hour

    common_hour = df.groupby(['hour']).size().sort_values(
        ascending=False).reset_index(name='counts')
    print('Most common hour : ', common_hour['hour'][0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df.mode()['Start Station'][0]
    print('Most common start station : ', common_start_station)

    # TO DO: display most commonly used end station
    common_end_station = df.mode()['End Station'][0]
    print('Most common end station : ', common_end_station)

    # TO DO: display most frequent combination of start station and end station trip

    common_station_pair = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False).reset_index(
        name="counts")

    common_start_pair = common_station_pair['Start Station'][0]
    common_end_pair = common_station_pair['End Station'][0]
    print("3. The start station for most common pair is '{}' and the end station is '{}'".format(
        common_start_pair, common_end_pair))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    seconds=total_travel_time%60
    total_minutes=total_travel_time//60
    minutes=total_minutes%60
    hours=total_minutes//60
    print("Total travel time is {} hours {} minutes {} seconds:".format(hours,minutes,seconds) )

    # TO DO: display mean travel time
    total_mean_time = df['Trip Duration'].mean()
    print("Mean travel time in seconds is :", total_mean_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types

    user_type_count = df["User Type"].value_counts()
    print(user_type_count)

    # TO DO: Display counts of gender
    if "Gender" in df.columns:
        gender_count = df["Gender"].value_counts()
        print(gender_count)

    # TO DO: Display earliest, most recent, and most common year of birth
    if "Birth Year" in df.columns:
        earliest_birth_year = df['Birth Year'].min()
        most_recent_birth_year = df['Birth Year'].max()
        most_common_birth_year = df['Birth Year'].mode()[0]
        print("\nEarliest birth year: '{}'. \nMost recent birth year: '{}'. \nMost common birth year: '{}'.\n"
                .format(earliest_birth_year,most_recent_birth_year, most_common_birth_year))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    city, month, day = get_filters()
    df = load_data(city, month, day)
    display_data(df)
    time_stats(df,month,day)
    station_stats(df)
    trip_duration_stats(df)
    user_stats(df)

    restart = input('\nWould you like to restart? Enter yes or no.\n')
    if restart.lower() == 'yes':
        main()
    else:
        exit()

if __name__=='__main__':
    main()