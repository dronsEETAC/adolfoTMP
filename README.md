**<h1>Multiple drone control in the Drone Engineering Ecosystem</h1>**

This is a project which has been made as a contribution to the collaborative project Drone Engineering Ecosystem. The main goal was to develop a desktop application using Python and CustomTkinter which makes possible to fly up to four drones at the same time inside the DroneLab in the EETAC (UPC) campus. This application allows the user to:
  - Display and movement tracking of up to four drones in the main panel.
  - Configuration of the geofence and its parameters for each drone.
  - Return To Launch maneuver for each drone from the main panel.
  - Secondarily it allows to pilot each drone from the app.
  - 

    ![tfgGithub](https://github.com/adolfosanmartin/adolfosanmartin-Multiple-Drone-Control-DEE/assets/159135459/ae946a58-3359-465f-88e9-b2ae0643d1c3)
    

**<h1>Demo</h1>**

In order to undersand how to to use this application a demonstration has been done in the following video: LINK.

The demonstration consists of four drones being simulated from the Mission Planner simulator. Through this video you will see all the funcionalities of the application and which order you should follow to run it successfully.

Moreover there is also a video explaining how the code of the application works. See the following link: LINK. 


**<h1>Contribution and installation</h1>**

In case you want to contribute to this project you will need to install Python 3.7. It is recommended to use Pycharm as your working environment as it provides lots of facilities for your coding. You will also need to install Mosquitto broker in order to get the Autopilot Service file working. This broker will be always run in localhome (port 1884) when simulating. Thus you will need to create a folder in your Mosquitto broker folder containing the following information:

listener 1884  

allow_anonymous true

For more information visit the Drone Engineering Ecosystem GitHub, https://github.com/dronsEETAC/DroneEngineeringEcosystemDEE.
    
