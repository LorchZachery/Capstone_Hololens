import serial              
from time import sleep, perf_counter
import sys
import os 
import requests
import shutil
import json
import sys

gpgga_info = "$GNGGA,"
GPGGA_buffer = 0
NMEA_buff = 0
dfcsURL = "http://ied-dfcs.com/capstone/scripts/"
def convert_to_degrees(raw_value):
    decimal_value = raw_value/100.00
    degrees = int(decimal_value)
    mm_mmmm = (decimal_value - int(decimal_value))/0.6
    position = degrees + mm_mmmm
    position = "%.6f" %(position)
    return position

def updateXY(curr_lat, curr_lon):
    #print("UPDATING")
    url = dfcsURL + 'x_y.php'
    data = {'lat' : curr_lat , 'lon' : curr_lon }
    try:
        r = requests.post(url, data = data)
    except:
        r = requests.post(url, data = data)

    b = r.content.decode()
    #print(b)

def main():
    end = perf_counter() + 60
    
    while perf_counter() < end:
        ser = serial.Serial ("/dev/ttyS0")
        i = 0
        while i < 10:
            try:
                received_data = (str)(ser.readline()) #read NMEA string received
                
                GPGGA_data_available = received_data.find(gpgga_info)   #check for NMEA GPGGA string                
                if (GPGGA_data_available>=0):
                    GPGGA_buffer = received_data.split("$GNGGA,",1)[1]  #store data coming after "$GPGGA," string
                    
                    NMEA_buff = (GPGGA_buffer.split(','))
                    nmea_time = []
                    nmea_latitude = []
                    nmea_longitude = []
                    nmea_time = NMEA_buff[0]                    #extract time from GPGGA string
                    nmea_latitude = NMEA_buff[1]                #extract latitude from GPGGA string
                    lat_sign = NMEA_buff[2]
                    nmea_longitude = NMEA_buff[3]               #extract longitude from GPGGA string
                    lon_sign = NMEA_buff[4]
                    
                    #print("NMEA Time: ", nmea_time)
                    lat = (float)(nmea_latitude)
                    lat = convert_to_degrees(lat)
                    if lat_sign == 'S':
                        lat = lat * -1
                    longi = (float)(nmea_longitude)
                    longi = convert_to_degrees(longi)
                    if lon_sign == 'W':
                        longi = float(longi) * -1
                        
                    updateXY(lat,longi)
                    #print ("NMEA Latitude:", lat,"NMEA Longitude:", longi)
                    i +=1
                
            except KeyboardInterrupt:
                try:
                    sys.exit(0)
                except SystemExit:
                    os._exit(0)
            except:
                #print("disconnect trying to reconnect..")
                i += 1
    return
    
if __name__ == '__main__':
    while True:
        #print("running for a minute")
        main()
        #print("sleeping for a minute")
        total = 1
        while total < 3:
            sleep(15)
            #print(str(total*15) + " seconds")
            total +=1 
    