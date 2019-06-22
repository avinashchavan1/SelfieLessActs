# SelfieLessActs
  
 ## Technologies/languages used:  
 a) Python  
 b) HTML  
 c) Javascript  
 d) Ajax  
 
   
 ## Introduction
 
SelfieLessActs is a Web Application, that is used to share information about anything that is good for the society that you observe. Examples of such acts could be:  
*  Picking up a piece of garbage and dumping it in a garbage can
* Road getting laid in your area  
* Someone helping a blind man cross the road.  

The orchestrator should be able to:  
* Start and stop container based on the number of HTTP requests received in the last 2 minutes.  
* Should load balance all the incoming HTTP requests equally between all the container.  
* Should monitor the health of all the containers through a health check API.  

## Health check and Crash server  

For health check, we have written a health check API in acts container, which returns 200 OK on requesting it.
For the Crash server, we have a global variable stat in the program. A POST request to /api/v1/_crash will set the stat variable to 0. In acts container whenever a HTTP request is received it first check the value of the stat variable and if the value is 0, it responds with 500 Internal server error.  


## Load Balancing  

Here we have another flask program which is orchestrator that acts as a parent to all the acts container. The parent flask program will receive requests on port 80 on the instance, call the retrunport() function(will be introduced soon) and forward it to the port given by this function.For Load Balancing, we have used the round-robin algorithm.


Database Schema:  
Container number, Port number, Status, Turn  
Example:  
	Container 1 , 8000,True,1  
	Container 2 , 8001,True,0  
A function returnport() will read the database and check for which container turn it is, store it in some local variable, make the current turn to zero, make next turn to one and then return the value of the local variable that stores the value of the port to which the HTTP request is to be forwarded.  


## Fault Tolerance
Here we have created a function called timer() which will poll the health check API of each acts container every one second. And created a thread and passed timer function as the target to it.
We have another function relaunch_port(port) which will relaunch the container on the port, that takes a port number as an argument. As soon as the health check API founds that the status of the container is FALSE it calls relaunch_port(port) and a new container is launched on that port.  

## Auto-Scaling  
We have two functions launch and stop, which will launch and stop the containers based on the number of requests received in the last 2 mins.
launch function reads the database and checks for which is the container which has the highest port number value, then launches a container on the port value one more than the highest port number and then adds this entry to the database.
stop function reads the database and checks for which is the container which has the highest port number value, then removes a container on the port and then deletes this entry from the database.   

## Generic Load Balancer
Here in flask program of the Parent orchestrator, we have three API’s which will respond to GET, POST and DELETE requests in a generic manner. Means all the get requests will be picked up by the same API in the Parent flask program, similarly for POST and DELETE.



