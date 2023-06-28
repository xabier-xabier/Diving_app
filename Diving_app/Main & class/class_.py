import requests
import sqlalchemy
from pprint import pprint
import matplotlib.pyplot as plt
from datetime import date


class Weather:

    # Use this app to show a map with the weather conditions in the area for diving
    def weather(lat,lon):
        base_url=f"https://openweathermap.org/weathermap?basemap=map&cities=true&layer=radar&lat={lat}&lon={lon}&zoom=50"

        return base_url
    

    # This function will be used to calculate the sea conditions for wave height, wind wave and swell wave
    def wind_wave_calculus(month,latitude,longitude):
        base_url=f"https://marine-api.open-meteo.com/v1/marine?latitude={latitude}&longitude={longitude}&hourly=wave_height,wind_wave_height,swell_wave_height&length_unit=metric"
        response = requests.get(base_url)
        resp_lan=response.json()

        sum_wave_height=0

        for i in resp_lan["hourly"]["wave_height"]:
            if i==None:
                sum_wave_height+=0
            else:
                sum_wave_height+=float(i)
        ave_wave_height=(sum_wave_height)/len(resp_lan["hourly"]["wave_height"]) # Average value of the wave_height of a month
        #---------------------------------------------------------------------------------------------------------------------------------

        sum_wind_wave=0

        for j in resp_lan["hourly"]["wind_wave_height"]:
            if j==None:
                sum_wind_wave+=0
            else:
                sum_wind_wave+=float(j)
        ave_wind_wave=sum_wind_wave/len(resp_lan["hourly"]["wind_wave_height"])  # Average value of the wind_wave_height of a month
        #----------------------------------------------------------------------------------------------------------------------------------

        sum_swell_wave=0

        for z in resp_lan["hourly"]["swell_wave_height"]:
            if z==None:
                sum_swell_wave+=0
            else:
                sum_swell_wave+=float(z)
        ave_swell_wave=sum_swell_wave/len(resp_lan["hourly"]["swell_wave_height"])    # Average value of swell_wave_height

        return ave_wave_height,ave_wind_wave,ave_swell_wave
    
    
    def cloud_wind_rain_calculus(month,latitude,longitude,year):
        base_url=f"https://archive-api.open-meteo.com/v1/archive?latitude={latitude}&longitude={longitude}&start_date={year}-{month}-01&end_date={year}-{month}-30&hourly=rain,cloudcover,windspeed_10m"
        response = requests.get(base_url)
        resp_lan=response.json()

        sum_rain=0

        for i in resp_lan["hourly"]["rain"]:
            sum_rain+=float(i)
        ave_rain=sum_rain/len(resp_lan["hourly"]["rain"])       # Average amount of rain in that month
        #-------------------------------------------------------------------------------------------------------------------------------

        sum_cloud=0
        for j in resp_lan["hourly"]["cloudcover"]:
            sum_cloud+=float(j)
        ave_cloud=sum_cloud/len(resp_lan["hourly"]["cloudcover"])  # Average value of cloudcover
        #---------------------------------------------------------------------------------------------------------------------------------

        sum_windspeed=0
        for z in resp_lan["hourly"]["windspeed_10m"]:
            sum_windspeed+=float(z)
        ave_wind=sum_windspeed/len(resp_lan["hourly"]["windspeed_10m"])   # Average of windspeed

        return ave_rain,ave_cloud,ave_wind
    

    def cloud_wind_rain_calculus_February(month,latitude,longitude,year):
        base_url=f"https://archive-api.open-meteo.com/v1/archive?latitude={latitude}&longitude={longitude}&start_date={year}-{month}-01&end_date={year}-{month}-28&hourly=rain,cloudcover,windspeed_10m"
        response = requests.get(base_url)
        resp_lan=response.json()

        sum_rain=0

        for i in resp_lan["hourly"]["rain"]:
            sum_rain+=float(i)
        ave_rain=sum_rain/len(resp_lan["hourly"]["rain"])       # Average amount of rain in that month
        #-------------------------------------------------------------------------------------------------------------------------------

        sum_cloud=0
        for j in resp_lan["hourly"]["cloudcover"]:
            sum_cloud+=float(j)
        ave_cloud=sum_cloud/len(resp_lan["hourly"]["cloudcover"])  # Average value of cloudcover
        #---------------------------------------------------------------------------------------------------------------------------------

        sum_windspeed=0
        for z in resp_lan["hourly"]["windspeed_10m"]:
            sum_windspeed+=float(z)
        ave_wind=sum_windspeed/len(resp_lan["hourly"]["windspeed_10m"])   # Average of windspeed

        return ave_rain,ave_cloud,ave_wind
    
    def equation_points(rank_points,wave_height,wind_wave_height,swell_wave,rain,cloudcover,windspeed):         #Calculation of all the weather conditions to rank it`s place. Higher points higher in the rank`
        equation=rank_points-0.05*(wave_height+wind_wave_height+swell_wave)-0.04*rain-0.03*cloudcover-0.08*windspeed

        return equation
    
    def data_in_graph(month,latitude,longitude,year):            #Use this function to extract data for ploting the graphs

        if month=="02":
            base_url=f"https://archive-api.open-meteo.com/v1/archive?latitude={latitude}&longitude={longitude}&start_date={year}-{month}-01&end_date={year}-{month}-28&hourly=rain,cloudcover,windspeed_10m"

        else:
            base_url=f"https://archive-api.open-meteo.com/v1/archive?latitude={latitude}&longitude={longitude}&start_date={year}-{month}-01&end_date={year}-{month}-30&hourly=rain,cloudcover,windspeed_10m"
            
        response = requests.get(base_url)
        resp_lan=response.json()

        time=resp_lan["hourly"]["time"]
        rain=resp_lan["hourly"]["rain"]
        cloud=resp_lan["hourly"]["cloudcover"]
        wind=resp_lan["hourly"]["windspeed_10m"]

        return time,rain,cloud,wind


