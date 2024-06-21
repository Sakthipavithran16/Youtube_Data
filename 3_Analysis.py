# Import the libraries below for streamlit application, connecting to mysql and view the data as dataframe
import streamlit as st
import pandas as pd
import mysql.connector

# To create connection between python and mysql
mydb = mysql.connector.connect( host="localhost", user="root", password="sakthi", auth_plugin='mysql_native_password' )

# Creating a memory space to execute the statements 
mycursor = mydb.cursor()

mycursor.execute("USE Youtube")

# This function sets the title for the page.
st.title('Youtube Data Analysis')

# Storing the list of questions in lst_questions variable
lst_questions = ["1. What are the names of all the videos and their corresponding channels?",
                 "2. Which channels have the most number of videos, and how many videos do they have?",
                 "3. What are the top 10 most viewed videos and their respective channels?",
                 "4. How many comments were made on each video, and what are their corresponding video names?",
                 "5. Which videos have the highest number of likes, and what are their corresponding channel names?",
                 "6. What is the total number of likes for each video, and what are their corresponding video names?",
                 "7. What is the total number of views for each channel, and what are their corresponding channel names?",
                 "8. What are the names of all the channels that have published videos in the year 2022?",
                 "9. What is the average duration of all videos in each channel, and what are their corresponding channel names?",
                 "10. Which videos have the highest number of comments, and what are their corresponding channel names?"]

# Creating a dropdown list which consists of questions
select_question = st.selectbox(
    "What Analysis you want",
    options = lst_questions,
    index=None,
    placeholder="Select any question"
)

# When user selects first question, then the answer is displayed in the form of dataframe
if select_question == "1. What are the names of all the videos and their corresponding channels?":
    mycursor.execute('''SELECT  video_name, channel_name
                        FROM  video v
                        INNER JOIN channel c on v.playlist_id = c.playlist_id''')

    myresult = mycursor.fetchall()

    st.write("")

    st.write(pd.DataFrame(myresult, columns = ['Video_name','Channels' ]))


# When user selects second question, then the answer is displayed in the form of dataframe
if select_question == "2. Which channels have the most number of videos, and how many videos do they have?":
    mycursor.execute('''SELECT channel_name, channel_videos
                        FROM channel
                        WHERE channel_videos = (SELECT max(channel_videos) FROM channel)''')

    myresult = mycursor.fetchall()

    st.write("")

    st.write(pd.DataFrame(myresult, columns = ['Channels','Total_Videos' ]))


# When user selects third question, then the answer is displayed in the form of dataframe
if select_question == "3. What are the top 10 most viewed videos and their respective channels?":
    mycursor.execute('''SELECT channel_name, video_name, views_count
                        FROM video v
                        INNER JOIN channel c on v.playlist_id = c.playlist_id
                        ORDER BY views_count desc
                        LIMIT 10''')

    myresult = mycursor.fetchall()

    st.write("")

    st.write(pd.DataFrame(myresult, columns = ['Channels','Video_Name', 'Views']))


# When user selects fourth question, then the answer is displayed in the form of dataframe
if select_question == "4. How many comments were made on each video, and what are their corresponding video names?":
    mycursor.execute('''SELECT video_name, comment_count
                        FROM video''')

    myresult = mycursor.fetchall()

    st.write("")

    st.write(pd.DataFrame(myresult, columns = ['Video_name', 'Total_comments']))


# When user selects fifith question, then the answer is displayed in the form of dataframe
if select_question == "5. Which videos have the highest number of likes, and what are their corresponding channel names?":
    mycursor.execute('''SELECT channel_name, video_name, likes_count
                        FROM  video v
                        INNER JOIN channel c on v.playlist_id = c.playlist_id
                        WHERE likes_count = (SELECT max(likes_count) FROM video)''')

    myresult = mycursor.fetchall()

    st.write("")

    st.write(pd.DataFrame(myresult, columns = ['Channels','Video_name', 'Likes']))


# When user selects sixth question, then the answer is displayed in the form of dataframe
if select_question == "6. What is the total number of likes for each video, and what are their corresponding video names?":
    mycursor.execute('''SELECT video_name, likes_count
                        FROM video''')

    myresult = mycursor.fetchall()

    st.write("")

    st.write(pd.DataFrame(myresult, columns = ['Video_name', 'Likes']))


# When user selects seventh question, then the answer is displayed in the form of dataframe
if select_question == "7. What is the total number of views for each channel, and what are their corresponding channel names?":
    mycursor.execute('''SELECT channel_id, channel_name, channel_views
                        FROM channel''')

    myresult = mycursor.fetchall()

    st.write("")

    st.write(pd.DataFrame(myresult, columns = ['Channel_id','Channels', 'Total_views']))


# When user selects eighth question, then the answer is displayed in the form of dataframe
if select_question == "8. What are the names of all the channels that have published videos in the year 2022?":
    mycursor.execute('''SELECT distinct channel_name
                        FROM video v
                        INNER JOIN channel c on v.playlist_id = c.playlist_id
                        WHERE year(published_date) = 2022''')

    myresult = mycursor.fetchall()

    st.write("")

    st.write(pd.DataFrame(myresult, columns = ['Channels']))


# When user selects nineth question, then the answer is displayed in the form of dataframe
if select_question == "9. What is the average duration of all videos in each channel, and what are their corresponding channel names?":
    mycursor.execute('''SELECT channel_id, channel_name, round(avg(duration),0)
                        FROM video v
                        INNER JOIN channel c on v.playlist_id = c.playlist_id
                        GROUP BY channel_id,channel_name''')

    myresult = mycursor.fetchall()

    st.write("")

    st.write(pd.DataFrame(myresult, columns = ['Channel_id', 'Channels', 'Average_duration_in_sec']))


# When user selects tenth question, then the answer is displayed in the form of dataframe
if select_question == "10. Which videos have the highest number of comments, and what are their corresponding channel names?":
    mycursor.execute('''SELECT channel_name, video_name, comment_count
                        FROM video v
                        INNER JOIN channel c on v.playlist_id = c.playlist_id
                        WHERE comment_count = (SELECT max(comment_count) FROM video)''')

    myresult = mycursor.fetchall()

    st.write("")

    st.write(pd.DataFrame(myresult, columns = ['Channels', 'Video_name', 'Total_comments']))