#
# Description: Project 1 - Utilizing retrieval of information from CTA2 L Daily Ridership database.
# Course: CS 341, Fall 2024, UIC
# Author: Saden Elkhatib, UIN: 668648511
#

import sqlite3
import matplotlib.pyplot as plt


#
# print_stats
#
# Given a connection to the CTA database, executes various
# SQL queries to retrieve and output basic stats.
#
def print_stats(dbConn):
    dbCursor = dbConn.cursor()

    print("General Statistics:")

    dbCursor.execute("Select count(*) from Stations;")
    row = dbCursor.fetchone();
    print("  # of stations:", f"{row[0]:,}")

    dbCursor.execute("Select count(*) from Stops;")
    row = dbCursor.fetchone();
    print("  # of stops:", f"{row[0]:,}")

    dbCursor.execute("Select count(*) from Ridership;")
    row = dbCursor.fetchone();
    print("  # of ride entries:", f"{row[0]:,}")

    dbCursor.execute("select distinct date(Ride_Date) from Ridership order by Ride_Date asc limit 1;")
    row = dbCursor.fetchone();
    print("  date range:", row[0], end="")

    dbCursor.execute("select distinct date(Ride_Date) from Ridership order by Ride_Date desc limit 1;")
    row = dbCursor.fetchone();
    print(" -", row[0])

    dbCursor.execute("Select sum(Num_Riders) from Ridership;")
    row = dbCursor.fetchone();
    print("  Total ridership:", f"{row[0]:,}")


#
# command1
#
# Finds all the station names that match the user input. The user will be asked to input a
# partial station name. SQL wildcards _ and % are allowed. Output station names in
# ascending order. If no stations are found, prints a message indicating that no stations
# were found.
#
def command1(dbConn):
    dbCursor = dbConn.cursor()
    inp = input("\nEnter partial station name (wildcards _ and %): ")
    dbCursor.execute(
        "Select Station_ID, Station_Name from Stations where Station_Name like (?) order by Station_Name asc;", [inp])
    result = dbCursor.fetchall()
    if (len(result) == 0):
        print("**No stations found...")
    else:
        for row in result:
            Station_ID, Station_Name = row
            print(f"{Station_ID} : {Station_Name}")


#
# command2
#
# Given a station name, finds the percentage of riders on weekdays, on Saturdays, and on
# Sundays/holidays for that station. The station name from the user must be an exact
# match. Each percentage is calculated out of the total number of riders for that
# station. Displays both the totals and the percentages.
#
def command2(dbConn):
    dbCursor = dbConn.cursor()
    inp = input("\nEnter the name of the station you would like to analyze: ")
    dbCursor.execute(
        "Select sum(Num_Riders) from Ridership join Stations on Ridership.Station_ID = Stations.Station_ID where Station_Name = (?);",
        [inp])
    totalRidership = dbCursor.fetchone()
    if (totalRidership[0] == None):
        print("**No data found...")
    else:
        # Total ridership during the week
        dbCursor.execute(
            "Select sum(Num_Riders) from Ridership join Stations on Ridership.Station_ID = Stations.Station_ID where Station_Name = (?) and Type_of_Day = 'W';",
            [inp])
        weekdayRidership = dbCursor.fetchone()
        # Total ridership during Saturdays
        dbCursor.execute(
            "Select sum(Num_Riders) from Ridership join Stations on Ridership.Station_ID = Stations.Station_ID where Station_Name = (?) and Type_of_Day = 'A';",
            [inp])  # A denotes Saturdays
        saturdayRidership = dbCursor.fetchone()
        # Total ridership for Sundays/Holidays
        dbCursor.execute(
            "Select sum(Num_Riders) from Ridership join Stations on Ridership.Station_ID = Stations.Station_ID where Station_Name = (?) and Type_of_Day = 'U';",
            [inp])  # U denotes Sundays/Holidays
        sundayHolidayRidership = dbCursor.fetchone()
        print(f"Percentage of ridership for the {inp} station: ")
        print("  Weekday ridership:", f"{weekdayRidership[0]:,}",
              f"({weekdayRidership[0] / totalRidership[0] * 100:.2f}%)")
        print("  Saturday ridership:", f"{saturdayRidership[0]:,}",
              f"({saturdayRidership[0] / totalRidership[0] * 100:.2f}%)")
        print("  Sunday/holiday ridership:", f"{sundayHolidayRidership[0]:,}",
              f"({sundayHolidayRidership[0] / totalRidership[0] * 100:.2f}%)")
        print("  Total ridership:", f"{totalRidership[0]:,}")


#
# command3
#
# Outputs the total ridership on weekdays for each station, with station names rather than
# the station IDs. Also shows the percentages, taken out of the total ridership on weekdays
# for all the stations. Orders the results in descending order by ridership.
#

