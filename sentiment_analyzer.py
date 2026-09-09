import pymysql
from textblob import TextBlob

try:
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='Rajvardhan@1212',
        database='social_engagement_db',
        port=3306
    )
    cursor = connection.cursor()
    
    # Fetching comments to run our Step 10 specific analysis
    cursor.execute("SELECT comment_id, comment_text FROM user_comments;")
    comments_records = cursor.fetchall()
    
    for comment_id, text in comments_records:
        analysis = TextBlob(text)
        polarity_score = analysis.sentiment.polarity
        
        # Step 9 Baseline Tags
        if polarity_score > 0.1:
            sentiment_tag = 'Positive'
        elif polarity_score < -0.1:
            sentiment_tag = 'Negative'
        else:
            sentiment_tag = 'Relatable'
            
        # ============================================================
        # STEP 10: LINGUISTIC TRIGGER & PROBLEM AWARENESS EXTRACTION
        # ============================================================
        # 1. Defining target word arrays that reveal viewer pain points
        problem_keywords = [
            'anxiety', 'stress', 'exhausting', 'stuck', 'pressure', 
            'lonely', 'sad', 'scared', 'struggling', 'confused'
        ]
        
        # 2. Convert text to lowercase to ensure matching works perfectly
        clean_text = text.lower()
        
        # 3. Binary evaluation check: flag as 1 if a problem trigger word is found
        problem_flag = 0
        if any(word in clean_text for word in problem_keywords):
            problem_flag = 1
            
        # If the text hits an explicit problem trigger, override to 'Relatable' 
        if problem_flag == 1:
            sentiment_tag = 'Relatable'
        # ============================================================
        
        # Save calculations permanently to your MySQL Workbench
        sql_update = """
        UPDATE user_comments 
        SET sentiment_tag = %s, problem_awareness_flag = %s 
        WHERE comment_id = %s
        """
        cursor.execute(sql_update, (sentiment_tag, problem_flag, comment_id))
        
    connection.commit()
    print("Success: Step 10 Problem Awareness Flags successfully calculated and stored.")

except Exception as e:
    print(f"Step 10 Script Error: {e}")

finally:
    if 'connection' in locals() and connection.open:
        cursor.close()
        connection.close()
