from urlextract import URLExtract
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
nltk.downloader.download('vader_lexicon')
import pandas as pd
import emoji
from wordcloud import WordCloud
from collections import Counter
def give_stats(df, selected):
    extract = URLExtract()
    if selected != 'Overall':
        df = df[df['users'] == selected]

    num_messages = df.shape[0]
    words = []
    for message in df['messages']:
        words.extend(message.split(" "))
    num_words = len(words)
    links = []
    for message in df['messages']:
        links.extend(extract.find_urls(message))
    num_links = len(links)

    num_media = df.loc[(df.messages.str.contains('<Media omitted>\n'))].shape[0]

    return num_messages, num_words, num_media, num_links

def get_monthly_time(df,selected):
    if selected!='Overall':
        df = df[df['users']== selected]

    timeline = df.groupby(['year','month_num','month']).count()['messages'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+ "-"+ str(timeline['year'][i]))
    timeline['time'] = time

    return timeline

def get_daily_time(df,selected):
    if selected!='Overall':
        df = df[df['users']== selected]

    timeline = df.groupby(['date']).count()['messages'].reset_index()
    return timeline

def get_map_by_month(df,selected):
    if selected!="Overall":
        df = df[df['users']== selected]

    months = df['month'].value_counts()
    return months

def get_map_by_day(df,selected):
    if selected != "Overall":
        df = df[df['users'] == selected]

    days = df['day'].value_counts()
    return days
def get_map_by_week(df,selected):
    if selected != "Overall":
        df = df[df['users'] == selected]
    user_map = df.pivot_table(index='day',columns='hour', values='messages',aggfunc='count').fillna(0)
    return user_map

def most_busy_users(df):
    df = df[df['users'] != 'Notification']
    x = df['users'].value_counts().head()
    new_df = round(df['users'].value_counts() / df.shape[0]*100,2).reset_index().rename(columns={'index':'name','users':'percent'})
    return x,new_df

def get_emoji(df,selected):
    if selected!='Overall':
        df = df[df['users']== selected]
    emojis = []
    for message in df['messages']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    lables = []
    for em in emoji_df[0].head():
        lables.append(emoji.demojize(em))
    return emoji_df,lables

def get_word_cloud(df,selected):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read().split('\n')
    if selected!='Overall':
        df = df[df['users']==selected]
    df = df[df['users'] != 'group_notification']
    df = df[df['messages'] != '<Media omitted>\n']
    wc = WordCloud(width=500,height=500,background_color='white',min_font_size=10,stopwords=set(stop_words))

    df_wc = wc.generate(df['messages'].str.cat(sep=" "))
    return df_wc

def get_words(df,selected):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    if selected != 'Overall':
        df = df[df['users'] == selected]
    df = df[df['users'] != 'group_notification']
    df = df[df['messages'] != '<Media omitted>\n']
    words = []

    for message in df['messages']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    final_list = []
    for word in words:
        msg=""
        for c in word:
            if c not in emoji.EMOJI_DATA:
                msg+=c
        if len(msg)>1:
            final_list.append(msg)
    mc_df = pd.DataFrame(Counter(final_list).most_common(20))
    labels = []
    for em in mc_df[0]:
         labels.append(em)
    return mc_df,labels

def get_sentiments(df,selected):
    df = df[df['messages'] != '<Media omitted>\n']
    df = df[df['users'] != 'group_notification']
    neutral = 0
    positive = 0
    negative = 0
    if selected != 'Overall':
        df = df[df['users'] == selected]
    sia = SentimentIntensityAnalyzer()
    for message in df['messages']:
        x = sia.polarity_scores(message)["compound"]
        if x > 0:
           positive+=1
        elif x==0:
            neutral+=1
        else:
            negative+=1
    sent_df = pd.DataFrame([positive,negative,neutral])
    sent_df2 = df = pd.DataFrame({'Type':['Positive','Negative','Neutral'], 'Message counts':[positive,negative,neutral]})
    labels = ['Positive','Negative','Neutral']
    return sent_df,labels,sent_df2