def command3(dbConn):
    dbCursor = dbConn.cursor()
    dbCursor.execute(
        "Select sum(Num_Riders) from Ridership where Type_of_Day = 'W';")  # total Ridership stats for weekdays
    totalWeekdayRidership = dbCursor.fetchone()
    dbCursor.execute(
        "Select Station_Name, sum(Num_Riders) from Ridership join Stations on Ridership.Station_ID = Stations.Station_ID where Type_of_Day = 'W' group by Station_Name order by sum(Num_Riders) desc;")  # total Ridership stats for the indputted station name
    resultsEachStation = dbCursor.fetchall()
    print("Ridership on Weekdays for Each Station")
    for row in resultsEachStation:
        Station_Name, weekdayRidership = row
        print(f"{Station_Name} : {weekdayRidership:,} ({weekdayRidership / totalWeekdayRidership[0] * 100:.2f}%)")


#
# command4
#
# Given a line color and direction, outputs all the stops for that line color in that direction.
# Orders by stop name in ascending order. The line color and direction are treated
# as case-insensitive
#
def command4(dbConn):
    validColor = False
    dbCursor = dbConn.cursor()
    inputColor = input("\nEnter a line color (e.g. Red or Yellow): ")
    dbCursor.execute("Select Color from Lines;")
    results = dbCursor.fetchall()
    for row in results:
        if (row[0].lower() == inputColor.lower()):
            validColor = True
    if (not validColor):
        print("**No such line...")
    else:
        inputDir = input("Enter a direction (N/S/W/E): ")
        inputDir.lower()
        if (inputDir == 'north'):
            inputDir = 'n'
        elif (inputDir == 'south'):
            inputDir = 's'
        elif (inputDir == 'west'):
            inputDir = 'w'
        elif (inputDir == 'east'):
            inputDir = 'e'

        dbCursor.execute(
            "Select Stop_Name, Direction, ADA from Stops join StopDetails on Stops.Stop_ID = StopDetails.Stop_ID join Lines on StopDetails.Line_ID = Lines.Line_ID where Color = (?) COLLATE NOCASE and Direction = (?) COLLATE NOCASE order by Stop_Name asc;",
            [inputColor, inputDir])
        resultStops = dbCursor.fetchall()
        if (len(resultStops) == 0):
            print("**That line does not run in the direction chosen...")
        else:
            for row in resultStops:
                stopName, direction, ada = row
                if (ada == 1):
                    accessible = "handicap accessible"
                else:
                    accessible = "not handicap accessible"
                print(f"{stopName} : direction = {direction} ({accessible})")


#
# command5
#
# Outputs the number of stops for each line color, separated by direction. Shows the results
# in ascending order by color name, and then in ascending order by direction. Also shows
# the percentage for each one, which is taken out of the total number of stops.
#
def command5(dbConn):
    dbCursor = dbConn.cursor()
    dbCursor.execute(
        "Select Color, Direction, Count(*) from Stops join StopDetails on Stops.Stop_ID = StopDetails.Stop_ID join Lines on StopDetails.Line_ID = Lines.Line_ID group by Direction, Color order by Color asc, Direction asc;")
    results = dbCursor.fetchall()
    dbCursor.execute("Select Count(*) from Stops;")
    totalNumStops = dbCursor.fetchone()
    print("Number of Stops For Each Color By Direction")
    for row in results:
        color, dir, count = row
        print(f"{color} going {dir} : {count} ({count / totalNumStops[0] * 100:.2f}%)")


#
# command6
#
# Given a station name, outputs the total ridership for each year for that station, in
# ascending order by year. Allows the user to use wildcards _ and % for partial names.
# Shows an error message if the station name does not exist or if multiple station names
# match.
# User is given the option to plot the data. If the user responds with any input other than
# “y”, data will not plot.
#
def command6(dbConn):
    dbCursor = dbConn.cursor()
    inp = input("\nEnter a station name (wildcards _ and %): ")
    dbCursor.execute("Select Station_Name from Stations where Station_Name like (?);", [inp])
    stationResults = dbCursor.fetchall()
    if (len(stationResults) == 0):
        print("**No station found...")
    elif (len(stationResults) > 1):
        print("**Multiple stations found...")
    else:
        stationName = stationResults[0][0]
        dbCursor.execute(
            "Select distinct strftime('%Y', Ride_Date) as Year, sum(Num_Riders) from Ridership join Stations on Ridership.Station_ID = Stations.Station_ID where Station_Name = (?) group by Year;",
            [stationName])
        yearlyRidership = dbCursor.fetchall()
        print(f"Yearly Ridership at {stationName}")
        for row in yearlyRidership:
            year, numRiders = row
            print(f"{year} : {numRiders:,}")
        askPlot = input("\nPlot? (y/n) ")
        if (askPlot.lower() == 'y'):
            x = []
            y = []
            year = 1
            for row in yearlyRidership:
                year, numRiders = row
                x.append(year)
                y.append(numRiders)
            plt.xlabel("Year")
            plt.ylabel("Number of Riders")
            plt.title(f"Yearly Ridership at {stationName} Station")
            plt.ioff()
            plt.plot(x, y)
            plt.show()


