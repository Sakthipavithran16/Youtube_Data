# Youtube Data Harvesting and Data Warehousing

This project explains about collecting the data from the Youtube and storing it in a database for analysing the data.


# Table of Contents

1. Introduction

2. Key Skills

3. Installation

4. Information about data

5. Workflow

6. References



# Introduction

The main aim of the project is to create a streamlit application which allows the user to access and analyse the data from multiple Youtube channels.


This application has the following features:

1. Takes the input from the user and retrieves all the relavent data of the respective channel.
2. An option is provided to store the data in MYSQL database to use it for further purpose.
3. Ability to store multiple channel data in the database.
4. It has a set of questions from which user can choose to analyse the retreived data from multiple channels.


# Key Skills

1. Python scripting
   
2. Data Collection
   
3. Streamlit

4. API integration

5. Data Management using SQL 


# Installation

## Prerequisites

1. Python
2. VS Code
3. Google Cloud Console account


## Libraries in Python

1. Streamlit
   
* To build Streamlit web application


 ```
pip install streamlit
 ```


2. Googleapiclient

* To connect with Google Cloud Console


```
pip install google-api-client
```


3. MYSQL Connector

* To connect with MYSQL database


```
pip install mysql-connector-python

```


4. Pandas

* To display the data in the form of Dataframe


```
pip install pandas

```


5.Datetime

* To convert a value from string to datetime datatype

  
```
pip install DateTime
```


6. Isodate

* To convert ISO 8601 duration string into a timedelta object


```
pip install isodate

```


## Google API Key

* Create an API key in Google Cloud Console.
  
* This API key is an unique key to access the Google API which acts as an intermediate between Google server and client.



# Workflow

1. Connect to the Youtube API

* Conneting to the Youtube API with the hekp of API key to retreive the channel details from the Google server.

```
api_key = '**YOUR API KEY**'
youtube = build('youtube', 'v3', developerKey=api_key)

```

2. Storing  and cleaning data

* We should request the Youtube with some parameters and a response is received from the server which contains the data.

* Part parameter

* snippet : includes basic details about the channel, such as its title, description, and thumbnail image.
* statistics : includes information about the channel's performance and engagement, such as the number of subscribers, views, and comments.
* contentDetails: includes additional information about the channel's content, such as the uploads playlist and the channel's featured channels.

* channel id should be passed for id parameter

* With the help of these parameters, a response is received which contains the data for channel.

* In the response ITEMS key has the information about the channel.

* Extract the required data from the ITEM keys and store it in a variable.


* Repeat these steps to collect the video and comment data respectively.

* Use the neccesary functions to get reponse for channel, video and comment data respectively.

* Once all the data is colleted, it should be cleaned like converting to appropiate datatype to store it in database.

* This is known as Data Harvesting.


3. Migrate data to a SQL database

*  After you've collected data for multiple channels, you can migrate it to a MYSQL database.

* Create a database and seperate tables for channel, video and comment data.
  
* These tables should be created with appropiate constraints so that exisiting channels should not be inserted.

* Insert the cleaned data of channel, video and comment into respective tables.

* This is known as Data Warehousing.

* In this project, we have connected the python and MySQL to do the above operations.


4. Analysing the data

* Query the data using SQL commands in MySQL database for finding the insights about our multiple channel informations.


5. Streamlit application

* Use Streamlit to display these analysis of the collected Youtube data for multiple channels.


* Overall, this approach involves building a simple UI with Streamlit, retrieving data from the YouTube API, storing the data SQL as a warehouse, querying the data warehouse with SQL, and displaying the data in the Streamlit app.















