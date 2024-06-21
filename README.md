# Youtube Data Harvesting and Data Warehousing

This project explains about collecting the data from the Youtube and store it in a database for analysing the data.

# Table of Contents

# Introduction

The main aim of the project is to create a streamlit application which allows the user to access and analyse the data from multiple Youtube channels.

This application has the following features:

1. Takes the input from the user and retrieves all the relavent data of the respective channel.
2. An option is provided to store the data in MYSQL database to use it for further purpose.
3. Ability to store multiple channel data in the database.
4. It has a set of questions from which user can choose to analyse the retreived data from multiple channels.


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

2. googleapiclient

* To connect with Google Cloud Console

```
pip install google-api-python-client
```

3. mysql connector

* To connect with MYSQL database

```
pip install mysql-connector-python

```
4. pandas

* To display the data in the form of Dataframe

```
pip install pandas

```

5.Datetime

* To convert a value from string to datetime datatype
```
pip install DateTime
```

6. isodate

* To convert ISO 8601 duration string into a timedelta object

```
pip install isodate

```

## Google API Key

* Create an API key in Google Cloud Console.
  
* This API key is an unique key to access the Google API which acts as an intermediate between Google server and client which is python.