#
# command7
#
# Given a station name and year, outputs the total ridership for each month in that year.
# The user can enter SQL wildcards (_ and %) for the station name.
# Once the station name and year have been entered, displays the monthly totals. Then,
# user is granted the option to see a plot of the results. If the user responds with “y” the
# program will plot the data accordingly.
#
def command7(dbConn):
    dbCursor = dbConn.cursor()
    inpStation = input("\nEnter a station name (wildcards _ and %): ")
    dbCursor.execute("Select Station_Name from Stations where Station_Name like (?);", [inpStation])
    stationResults = dbCursor.fetchall()
    if (len(stationResults) == 0):
        print("**No station found...")
    elif (len(stationResults) > 1):
        print("**Multiple stations found...")
    else:
        stationName = stationResults[0][0]
        inpYear = input("Enter a year: ")
        dbCursor.execute(
            "Select strftime('%m', Ride_Date), sum(Num_Riders) from Ridership join Stations on Ridership.Station_ID = Stations.Station_ID where Station_Name = (?) and strftime('%Y', Ride_Date) = (?) group by strftime('%m', Ride_Date);",
            [stationName, inpYear])
        monthlyResults = dbCursor.fetchall()
        print(f"Monthly Ridership at {stationName} for {inpYear}")
        for row in monthlyResults:
            month, numRiders = row
            print(f"{month}/{inpYear} : {numRiders:,}")
        askPlot = input("\nPlot? (y/n) ")
        if (askPlot.lower() == 'y'):
            x = []
            y = []
            month = 1
            for row in monthlyResults:
                month, numRiders = row
                x.append(month)
                y.append(numRiders)
            plt.xlabel("Month")
            plt.ylabel("Number of Riders")
            plt.title(f"Monthly Ridership at {stationName} Station {inpYear}")
            plt.ioff()
            plt.plot(x, y)
            plt.show()


#
# command8
#
# Given two station names and year, outputs the total ridership for each day in that year.
# The user can enter SQL wildcards (_ and %) for each station name. Note: only outputs the first 5 days and last 5
# days of data for each station. After collecting data, If the user responds with “y", data will be plotted.
# If the user responds with any other input, data will NOT be plotted. Also, if there are multiple stations
# or no stations found, the user will be notified and will need to reselect their query.
#
def command8(dbConn):
    dbCursor = dbConn.cursor()
    inpYear = input("\nYear to compare against? ")
    inpStation1 = input("\nEnter station 1 (wildcards _ and %): ")
    dbCursor.execute("Select Station_ID, Station_Name from Stations where Station_Name like (?);", [inpStation1])
    stationResults = dbCursor.fetchall()
    if (len(stationResults) == 0):
        print("**No station found...")
    elif (len(stationResults) > 1):
        print("**Multiple stations found...")
    else:
        stationID1 = stationResults[0][0]
        stationName1 = stationResults[0][1]
        inpStation2 = input("\nEnter station 2 (wildcards _ and %): ")
        dbCursor.execute("Select Station_ID, Station_Name from Stations where Station_Name like (?)", [inpStation2])
        stationResults = dbCursor.fetchall()
        if (len(stationResults) == 0):
            print("**No station found...")
        elif (len(stationResults) > 1):
            print("**Multiple stations found...")
        else:
            stationID2 = stationResults[0][0]
            stationName2 = stationResults[0][1]

            print(f"Station 1: {stationID1} {stationName1}")
            dbCursor.execute(
                "Select date(Ride_Date), Num_Riders from Ridership where Station_ID = (?) and strftime('%Y', Ride_Date) = (?) order by Ride_Date asc;",
                [stationID1, inpYear])
            resultStation1 = dbCursor.fetchall()
            for row in resultStation1[:5]:
                rideDate, numRiders = row
                print(f"{rideDate} {numRiders}")
            for row in resultStation1[-5:]:
                rideDate, numRiders = row
                print(f"{rideDate} {numRiders}")

            print(f"Station 2: {stationID2} {stationName2}")
            dbCursor.execute(
                "Select date(Ride_Date), Num_Riders from Ridership where Station_ID = (?) and strftime('%Y', Ride_Date) = (?) order by Ride_Date asc;",
                [stationID2, inpYear])
            resultStation2 = dbCursor.fetchall()
            for row in resultStation2[:5]:
                rideDate, numRiders = row
                print(f"{rideDate} {numRiders}")
            for row in resultStation2[-5:]:
                rideDate, numRiders = row
                print(f"{rideDate} {numRiders}")
            askPlot = input("\nPlot? (y/n) ")
            if (askPlot.lower() == 'y'):
                # station 1
                x1 = []
                y1 = []

                # station 2
                x2 = []
                y2 = []
                day = 1
                for row in resultStation1:
                    x1.append(day)
                    y1.append(row[1])
                    day = day + 1
                day = 1
                for row in resultStation2:
                    x2.append(day)
                    y2.append(row[1])
                    day = day + 1
                plt.xlabel("Day")
                plt.ylabel("Number of Riders")
                plt.title(f"Ridership Each Day of {inpYear}")
                plt.plot(x1, y1, label=f'{stationName1}')
                plt.plot(x2, y2, label=f'{stationName2}')
                plt.ioff()
                plt.legend()
                plt.show()


