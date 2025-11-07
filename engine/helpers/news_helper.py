# engine/helpers/news_helper.py

# --- COUNTRY CODE MAP ---
# (This map is still useful for converting names to codes)
COUNTRY_MAP = {
    "india": "in",
    "united states": "us",
    "us": "us",
    "usa": "us",
    "united kingdom": "gb",
    "uk": "gb",
    "germany": "de",
    "france": "fr",
    "australia": "au",
    "canada": "ca",
    "china": "cn",
    "japan": "jp",
}

def find_country_code(command):
    # (This function doesn't need to change)
    for country_name, code in COUNTRY_MAP.items():
        if country_name in command:
            return code
    return 'us'

# --- THE MAIN FUNCTION, UPGRADED FOR pygooglenews ---
def get_top_headlines(country='us', count=5):
    """
    Fetches top news headlines using the pygooglenews library.
    """
    try:
        # Import the library here to avoid any potential startup blocking
        from pygooglenews import GoogleNews
        
        # Initialize the client with the country code
        gn = GoogleNews(country=country)
        
        # Get the top news
        top_news = gn.top_news()
        
        # 'top_news' contains a dictionary, we want the 'entries'
        articles = top_news['entries']

        if articles:
            # Get the top 'count' articles
            top_articles = articles[:count]
            
            # Format the headlines into a speakable string
            headlines = [f"Headline {i+1}: {article['title']}" for i, article in enumerate(top_articles)]
            news_report = "According to Google News, here are the top headlines... " + "... ".join(headlines)
            
            return news_report
        else:
            return "Sorry, I couldn't find any articles from Google News."

    except Exception as e:
        print(f"An error occurred with pygooglenews: {e}")
        return "Sorry, an unexpected error occurred while fetching the news."