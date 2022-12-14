def getChannel_Statistics(youtube,channel_id):
    
    """
    Get channel statistics: title, subscriber count, view count, video count, upload playlist
    Params:
    
    youtube: the build object from googleapiclient.discovery
    channels_ids: list of channel IDs
    
    Returns:
    Dataframe containing the channel statistics for all channels in the provided list: title, subscriber count, view count, video count, upload playlist
    
    """
    
    all_data=[]
    
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=','.join(channel_id)
        )
    response = request.execute()
    
    for item in response['items']:
        data={'channelName':item['snippet']['title'],
             'suscribers':item['statistics']['subscriberCount'],
             'views':item['statistics']['viewCount'],
             'totalVideos':item['statistics']['videoCount'],
             'playList':item['contentDetails']['relatedPlaylists']['uploads']
             }
        all_data.append(data)

    return(pd.DataFrame(all_data))

def get_video_ids(youtube,playlist_id):
    
    video_ids=[]
    request = youtube.playlistItems().list(
                part="snippet,contentDetails",
                playlistId=playlist_id,
                maxResults=50
            )
    response = request.execute()

    for item in response['items']:
        video_ids.append(item['contentDetails']['videoId'])
            
    next_page_token=response.get('nextPageToken')
    
    while next_page_token is not None:
        request = youtube.playlistItems().list(
                part="snippet,contentDetails",
                playlistId=playlist_id,
                maxResults=50
            )
        response = request.execute()

        for item in response['items']:
            video_ids.append(item['contentDetails']['videoId'])
            
        next_page_token=response.get('nextPageToken')
        
    return video_ids

def get_video_details(youtube,video_ids):
    all_videoInfo=[]

    for i in range(0,len(video_ids),50):
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=','.join(video_ids[i:i+50])
        )
        response = request.execute()

        for video in response['items']:
            stats_to_keep={'snippet':['channelTitle','title','description','tags','publishedAt'],
                          'statistics':['viewCount','likeCount','favouriteCount','commentCount'],
                          'contentDetails':['duration','definition','caption']
                          }
            video_info={}
            video_info['video_id']=video['id']

            for k in stats_to_keep.keys():
                for v in stats_to_keep[k]:
                    try:
                        video_info[v]=video[k][v]
                    except:
                        video_info[v]=None

            all_videoInfo.append(video_info)
    
    return pd.DataFrame(all_videoInfo)

def get_comment_in_videos(youtube,video_ids):
    all_comments=[]
    
    for video_id in video_ids:
        request=youtube.commentThreads().list(
            part="snippet,replies",
            videoId=video_id
        )
        response=request.execute()
        
        comments_in_video=[comment['snippet']['topLevelComment']['snippet']['textOriginal'] for comment in response['items'][0:10]]
        comments_in_video_info={'video_id':video_id,'comments':comments_in_video}
        
        all_comments.append(comments_in_video_info)
    
    return pd.DataFrame(all_comments)