class MySql:

    # When the user selects the continent to go for diving this function will go to the database 
    # to check the items that match this requirement

    def read_data_out_list(continent):
        engine = sqlalchemy.create_engine('mysql+pymysql://root:_________@127.0.0.1/diving')      #Conect to the database
        connection = engine.connect()                                                                   #Take the data from diving schema
        metadata = sqlalchemy.MetaData()

        diving = sqlalchemy.Table('diving_data', metadata, autoload_with=engine)                    #Based on the continent and month selction 
        query1=sqlalchemy.select((diving)).order_by(sqlalchemy.desc("rank_points"))                 #we will acces that specific ddata
        result_proxy1=connection.execute(query1)
        result_set1=result_proxy1.fetchall()

        name=[]
        country=[]
        latitude=[]
        longitude=[]
        web=[]
        points=[]

        for i in range(0,99,1):
            if result_set1[i][2]==continent:            #Inspect the data we are looking for and store it in variables
                name.append(result_set1[i][1])
                country.append(result_set1[i][3])
                web.append(result_set1[i][4])
                points.append(result_set1[i][5])
                latitude.append(result_set1[i][6])
                longitude.append(result_set1[i][7])
            else:
                pass
        return name,country,web,points,latitude,longitude,web    # Output all the items needed to calculate the points after weather history record and rank it


    def create_new_table(user_name):
        # When it`s a new user asking for recommendations for diving we will create a new table in the data base
        
        engine = sqlalchemy.create_engine('mysql+pymysql://root:_________@127.0.0.1/diving')
        connection = engine.connect()
        metadata = sqlalchemy.MetaData()

        newTable = sqlalchemy.Table(user_name, metadata,
                       sqlalchemy.Column('name', sqlalchemy.String(255), nullable=False),
                       sqlalchemy.Column('country', sqlalchemy.String(255), nullable=False),
                       sqlalchemy.Column('web', sqlalchemy.String(255), nullable=False),
                       sqlalchemy.Column('Points', sqlalchemy.Float(), default=100.0),
                       sqlalchemy.Column('latitude', sqlalchemy.Float(), default=100.0),
                       sqlalchemy.Column('longitude', sqlalchemy.Float(), default=100.0),
                    )

        metadata.create_all(engine)

    def insert_data(user_name,name,country,web,points,latitude,longitude):
        # We will check the diving_data table to take info and insert it in the new user table for later post processing

        engine = sqlalchemy.create_engine('mysql+pymysql://root:________@127.0.0.1/diving')
        connection = engine.connect()
        metadata = sqlalchemy.MetaData()

        newTable = sqlalchemy.Table(user_name, metadata, autoload_with=engine)

        query = sqlalchemy.insert(newTable).values(name=name, country=country, web=web,Points=points, latitude=latitude, longitude=longitude)
        result_proxy = connection.execute(query)
        result_proxy1=connection.commit()      # need to commit the data to the database


    def order_table(user_name):
        engine = sqlalchemy.create_engine('mysql+pymysql://root:___________@127.0.0.1/diving')
        connection = engine.connect()
        metadata = sqlalchemy.MetaData()

        diving = sqlalchemy.Table(user_name, metadata, autoload_with=engine)
        query1=sqlalchemy.select((diving)).order_by(sqlalchemy.desc("Points"))      #Order the table after point calculation for post-processing
        result_proxy1=connection.execute(query1)
        result_set1=result_proxy1.fetchall()
        return result_set1
    
    def check_user_table(user_name):        #Check if the user already consulted already the database and created a profile
        engine = sqlalchemy.create_engine('mysql+pymysql://root:____________@127.0.0.1/diving')
        insp=sqlalchemy.inspect(engine)
        
        out=insp.has_table(user_name)

        return out
    
    def reset_table(user_name):     #In case the user exists in the database reset it and proceed to new search
        engine = sqlalchemy.create_engine('mysql+pymysql://root:____________@127.0.0.1/diving')
        connection=engine.connect()
        metadata = sqlalchemy.MetaData()

        newTable = sqlalchemy.Table(user_name, metadata, autoload_with=engine)

        query = sqlalchemy.delete(newTable)
        connection.execute(query)
        connection.commit()

