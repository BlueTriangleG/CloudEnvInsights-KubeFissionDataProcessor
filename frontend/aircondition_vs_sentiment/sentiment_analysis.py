from textblob import TextBlob

def add_sentiment_column(df):
    df['sentiment'] = df['tokens'].apply(lambda tokens: ' '.join(tokens)).apply(lambda x: TextBlob(x).sentiment.polarity)
    return df
