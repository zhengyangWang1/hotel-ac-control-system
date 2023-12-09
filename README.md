# README

choose another language：

- zh_CN [简体中文](readme/README_ch.md)

# hotel-ac-control-system
Django full stack frame


## project architecture
- air conditioning control interface

    Main features:
    - user registration and login
    - control the opening and closing of the air conditioner, and change the air speed and temperature of the air conditioner.
    - display current room temperature, target temperature, cost, and wind speed
- air conditioning monitoring interface
    Main features:

    - display the air conditioning status of each room, including temperature, wind speed and cost
- front desk interface

    Main features:
    - download the air conditioning usage list (CSV file) for each room
## project background
Bupt Cheap Hotel is located in College Station City, outside the fifth ring road of the capital. The hotel was founded in 2000, after 10 years of operation has accumulated a good reputation, in order to respond to the government's concept of green business, expected to build air-conditioning temperature control billing system: advocating the use of more pay, less pay, do Not Pay the bill model, cost-saving at the same time so that customers can always see the amount spent, to achieve a number of savings in mind, further attracting young people to stay. The hotel has a total of 5 rooms, but due to free resources, a maximum of 3 rooms open air conditioning.
## backend implementation
Scheduling strategy
The basic scheduling strategy is: Priority Scheduling + time slice scheduling. The priority scheduling is based on the requested wind speed, so the priority strategy should be considered first
1) when the number of service objects is less than the maximum number of service objects, all requests will be assigned a service object;
2) when the number of service objects is greater than or equal to the upper limit of service objects, start the scheduling policy: first, determine whether the priority policy is satisfied; the wind speed of the requested service and the wind speed of the service objects:

- 2.1. If the decision = is greater than, the priority scheduling policy is initiated, and several service objects are judged to have a lower wind speed than the request wind speed:

    - 2.1.1 if there is only one, the room is placed in a waiting queue and assigned a waiting service time: the service object is released and assigned to a new request object;
    - 2.1.2 if more than one service object has the same wind speed and is lower than the requesting object, the service object with the longest service time is released and assigned to the new requesting object, and the room is placed in the waiting queue, and allocating a waiting time;
    - 2.1.3 if the wind speed of more than one service object is lower than the requested wind speed and the wind speed is not equal, the service object with the lowest wind speed is released, and the room is placed in a waiting queue and assigned a waiting service time;

- 2.2 if judgment = equal, the timeslice scheduling policy is started
    
    - 2.2.1 place the request object in a wait queue and allocate a wait service time;
    - 2.2.2 during these two minutes, if there is no change in the service state, the service object with the longest service time in the service queue is released when the wait time = 0 and the room is placed in the wait queue, and is assigned a waiting service time: The Waiting Service object is assigned a service object to start the service;
    - 2.2.3 during this two-minute wait, if the target temperature of any service object reaches or shuts down (which means the service object is released) , the object with the least waiting time in the waiting queue gets the service object
- 2.3 if the judgment = is less than, the request object must wait until a service object is idle before it is available Services.

## A rebound strategy
Air-conditioning adjustable temperature range 18-25, open air-conditioning every minute heating 0.5 degrees, when the air-conditioning waiting for service, the room temperature unchanged. When the air conditioner is turned off, the room temperature drops by 0.5 degrees per minute until it reaches the initial temperature.

## Billing strategy
The rate is only related to wind speed. High winds are 1 yuan per minute, strokes are 0.5 yuan per minute, and low winds are 1/3 yuan per minute.
