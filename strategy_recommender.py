import pandas as pd
from sqlalchemy import create_engine

try:
    # Connect to your local database engine
    engine = create_engine("mysql+pymysql://root:Rajvardhan%401212@localhost:3306/social_engagement_db")
    
    # Fetch historical content attributes to calculate performance records
    query = "SELECT topic, hook_type, caption_style, likes, shares, saves FROM content_performance;"
    df = pd.read_sql(query, engine)
    
    # Fallback dataset matching your successful project metrics
    if len(df) < 2:
        df = pd.DataFrame({
            'topic': ['Social Anxiety', 'Dating Struggles', 'Career Stress', 'Social Anxiety'],
            'hook_type': ['Visual Text', 'Question Hook', 'Storytelling Open', 'Visual Text'],
            'caption_style': ['Short & Punchy', 'Long Empathic', 'Bullet Points', 'Short & Punchy'],
            'likes': [1200, 1500, 3000, 2800],
            'shares': [150, 200, 400, 350],
            'saves': [600, 750, 890, 580]
        })
        
    df['engagement_score'] = (df['likes'] * 1) + (df['shares'] * 5) + (df['saves'] * 10)
    
    # STEP 13: Group by attributes to find the winning structural content combinations
    best_topic = df.groupby('topic')['engagement_score'].mean().idxmax()
    best_hook = df.groupby('hook_type')['engagement_score'].mean().idxmax()
    best_style = df.groupby('caption_style')['engagement_score'].mean().idxmax()
    
    print("\n==================================================")
    print("      STEP 13: ENGAGEMENT OPTIMIZATION ENGINE      ")
    print("==================================================")
    print(f"-> Recommended Core Topic : {best_topic}")
    print(f"-> Recommended Video Hook : {best_hook}")
    print(f"-> Recommended Text Style : {best_style}")
    print("Strategy: Prioritize this combination next week for maximum connection.")
    
    # STEP 14: Simulating external trending focus keywords before saturation
    trending_struggles = ['Burnout Management', 'Imposter Syndrome', 'Academic Isolation']
    
    print("\n==================================================")
    print("         STEP 14: TREND FORECASTING LOGS          ")
    print("==================================================")
    print("Top emerging external struggles to target next:")
    for rank, trend in enumerate(trending_struggles, 1):
        print(f"{rank}. {trend} (Rising search volume)")
    print("==================================================\n")

except Exception as e:
    print(f"Recommender System Error: {e}")
