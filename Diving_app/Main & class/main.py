import PySimpleGUI as psg
import webbrowser
from class_ import Weather, MySql, Month, Graph, Time_


#set the theme for the screen/window
psg.theme('SandyBeach')


#define layout
layout=[[psg.Text('Choose the continent you want to go to dive',size=(40, 1), font='Lucida',justification='left')],
        [psg.Combo(['America','Asia','Africa', 'Europe','Oceania'],default_value='America',key='continent')],
        [psg.Text('Choose the month you want to dive ',size=(30, 1), font='Lucida',justification='left')],
        [psg.Combo(['January','February','March', 'April','May','June','July','August','September','October','November','December'],default_value="January",key='month')],
        [psg.Text('Choose your user name',size=(30, 1), font='Lucida',justification='left')],
        [psg.InputText("", key='user_name')],
        [psg.Button('SEARCH', font=('Times New Roman',12)),psg.Button('CANCEL', font=('Times New Roman',12))]]

#Define Window
win =psg.Window('Choose the period and place for diving',layout)

while True:  # Event Loop
    event, values = win.read()
    if event in (psg.WIN_CLOSED, 'CANCEL'):         # If Cancel or close window, the program will end
        break

    elif values['user_name']=="":
        psg.popup('The user name input it`s empty. Please write a user name',title='No user name')      # Force the user to write a name
        
    else:
        check=MySql.check_user_table(values['user_name'])     # Check if the user name table exists

        if check==True:
            MySql.reset_table(values['user_name'])

        else:
            pass

        month=Month.change_to_number(values['month'])                           # Store the values in variables
        user_table=MySql.create_new_table(values['user_name'])                  #Create a table for the user in the database
        read_data=MySql.read_data_out_list(values['continent'])                 #Read values from diving schema
        year=Time_.current_connection_time()               

        for i in range(0,len(read_data[0]),1):                                  # Read data and store it in the new user table
            name_=read_data[0][i]
            country=read_data[1][i]
            web=read_data[2][i]
            points=read_data[3][i]
            latitude=read_data[4][i]
            longitude=read_data[5][i]
            if name_=="Silfra, Thingvellir": 
                if month=="February":                                                                             #Calculation if the month selected it`s February`                                                            
                    non_wave_cal=Weather.cloud_wind_rain_calculus_February(month,str(latitude),str(longitude),int(year)-1)          
                    final_calc=Weather.equation_points(points,0,0,0,non_wave_cal[0],non_wave_cal[1],non_wave_cal[2])
                else:                                                                                             # calculation if the selected month it`s not February`
                    non_wave_cal=Weather.cloud_wind_rain_calculus(month,str(latitude),str(longitude),int(year)-1)
                    final_calc=Weather.equation_points(points,0,0,0,non_wave_cal[0],non_wave_cal[1],non_wave_cal[2])
            else:
                if month=="February":                                                                               #Calculation for marine conditions if the month chosen it`s February`
                    wave_calc=Weather.wind_wave_calculus(month,str(latitude),str(longitude))
                    non_wave_cal=Weather.cloud_wind_rain_calculus_February(str(month),str(latitude),str(longitude),int(year)-1)
                    final_calc=Weather.equation_points(points,wave_calc[0],wave_calc[1],wave_calc[2],non_wave_cal[0],non_wave_cal[1],non_wave_cal[2])
                else:                                                                                               # Calculation for marine conditions if the month it`s not February`
                    wave_calc=Weather.wind_wave_calculus(month,str(latitude),str(longitude))
                    non_wave_cal=Weather.cloud_wind_rain_calculus(month,str(latitude),str(longitude),int(year)-1)
                    final_calc=Weather.equation_points(points,wave_calc[0],wave_calc[1],wave_calc[2],non_wave_cal[0],non_wave_cal[1],non_wave_cal[2])

            MySql.insert_data(values["user_name"],name_,country,web,final_calc,latitude,longitude)          # Insert all this data in the new table for the user
        
        table_order=MySql.order_table(values['user_name'])                                  # Order the table based on the points just calculated

        
        num=0
        psg.Print(f"Rank of places for diving in {values['continent']} in {values['month']}:\n")
        for i in table_order:
            num+=1
            psg.Print(f"{num}.-{i[0]}, {i[1]}, Total points= {i[3]}")                         # Print the list in oredr of points basde on the user selection
           
        while True:
            num=psg.popup_get_text("Choose a number from the list please: ",title="Rank list")                                #Choose the destination you are interested in
            try:
                int(num)

                if event in (psg.WIN_CLOSED, 'CANCEL'):
                    break

                elif int(num)<=0 or int(num)>len(table_order):
                    psg.popup("Error, number not in the list. Choose a number in the list",title="Error, number not in list")   # If the number it`s not in the list popup warning`

                else:
                    webbrowser.open(table_order[int(num)-1][2])                                                     # Show the webpage for the selected option for diving
                    psg.popup("The web page for diving it`s displayed in google chrome",title='Web page',)
                    psg.popup('These are the total points after calculation:' ,table_order[int(num)-1][3],title="Total points")     #Show the points after calculation for this option
                    webbrowser.open(Weather.weather(table_order[int(num)-1][4],table_order[int(num)-1][5]))                                 #Current Weather conditions in the area
                    psg.popup("The web page for weather conditions in the area it`s displayed in google chrome",title='Weather conditions',)
                    graph_data=Weather.data_in_graph(month,table_order[int(num)-1][4],table_order[int(num)-1][5],int(year)-1)
                    Graph.create_multiple_plot(graph_data[0],graph_data[1],graph_data[2],graph_data[3],values['month'],int(year)-1)             #Weather record for rain, cloudcover and windspeed for the selected month
                    psg.popup("Now will be displayed all the weather condions apart in different graphs",title='Weather conditions',)
                    Graph.create_plot(graph_data[0],graph_data[1],f"Amount of Rain in mm in {values['month']} {int(year)-1}","Time(hours)","Rain in mm" )            #Print each each atribute in different graphs for better visualization
                    Graph.create_plot(graph_data[0],graph_data[2],f"Percentage of Cloudcover in {values['month']} {int(year)-1}","Time(hours)","Cloudcover %" )
                    Graph.create_plot(graph_data[0],graph_data[3],f"Windspeed during {values['month']} {int(year)-1}","Time(hours)","Windspeed km/h" )
                
                
            except ValueError:
                psg.popup("Please choose a integer in the list shown please",title="Value error")        #Be sure that the user inputs a integer in the list
            

win.close()