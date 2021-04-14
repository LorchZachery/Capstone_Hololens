# PI Server
## Pi general infromation
Connecting into the PI server is a nessary action.  
username: pi  
password: 6yhn7ujm^YHN&UJM  
when connected to the ravpower the pi's ip address will be 10.10.10.40  
ravpower:  
name: Capstone 
password: 1111111  
Gateway: 10.10.10.254  (if you want to see what is going on on server go to gateway)  
  
## PI connection
I have set up the ravpower to first point to the pi so you can go to https://ied-dfcs.com or http://ied-dfcs.com to access the pi from any machine connected to
 the rav power. 
 To change these things or if you get a new router access static ip is in /etc/dhcpd.conf and the DNS name is set in /etc/hosts  
  
## PI Database
The reason we have the pi is to allow for a local database  
to access the database on the pi:  
```mysql -u root -p```  
the password is 6yhn7ujm^YHN&UJM  
the name of the database is capstone it has two tables ```bombs``` and ```current_location```  
bombs has the tables ```ID,lat,lon,x,y,color```  ```ID``` is the primary key of ecah entry they do not need to be in order, it is just an identifier, ```lat``` and ```lon``` are the gps locations, ```x``` and 
```y``` are the x and y distances from the ```current_location``` gps. this is what the file x_y.php is able to do. (math intensive).  
