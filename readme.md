# Data Pipeline: Sales Analysis


## Description
As a retail organisation with vasts amounts of data, we need a data warehouse to capture all our data from the various sources like CRM systems, POS systems, website data etc which can then be used for various downstream processes like Analytics, ML etc
This repo contains code to extract data from APIs, flat file in file system which are then written to a datalake

Further data is transformed and various metrics are generated from the data and written to the data warehouse 


## Table of Contents
* data: Holds flat file data (This is a place holder, in real world this would be some other data source like s3)
* data_extraction: Holds data to capture raw data from APIs/ file system and writes them to dl
* data_validates: Validates various data to ensure integrity
* data_load: Loads data aggregations/stats to data warehouse


## Installation
Ensure installation of the below in your machine
1. Python
2. Docker
3. sqllite

## Usage


1. Download the repo from github with <br> ``git clone <<>>``
2. Navigate to the root directory of the project <br> ``cd dp_sales_analysis`` 
3. run <br> ``docker build -t dp_sales_analysis .``
4. run <br> ``docker run -v $(pwd):/dp_sales_analysis dp_sales_analysis``


## Database Schema

Please navigate to https://miro.com/app/board/uXjVM1N4nJA=/?share_link_id=376431550208


<iframe width="768" height="432" src="https://miro.com/app/live-embed/uXjVM1N4nJA=/?moveToViewport=-1319,838,4704,2704&embedId=288440545635" frameborder="0" scrolling="no" allow="fullscreen; clipboard-read; clipboard-write" allowfullscreen></iframe>
