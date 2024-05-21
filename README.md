## Introduction to our project

This project designs and implements a cloud data processing system based on Kubernetes and Fission framework on the OpenStack server platform. This system can automatically crawl and process raw real-time data through Fission Trigger, and store and manage it via Elasticsearch.

For data anlysis, this project will explore several different scenarios that underscore the critical role of sustainable practices in urban environments. We aim to help people get to know more about the impact of the environment on daily life, find the potential linkage between humans and the environment, and ask people to focus more on climate protection.

## Entry point

Enter the frontend folder to access our key functionalities. There is a detailed explanation of the function call inside the file readme.

## Project structure

This project code mainly consists of these structures as follows:

- backend
  - The backend folder consists of functions and packages deployed in fission. It is divided into two main sections: data craw and preprocess and the main data store fetching api for our project.
- data
  - The data folder consists mainly of the data we extracted and analysed from the previous section.
- database
  - The database folder should contain our design code for the database and the design framework.
- docs
  - The docs folder contains our design documentation for our system.
- frontend
  - The frontend folder contains our data extraction code and data analysis code. It is the main location of our system to display the results. Jupyter notebook is used to implement the frontend function.
- test
  - The test folder contains mostly test scripts for our teammates our system.

## Contributer

GaoyuanHao
Jinuo Sun
Yulin Dong
Jin Wang
Zihan Xu
