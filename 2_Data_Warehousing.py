# Import the libraries below for streamlit application, connecting to mysql and use datetime functions
import streamlit as st
import mysql.connector
from datetime import datetime
import isodate

# This function sets the title for the page.
st.title('Youtube Data Warehousing')

# If insert to SQL button is clicked, then the following functions are executed.
if(st.button('Insert to SQL')):
    
    # To create connection between python and mysql
    mydb = mysql.connector.connect(host="localhost", user="root", password="sakthi", auth_plugin='mysql_native_password')

    # Creating a memory space to execute the statements 
    mycursor = mydb.cursor()

    mycursor.execute("CREATE database IF NOT EXISTS Youtube")

    mycursor.execute("USE Youtube")

    # Table creation function
    def table_creation():
        mycursor.execute('''CREATE table IF NOT EXISTS channel (
                                channel_id varchar(255) UNIQUE NOT NULL ,
                                channel_name varchar(255) NOT NULL,
                                channel_description text,
                                channel_subscriptions int,
                                channel_views int,
                                channel_videos int,
                                playlist_id varchar(255) PRIMARY KEY
                            )''')                   

        mycursor.execute('''CREATE table IF NOT EXISTS video (
                                video_id varchar(255) PRIMARY KEY,
                                playlist_id varchar(255),
                                video_name varchar(255) NOT NULL,
                                video_description text,
                                video_tags varchar(500),
                                published_date datetime,
                                views_count int,
                                likes_count int,
                                favorite_count int,
                                comment_count int,
                                duration int,
                                thumbnail varchar(255),
                                caption_status varchar(255),
                                FOREIGN KEY (playlist_id) REFERENCES channel(playlist_id)
                                )''')

        mycursor.execute('''CREATE table IF NOT EXISTS comment ( 
                                comment_id varchar(255) PRIMARY KEY,
                                video_id varchar(255),
                                comment_text text,
                                comment_author varchar(255),
                                comment_published_date datetime,
                                FOREIGN KEY (video_id) REFERENCES video(video_id)
                                )''')


    # Inserting extracted channel data to mysql
    def insert_channel_data(channel_data):   
        sql = ''' INSERT INTO channel (channel_id, channel_name, channel_description, channel_subscriptions, 
                                       channel_views, channel_videos, playlist_id) values(%s, %s, %s, %s, %s, %s, %s)'''
        
        val = (channel_data['Channel_Id'], channel_data['Channel_Name'], channel_data['Channel_Description'], 
               int(channel_data['Channel_Subscription_Count']),int(channel_data['Channel_Views']), 
               int(channel_data['Channel_Videos']), channel_data['Channel_Playlist_Id'])
        
        mycursor.execute(sql, val)
        mydb.commit()

        
    # This function is used to change the datatype from string to datetime
    def date_time_format(date_str):
        str_dt = datetime.fromisoformat(date_str)
        dt_str =  str_dt.strftime('%Y-%m-%d %H:%M:%S')
        dt_time = datetime.strptime(dt_str,'%Y-%m-%d %H:%M:%S')

        return dt_time
        

    # Inserting extracted video data to mysql
    def insert_video_data(video_data):
        for vid in range(0,len(video_data)):

            # 'Video_Tags' is in list datatype, so we are combining all the tags to single string function.
            tag = ''
            for i in video_data[vid]['Video_Tags']:
                tag+=i+','

            # Replacing the changed dataype value for 'Video_Tags'
            video_data[vid]['Video_Tags'] = tag[:len(tag)-1]
        
            dt_tm = date_time_format(video_data[vid]['Published_At'])
        
            # Replacing the changed dataype value for 'Published_At'
            video_data[vid]['Published_At'] = dt_tm
        
            # This function parses the ISO 8601 duration string into a timedelta object.
            conv = isodate.parse_duration(video_data[vid]['Duration'])
            
            #  This function converts the timedelta object into the total number of seconds and then converted to int
            dur_secs = int(conv.total_seconds())
        
            # Replacing the changed dataype value for 'Duration'
            video_data[vid]['Duration'] = dur_secs
        

            sql = ''' INSERT INTO video (video_id, playlist_id, video_name, video_description, video_tags, published_date, 
                                         views_count, likes_count,favorite_count, comment_count, duration, 
                                         thumbnail, caption_status) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        
            val = (video_data[vid]['Video_Id'], video_data[vid]['playlist_id'], video_data[vid]['Video_Name'], 
                   video_data[vid]['Video_Description'], video_data[vid]['Video_Tags'], video_data[vid]['Published_At'], 
                   int(video_data[vid]['Views_Count']), int(video_data[vid]['Likes_Count']), int(video_data[vid]['Favorite_Count']), 
                   int(video_data[vid]['Comment_Count']), video_data[vid]['Duration'], video_data[vid]['Thumbnail'],
                   video_data[vid]['Caption_Status'])
        
            mycursor.execute(sql, val)
            mydb.commit()

            
    # Inserting extracted comment data to mysql
    def insert_comment_data(comment_data):
        for cid in range(0,len(comment_data)):

            # Changing the datatype of 'Comment_PublishedAt'
            dat_tim = date_time_format(comment_data[cid]['Comment_PublishedAt'])

            # Replacing the changed dataype value
            comment_data[cid]['Comment_PublishedAt'] = dat_tim

            sql = ''' INSERT INTO comment (comment_id, video_id, comment_text, comment_author, comment_published_date)
                                           values(%s, %s, %s, %s, %s)'''
        
            val = (comment_data[cid]['Comment_Id'], comment_data[cid]['Video_id'], comment_data[cid]['Comment_Text'], 
                   comment_data[cid]['Comment_Author'], comment_data[cid]['Comment_PublishedAt'])
        
            mycursor.execute(sql, val)
            mydb.commit()
    

    # To avoid dupicate entires of channels details we set UNIQUE constraint for channel id column.
    # So if any exisitng channel_id is entered by the user, it will not be inserted and displays the "Channel already exists" message.
    # We have handled the duplicate entry error with exceptional handling.
    def insert_to_sql():
        try:
            table_creation()
            insert_channel_data(st.session_state["channel_data"] )
            insert_video_data(st.session_state["video_data"])
            insert_comment_data(st.session_state["comment_data"])
            st.success("Inserted to SQL")
        except:
            st.success("Channel already exists")


    insert_to_sql()