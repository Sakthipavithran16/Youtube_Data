# Import the libraries below to use streamlit application and googleapiclient functions
import streamlit as st
import googleapiclient.discovery


# Create your Api key and use it for data extraction.
api_key = "AIzaSyDxbDE-5y0PX_br5-fcWQ4vhEkwIBeaYkQ"

api_service_name = "youtube"
api_version = "v3"

# Connecting with Google cloud console to collect data 
youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)


st.set_page_config(page_title="Youtube")

# To use variables in other pages of stramlit app we use st.session_state.
# Since this is the first page and variables not availabe we assign None values.
if "channel_data" not in st.session_state:
    st.session_state["channel_data"]= None

if "video_data" not in st.session_state:
    st.session_state["video_data"]= None

if "comment_data" not in st.session_state:
    st.session_state["comment_data"]= None


# This function sets the title for the page.
st.title('Youtube Data Harvesting')


# Getting channel_id from the user
channel_id = st.text_input("Enter Channel ID")


# The following functions will be executed if Scrap button is clicked by user.
if(st.button('Scrap')):
    def channel_details(channel_id):
        # We are requesing to the server with required parameter to get channel data
        ch_request = youtube.channels().list(
            part="snippet,contentDetails,statistics",
            id= channel_id
        )

        # From the server response will be recieved
        ch_response = ch_request.execute()

        # We are extracting the required channel details with the response we received
        channel_info = {
            "Channel_Id":channel_id,
            "Channel_Name":ch_response["items"][0]["snippet"]["title"],
            "Channel_Description":ch_response["items"][0]["snippet"]["description"],
            "Channel_Playlist_Id":ch_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"],
            "Channel_Subscription_Count":ch_response["items"][0]["statistics"]["subscriberCount"],
            "Channel_Views":ch_response["items"][0]["statistics"]["viewCount"],
            "Channel_Videos":ch_response["items"][0]["statistics"]["videoCount"]
        }

        return channel_info
    


    def video_id_list(playlist_id):
        video_id = []
        next_page = ''

        while True:
            # Requesting the server with playlist_id and other parameters to get video_id list
            pl_request = youtube.playlistItems().list(
                part="snippet",
                playlistId = playlist_id,
                maxResults = 50,                    
                pageToken = next_page
            )

            # Response will have multiple pages if there is more the 50 videos 
            pl_response = pl_request.execute()

            # Looping through the response to collect the video_id
            for item in pl_response["items"]:
                video_id.append(item["snippet"]["resourceId"]["videoId"])
            
            # Getting the nextPageToken to navigate to next page of response
            next_page = pl_response.get("nextPageToken")

            # If we reached the last page then the loop is breaked
            if next_page is None:
                break

        return video_id

    

    def video_details(video_lst):
        video_info = []

        # Looping through the video id to get the details of all the videos in the channel.
        for id in video_lst:
            video_request = youtube.videos().list(
                part="snippet,contentDetails,statistics",
                id=id
            )

            video_response = video_request.execute()
            
            # Extracting the data with help of get() to avoid key error. If key is not found, then it takes given default value
            video_info.append({
                "Video_Id":id,
                "playlist_id": playlist_id,
                "Video_Name":video_response["items"][0]["snippet"]["title"],
                "Video_Description":video_response["items"][0]["snippet"]["description"],
                "Video_Tags":video_response['items'][0]['snippet'].get("tags", "No tags"),
                "Published_At":video_response["items"][0]["snippet"]["publishedAt"],
                "Views_Count":video_response["items"][0]["statistics"].get("viewCount", "0"),
                "Likes_Count":video_response["items"][0]["statistics"].get("likeCount", "0"),
                "Favorite_Count":video_response["items"][0]["statistics"].get("favoriteCount", "0"),
                "Comment_Count":video_response["items"][0]["statistics"].get("commentCount", "0"),
                "Duration": video_response["items"][0]["contentDetails"]["duration"],
                "Thumbnail":video_response["items"][0]["snippet"]["thumbnails"]["default"]["url"],
                "Caption_Status":video_response["items"][0]["contentDetails"]["caption"]
            })
            
        return video_info

    
    
    def comment_details(video_lst):
        comment_info =[]

        # Some of the videos have disabled the comments. So we are using exceptional handling to handle errors.
        # If the video has disabled comments, then it will continue to next video to extract comment data.
        for id in video_lst:
            try:
                comment_request = youtube.commentThreads().list(
                    part="snippet",
                    videoId=id,
                    maxResults = 100
                )
                comment_response = comment_request.execute()

            except:
                continue

            else:
                for comment in comment_response["items"]:
                    comment_info.append({
                        "Comment_Id": comment["snippet"]["topLevelComment"]["id"],
                        "Video_id" : id,
                        "Comment_Text": comment["snippet"]["topLevelComment"]["snippet"]["textDisplay"],
                        "Comment_Author": comment["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"],
                        "Comment_PublishedAt": comment["snippet"]["topLevelComment"]["snippet"]["publishedAt"]
                    })   
            
        return comment_info
        

    # Calling all the functions to get channel, video, comment data and stored in respective variable 
    st.session_state["channel_data"] = channel_details(channel_id)
    playlist_id = st.session_state.channel_data["Channel_Playlist_Id"]
    video_lst = video_id_list(playlist_id)
    st.session_state["video_data"] = video_details(video_lst)
    st.session_state["comment_data"] = comment_details(video_lst)

    # If data is successfully extracted then the below message is displayed to user.
    st.success("Data successfully collected")
