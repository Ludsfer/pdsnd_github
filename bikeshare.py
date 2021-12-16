import time
import pandas as pd
import numpy as np


pd.set_option('display.max_columns', 10)  # coerce all the available columns so that the output prints only ten columns 
pd.set_option('display.width', 1000)


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_filters_load():
    """
    Asks user to specify a city, month, and day to analyze and load data into dataframe ready for analysis.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    user_input = input("\nEnter 'chicago' or 'new york city' or 'washington' to load the available data for the analysis: ").lower()
    
    while True:
        if  user_input in CITY_DATA.keys():
            city = pd.read_csv(CITY_DATA[user_input])  # load data corresponding to the city selected 
            city.dropna(axis = 0, inplace = True)  # remove the nan in the city's data
            
            city['Start Time'] = pd.to_datetime(city['Start Time'])  # convert attribute to a datatime like
            city['month'] = city['Start Time'].dt.month_name()  # name months in the selected city
            city['day_of_week'] = city['Start Time'].dt.day_name()  # name days in the selected city
            
            month = input('Select month to display (january, february, ... , june), \'all\' to view all the months: ').lower().title()
            months = list(city['month'].unique())   # make a list of available month having data in the selected city
            
            if (month != 'All') and (month in months):
                 
                day = input('Select a day of week (monday, tuesday, ... , sunday), \'all\' to view all week days: ').lower().title()
                days = list(city['day_of_week'].unique()) # make a list of available days having data in the selected city
                
                if (day != 'All') and (day in days):
                    city = city[city['month'] == month] # intermediate result trimming by the selected month
                    return city[city['day_of_week'] == day] # trim the intermediate result by the day
                
                else:
                    print(f'\nThe selected city does not have data for day \'{day}\' in \'{month}\'.')
                    print('Loaded is the data of all the week_days contained in the month of \'{}\'.'.format(month))
                    return city[city['month'] == month]      
            else:
                print('Loaded is the data of all the months contained in the city')
                return city
        
        else:
            print("\nOops, '{}' cannot be found in the dictionary of cities.".format(user_input))
            print("Please enter 'chicago' or 'new york city' or 'washington' to proceed with the statistics: ")
            user_input = input().lower()




def display(filtered_data, size = 5):
    """  
    Display function asks the user whether he would like to view chunck of data, if yes then display five lines of the data otherwise, proceed with the next step
    
    Args:
    size - default argument specifying the number of lines to be printed
    filtered_data - data over which iteration is done
    """
    i = 0
    user_input = input(f"\nWould you like to see chunck of lines of raw data? \n('yes' or 'y') to view {size} lines the data ('no' or 'n') to proceed with the statistics: ").lower()
    
    while user_input == 'yes' or user_input == 'y':
        print(filtered_data[i:(i + size)])
        user_input = input("Would you like to see another {} more lines of raw data?: ".format(size)).lower()
        
        if i >= len(filtered_data):  # check for whether the size to be printed will be out of range of the length of the data if so just print the remaining row of the data
            j = i - len(filtered_data)
            i -= size
            size -= j
            print(f"It remmains only {size} rows of data\n.")
        else:
            i += size
            
    print('-'*40)       
 



def time_stats(filtered_data):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    common_month = filtered_data['month'].mode()[0]
    print(f'Most frequent travel month: {common_month}')

    # Display the most common day of week
    common_day = filtered_data['day_of_week'].mode()[0]
    print(f'Most travel took place on: {common_day}')

    # Display the most common start hour
    filtered_data['hour'] = filtered_data['Start Time'].dt.hour
    common_hour = filtered_data['hour'].mode()[0]
    print('Frequently traveled hour is {}\n'.format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)




def station_stats(filtered_data):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used Start Station
    print("the most commonly used Start Station:")
    StartStation_maxCount = max(filtered_data['Start Station'].value_counts())
    count = filtered_data['Start Station'].value_counts()
    station = count[count == StartStation_maxCount]
    print(station)
    print('-'*10)
    
    # Display most commonly used End Station
    print("the most commonly used End Station:") 
    EndStation_maxCount = max(filtered_data['End Station'].value_counts())
    count = filtered_data['End Station'].value_counts()
    station = count[count == EndStation_maxCount]
    print(station)
    print('-'*10)
   

    # Display most frequent combination of start station and end station trip
    
    start_end = {} # create an empty dictionary
    combination_StartEnd = zip(filtered_data['Start Station'], filtered_data['End Station'])
    for key in combination_StartEnd:
        if key not in start_end:
            start_end[key] = 1
        else:
            start_end[key] += 1

    max_value = max(start_end.values())  # look for the highest occurence of the combination of start-end station key
    keys_list = list(start_end.keys())  # make a list of the keys
    values_list = list(start_end.values())  # make a list of the values
    position = values_list.index(max_value)  # check for thr index position of the maximum occurence
    
    # print key with value = max_value
    freq_key = keys_list[position]
    
    print(f"The most frequent combination of Start Station and End Station is: {freq_key} with number of occurence: {max_value}.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
    
    
def user_stats(filtered_data):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Statistics of User Type: ")
    UserType_count = filtered_data['User Type'].value_counts()
    print(UserType_count)
    print('-'*10)
    
    # Display counts of gender
    if 'Gender' in filtered_data.columns:
        print("Gender Statistics: ")
        Gender_stats = filtered_data['Gender'].value_counts()
        print(Gender_stats)
    print('-'*10)
    
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in filtered_data.columns:
        Earliest_Birthyear = min(filtered_data['Birth Year'])
        Recent_Birthyear = max(filtered_data['Birth Year'])
        Common_Birthyear = filtered_data['Birth Year'].mode()[0]
        print(f"The earliest year of birth: {Earliest_Birthyear} ")
        print(f"The most recent year of birth: {Recent_Birthyear} ")
        print(f"The most common year of birth: {Common_Birthyear} ")
    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)




def trip_duration_stats(filtered_data):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    Total_travelTime = sum(filtered_data['Trip Duration'])
    print(f"Total of travel time: {Total_travelTime}. ")

    # Display mean travel time
    Mean_travelTime = filtered_data['Trip Duration'].mean()
    print(f"Mean travel time: {Mean_travelTime}. ")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    

    
    
def length_station(filtered_data):
    """Displays statistics on the longuest, shortest name of each station."""
    
    print('\nCalculating station name length...\n')
    start_time = time.time()
    
    # Display the longest name in the Start station
    max_len = 0
    for name in list(filtered_data['Start Station'].unique()):
        if (len(name) > max_len):
            max_len = len(name)
            station_name = name
    print(f"The longuest Start Station name: \'{station_name}\', with length: {max_len}")
    
    # Display the Shortest name in the Start station
    min_len = 100  #  arbitrary value from which to search for the shortest length
    for name in list(filtered_data['Start Station'].unique()):
        if (len(name) < min_len):
            min_len = len(name)
            station_name = name
    print(f"The shortest Start Station name: \'{station_name}\', with length: {min_len}")
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
    
    
def compose_code(filtered_data):
    """set up a code composed of the first three letters of the User Type, month and day_of_week\n and check for the number of possibe combination in the data loaded"""
    
    print('Number of possibe combination of the made up code...\n')
    start_time = time.time()
    
    codes = []
    count = 0
    code_base = zip(filtered_data['User Type'], filtered_data['month'], filtered_data['day_of_week'])
    for userT, month, day in code_base:
        code = userT[:3] + month[:3] + day[:3]
        if code not in codes:
            codes.append(code)
            count += 1
    print(f"From the data enquiries, we found in total {count} possible combination of User types, travelling a given month on a given day.")
    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    


def start_with(filtered_data):
    """Statistics of the number of station in the loaded data that starts with a letter or digit. """
    
    print('\nNumber of possibe combination of the made up code...\n')
    start_time = time.time()
    
    letter = 0
    num = 0
    other = 0
    for station in list(filtered_data['Start Station']):
        if station[0].isalpha():
            letter += 1
        elif station[0].isnumeric():
            num += 1
        else:
            other += 1
    print(f"The loaded data contains in total {letter} Start Stations with rows name starting with a letter,\n {num} Start Station with rows starting with a numeric value and {other} rows starting with other special characters")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
    
    
def GenderTrip_Uniformity(filtered_data):
    """Check for both whether the number of male that went to a trip in the filtered data surpasses the females and 
    whether the most common trip duration is equally distributed around the mean Trip Duration within 5% confidence bound
    """
    
    print('\nStatistics on the Gender\'s data and Trip Duration\'s uniformity...\n')
    start_time = time.time()
    
    male_data = filtered_data[filtered_data['Gender'] == 'Male']
    male = male_data['Trip Duration']
    mean_MaleTripDuration = male.mean()
    female_data = filtered_data[filtered_data['Gender'] == 'Female']
    female = female_data['Trip Duration']
    mean_FemaleTripDuration = female.mean()
    percentage_male = float(len(male_data))/float(len(filtered_data)) * 100
    percentage_female = float(len(female_data))/float(len(filtered_data)) * 100
    t0 = min(filtered_data['Start Time'])
    t1 = max(filtered_data['Start Time'])
    if percentage_female > percentage_male:
        print(f"The filtered data contains only {percentage_male:.2f}% of males while females represent {percentage_female:.2f}% for the selected period which spans from {t0} and {t1}.")
        print(f"with the males average Trip Duration of {mean_MaleTripDuration} compare to {mean_FemaleTripDuration} for female")
    else:
        print(f"In the filtered data, males represents {percentage_male:.2f}% and females {percentage_female:.2f}% for the selected period which spans from {t0} and {t1}.")
        print(f"with the males average Trip Duration of {mean_MaleTripDuration:.3f} compare to {mean_FemaleTripDuration:.3f} for female")
    
    
    mode = filtered_data['Trip Duration'].mode()[0]
    mean_TripDuration = filtered_data['Trip Duration'].mean()
    if (mode > mean_TripDuration*0.975) and (mode < mean_TripDuration*1.025):
        print("The most common trip duration is within 5% confidence bound of the average duration of the total trip")
    else:
        print("The most common trip duration is out of the 5% confidence bound of the average duration of the total trip")
       
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
    
    
def main():
    while True:
         
        filtered_data = get_filters_load() # filtered_data - Pandas DataFrame containing city data filtered by month and day ready for analysis 
        display(filtered_data)  # calling the display function and display chunk of data upon request
        time_stats(filtered_data)
        station_stats(filtered_data)
        trip_duration_stats(filtered_data)
        user_stats(filtered_data)
        
        
        if 'Gender' in filtered_data.columns:
            user_input = input("Would you like to check whether the Trip Duration of the \'Gender\' from the filtered data is uniformly distributed? : ").lower()
            if user_input == 'yes' or user_input == 'y':
                GenderTrip_Uniformity(filtered_data)
        
        user_input = input("Would you like to check the lengthiest or shortest Start Station name in the loaded city? : ").lower()
        if user_input == 'yes' or user_input == 'y':
            length_station(filtered_data)
        
        user_input = input("Do you want statistics of the number of Start Station in the loaded city commencing with letters, numbers or other special characters? : ").lower()
        if user_input == 'yes' or user_input == 'y':
            start_with(filtered_data)
        
        user_input = input("Are you interested in checking for the possible combination of \'User Type\', \'month\' and \'day\' in the loaded city's data?: ").lower()
        if user_input == 'yes' or user_input == 'y':
            compose_code(filtered_data)
        

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
