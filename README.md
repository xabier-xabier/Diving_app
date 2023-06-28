# Diving_app
Top 99 diving places Rank.

The target of this app is to select the best places to dive per continent based on the weather conditions and rank points.
The weather conditions will consider historic record of windspeed, cloudcover and rain and marine forecast of Wave height, Wind Wave height and Swell Wave height.

To be consistent with the rank points that I researched on the internet i consider a small percentage of this conditions impacting into the equation to calculate the final points based on weather conditions.

The equation for point calculation is the following one:

equation=rank_points-0.05*(wave_height+wind_wave_height+swell_wave)-0.04*rain-0.03*cloudcover-0.08*windspeed


There is already created in MySql a table with data related to the best 99 diving places in the world. 
I created a Schema called diving in MySql.
You can directly upload it using the diving_data file provided.
In this table the following data is provided:

1)Id number based on the rank points.
2)The name of each place
3)Continent 
4)Country
5)Web page with info related to diving in that place
6)Rank points
7)latitude of the place (for locating the place for weather condition search)
8)Longitude of the place (for locating the place for weather condition search)
9)Info to know if the place it`s in the ocean or lake.


This app will request at the begining info about the month when the user would like to go diving, the continent of preference and a user name.
If the user name doesn`t exist will create a new table with the user name in MySql to store data for further post processing.

When selecting the Month and continent the app will access the data in diving_data table.
The app will store the name of the place, country, webpage, latitude, longitude and will proceed to the point calculation based on the month chosen.
Once the new table it`s created it willbe reordered based on the points calculated to show it to the user.

Once the list is displayed the user will be able to choose any option from the list.
Once the user chooses a place the following data will be displayed:

1)webpage of that diving place 
2)Number of points after calculation
3)Weather forecast in the area
4)Weather conditions record of the chosen month but belonging to last year (Rain,Cloudcover and Windspeed)
5)Rain in mm for the chosen month (last year)
6)Cloudcover % for the chosen month (last year)
7)Windspeed (km/h) for the chosen month (last year)

The user can choose another option from the list or just end the program by closing the window or selecting "cancel".