#
# command9
#
# Given a set of latitude and longitude from the user, finds all stations within a mile square
# radius. Gives the user the option to plot these stations on a map of Chicago from OpenStreetMaps.
# Program checks that the latitude and longitude are within the bounds of Chicago. The latitude
# must be between 40 and 43 degrees, and the longitude must be between -87 and -88 degrees.
# If user inputs invalid coordinates or there are no stations found, they will be notified accordingly.
#
def command9(dbConn):
    dbCursor = dbConn.cursor()
    inpLat = float(input("\nEnter a latitude: "))
    if (inpLat >= 40 and inpLat <= 43):
        inpLong = float(input("Enter a longitude: "))
        if (inpLong <= -87 and inpLong >= -88):
            # square mile radius boundaries
            # LATITUDE
            latLower = round(inpLat - (1 / 69), 3)  # 1 mile/69
            latUpper = round(inpLat + (1 / 69), 3)
            # LONGITUDE
            longLower = round(inpLong - (1 / 51), 3)  # 1 mile/51
            longUpper = round(inpLong + (1 / 51), 3)
            # Selects stations that have a longitude and latitude within one square mile's distance from user inputted coordinates (uses BETWEEN)
            dbCursor.execute(
                "Select distinct Station_Name, Latitude, Longitude from Stops join Stations on Stops.Station_ID = Stations.Station_ID where Latitude between (?) and (?) and Longitude between (?) and (?) order by Station_Name asc;",
                [latLower, latUpper, longLower, longUpper])
            results = dbCursor.fetchall()
            if (len(results) > 0):
                print("\nList of Stations Within a Mile")
                for row in results:
                    stationName, latitude, longitude = row
                    print(f"{stationName} : ({latitude}, {longitude})")
                askPlot = input("\nPlot? (y/n) ")
                if (askPlot.lower() == 'y'):
                    x = []
                    y = []
                    for row in results:
                        stationName, latitude, longitude = row
                        x.append(longitude)
                        y.append(latitude)
                    image = plt.imread("chicago.png")
                    xydims = [-87.9277, -87.5569, 41.7012, 42.0868]
                    plt.imshow(image, extent=xydims)
                    plt.title("Stations Near You")
                    plt.plot(x, y, marker='o', linestyle='', color='blue', label='stations')
                    for row in results:
                        stationName, latitude, longitude = row
                        plt.annotate(stationName, (longitude, latitude))
                    # Definite limits for coordinate boundaries
                    plt.xlim([-87.9277, -87.5569])
                    plt.ylim([41.7012, 42.0868])
                    plt.ioff()
                    plt.show()
            else:
                # If no station is found within 1 mile of user inputted coordinates
                print("**No stations found...")
        else:
            print("**Longitude entered is out of bounds...")
    else:
        print("**Latitude entered is out of bounds...")


##################################################################
#
# main
#
print('** Welcome to CTA L analysis app **')
print()

dbConn = sqlite3.connect('CTA2_L_daily_ridership.db')

print_stats(dbConn)

cont = True
while (cont):
    inp = input("\nPlease enter a command (1-9, x to exit): ")
    if (inp == "1"):
        command1(dbConn)
    elif (inp == "2"):
        command2(dbConn)
    elif (inp == "3"):
        command3(dbConn)
    elif (inp == "4"):
        command4(dbConn)
    elif (inp == "5"):
        command5(dbConn)
    elif (inp == "6"):
        command6(dbConn)
    elif (inp == "7"):
        command7(dbConn)
    elif (inp == "8"):
        command8(dbConn)
    elif (inp == "9"):
        command9(dbConn)
    elif (inp == "x"):
        cont = False
    else:
        print("**Error, unknown command, try again...")

#
# done
#