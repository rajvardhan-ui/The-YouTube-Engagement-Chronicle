import pymysql
from datetime import datetime
from googleapiclient.discovery import build

# Paste your real Google Cloud alphanumeric API key inside the quotes below
YOUTUBE_API_KEY = 'AIzaSyA5HRZAXUob68DIF-cruZfZYqV7RUdzyd0'

# Sample YouTube Video IDs to scrape (You can replace these with your own choice later)
VIDEO_IDS_LIST = ['dQw4w9WgXcQ', 'jNQXAC9IVRw']

try:
    # Set up our secure relational link to MySQL Workbench
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='Rajvardhan@1212',
        database='social_engagement_db',
        port=3306
    )
    cursor = connection.cursor()
    print("Database connection verified successfully.")
    
    # Initialize the Google API client service
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    
    # Step 4: Call the API to fetch video statistics
    request = youtube.videos().list(
        part="snippet,statistics",
        id=",".join(VIDEO_IDS_LIST)
    )
    response = request.execute()
    
    for item in response.get('items', []):
        title = item['snippet']['title']
        tags_list = item['snippet'].get('tags', ['Social Engagement'])
        topic = tags_list[0]  # Grab the first primary hashtag/tag category
        likes = int(item['statistics'].get('likeCount', 0))
        
        # Step 7: Push video properties into the content performance table
        sql_content = """
        INSERT INTO content_performance 
        (title, topic, content_type, video_length_seconds, hook_type, caption_style, shares, saves, likes, retention_rate, posted_at)
        VALUES (%s, %s, 'Video Longform', 0, 'API Fetch', 'Standard Caption', 0, 0, %s, 0.00, %s)
        """
        cursor.execute(sql_content, (title, topic, likes, datetime.now()))
        content_id = cursor.lastrowid # Keep track of this ID for linking comments
        
        # Step 5 & 6: Fetch up to 5 raw public comments from under that video
        comment_request = youtube.commentThreads().list(
            part="snippet",
            videoId=item['id'],
            maxResults=5
        )
        comment_response = comment_request.execute()
        
        for c_item in comment_response.get('items', []):
            raw_comment = c_item['snippet']['topLevelComment']['snippet']['textDisplay']
            
            # Step 7: Save raw comment string linked to parent video ID
            sql_comment = """
            INSERT INTO user_comments (content_id, comment_text)
            VALUES (%s, %s)
            """
            cursor.execute(sql_comment, (content_id, raw_comment))
            
    # Commit changes permanently to MySQL Workbench
    connection.commit()
    print("Success: Live metrics and comments pulled and saved to database tables!")

except Exception as e:
    print(f"Live Pipeline Execution Error: {e}")

finally:
    if 'connection' in locals() and connection.open:
        cursor.close()
        connection.close()
        print("Database session closed cleanly.")