class Graph:

    def create_plot(x_data,y_data,title,x_data_title,y_data_title):     #Create graph with a single variable
        plt.plot(x_data,y_data,color="blue",marker="o")
        plt.title(title,fontsize=14)
        plt.xlabel(x_data_title,fontsize=14)
        plt.ylabel(y_data_title,fontsize=14)
        plt.grid(True)
        plt.show()
        
    
    def create_multiple_plot(x_data,y_data,y_data1,y_data2,month,year):  #Create a graph with multiple variables

        plt.figure(figsize=(5,3),dpi=100)
        plt.plot(x_data,y_data,lw=1,color='red',linestyle='-',label='Rain (mm)')
        plt.plot(x_data,y_data1,lw=1,color='green',linestyle='-',label='Cloudcover %')
        plt.plot(x_data,y_data2,lw=1,color='blue',linestyle='-',label='Windspeed (km/h)')
        plt.legend(loc='upper center')
        plt.title(f"Weather condition in {month} {year}",fontsize=10)
        plt.xlabel('Time (hours)')
        plt.ylabel('Weather output')
        plt.xlim(x_data[0],x_data[-1])
        plt.grid()
        plt.show()
        

        
class Month:

    def change_to_number(month):        #Based on the chosen month convert it to number for 
        if month=="January":            #API Weather search based on coordinates and date
            out="01"
        elif month=="February":
            out="02"
        elif month=="March":
            out="03"
        elif month=="April":
            out="04"
        elif month=="May":
            out="05"
        elif month=="June":
            out="06"
        elif month=="July":
            out="07"
        elif month=="August":
            out="08"
        elif month=="September":
            out="09"
        elif month=="October":
            out="10"
        elif month=="November":
            out="11"
        else:
            out="12"
        
        return out
    

class Time_:
    #use this function to extract previous year data to check weather conditions last year
    def current_connection_time():              
        today = date.today()
        year=today.strftime("%Y")

        return year

