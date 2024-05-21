# Frontend Documentation

## Overview

This repository contains the frontend components for visualizing data collected from our backend server. The visualizations are primarily conducted through Jupyter Notebooks (frontend.ipynb) located in various subfolders.

## Prerequisites

Before using this frontend, ensure you are connected to the University of Melbourne's VPN or are within the campus network. Additionally, set up the environment by running the following commands:

1. Source the project's OpenStack RC file:
   source ./unimelb-comp90024-2024-grp-55-openrc.sh

2. Connect to the backend services using SSH and port forwarding:
    ssh -i <path-to-private-key> (e.g. ~/Downloads/mykeypair.pem) -L 9090:$(openstack coe cluster show elastic -f json | jq -r '.master_addresses[]'):6443 ubuntu@$(openstack server show bastion -c addresses -f json | jq -r '.addresses["qh2-uom-internal"][]')

3. Forward the required ports:
    kubectl port-forward service/router -n fission 9090:80

## Folder Structure
aircondition_vs_sentiment/: Analysis of air quality versus sentiment.
aircondition_vs_weather/: Analysis of air quality versus weather conditions.
child_vs_aircondition/: Analysis of the average air quality score around each child care center
methods_of_residents/: Analysis of residents' travel methods.
weather_vs_sentiment/: Analysis of weather conditions versus sentiment.
oneDayAnalysis/: Visualization of daily weather and PM2.5 data.
- all the main.py file in the above folder were only used for local testing, no need for call them inside frontend.ipynb
- all the other functions above will be called by frontend.ipynb

dataInOneDay/: Stores real-time daily weather and air quality data.
realtimeData/: Stores all the collected data on air quality, weather, and Mastodon social media posts.