# Locust-Taurus

## Table of contents
* [General info](##general-info)
* [Technologies](##technologies)
* [Setup](##setup)


## General Info
* The aim of this project is to perform (performance testing) for a technology that uses socketIO

## Technologies:
Project is created with:
* Locust
* Taurus
* Python

## Setup
To run this project, install these requirements locally:
* Install python
* pip install locust
* install dependencies

### Execute project with locust:
  * locust -f file.py, 
    and the locust UI will open on http://localhost:8089/

### Execute project without locust UI
  * locust -f src/demo_requests.py -u <users> -r 1 --headless
  
### Execute just a file.py:
  * py file.py

### Execute project with Taurus
  * Docker must be running on the computer.
  * If you want to run the project in the cloud, execute: 
    docker run -it --rm -v path/(project name)):/bzt-configs (blazemetr image):latest script.yml -cloud
    
  * If you want to run the project local, execute: 
    docker run -it --rm -v path/Locust-Taurus:/bzt-configs graviel/blazemeter:latest script.yml -local