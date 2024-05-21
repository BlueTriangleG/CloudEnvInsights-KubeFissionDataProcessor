# Introduction

This folder is mainly used to store the backend code. The core equations here are deployed to MRC's K8s using fission. There are two main folders where the fission code is stored, apiInterface and dataCrawAndProcess. I'll describe the functionality and structure of this code in more detail.

## framework

In both of these core functional blocks, I use a format that facilitates fission deployment, with the base format being:
-- function area
-- functions
-- specs
The functions will hold the fission functions for this function block, and the specs will hold the yaml configuration file for the fissoin deployment. I can use the fission command to use the yaml configuration file in specs to deploy my code in fission. It also saves a zip archive that can be used to build the fission package environment later. You can also use yaml to configure the fission router for subsequent calls.

### dataCrawAndProcess

In this code mainly stores the data crawler, which mainly crawls data from 3 data sources:

1. aircondition is a function that crawls Melbourne's current bpm2.5.
2. mastodon-aus-social This function is mainly used to crawl the chat logs of aus area in mastodon. 
3. weathercondition This function is mainly used to crawl the latest weather data of Melbourne for subsequent data analysis.

### apiInterface

This code is mainly used to store the interface between fission and the elasticsearch database, which can be used to call it remotely so that it can interact with the database.

1. getfulldata:

   - This function is mainly used for the fission router to connect to the database and extract all the data of the specified database topic through restful api.
     - Restful api design:
       - curl -X GET http://$FISSION_ROUTER/database/{datatype:[a-zA-Z0-9-]+}
         Use this restful api to access this function in fission where datatype is the data topic name.

2. get-timeperioddata:

   - This function mainly connects to the database via fission router, and extracts the time period information via restful api, so that we can extract the data in a specific time range from a specific topic in the elastic search database.
     - Resftul api design:
       - curl -X GET http://$FISSION_ROUTER/database/{datatype:[a-zA-Z0-9-]+}/{startdate:[0-9]{4}-[0-1][0-9]-[0-3][0-9]-[0-2][0-9]}/{enddate:[0-9]{4}-[0-1][0-9]-[0-3][0-9]-[0-2][0-9]}
         Use this restful api to access this function in fission. where datatype is: the database where your database is located. startdate is the start time of the time range and enddate is the end time of the time range.

3. put-database:
   - This function connects to a database via a fission router and transfers a json file to the remote database via a restful api. This allows you to transfer a file to a specific topic in the elastic search database.
     - Resftul api design:
       - curl -X POST http://$FISSION_ROUTER/database/{datatype:[a-zA-Z0-9-]+}
         Use this restful api for the put-database function in fisison, where dabase is the name of the database topic you want to transfer data to. You need to transfer a json file.
