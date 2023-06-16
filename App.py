import numpy as np
import pandas as pd
import streamlit as st
import preprocessor,Functions
import matplotlib.pyplot as plt
import seaborn as sns
st.sidebar.title('Whatsapp Chat Analyzer ')

upload_file = st.sidebar.file_uploader('choose a file')

if upload_file is not None:
    byte_data = upload_file.getvalue()
    data = byte_data.decode('utf-8')
    df = preprocessor.preprocess(data)
    user_list = df['users'].unique().tolist()
    user_list.sort()
    user_list.remove('Notification')
    user_list.insert(0 , 'Overall')
    selected = st.sidebar.selectbox("Select User from List",user_list)
    if st.sidebar.button("show Analysis"):
        #stats numOfMessages, numOfWords , numOfMedia, numOfLinks
        num_messages, num_words, num_media, num_links  = Functions.give_stats(df, selected)
        st.title("Chat Stats ")
        col1,col2,col3,col4 = st.columns(4)

        with col1:
            st.header("total Messages")
            st.title(num_messages)
        with col2:
            st.header("total Words")
            st.title(num_words)
        with col3:
            st.header("total Media Files")
            st.title(num_media)
        with col4:
            st.header("total Links")
            st.title(num_links)

        #monthly timeline
        st.title('Monthly Usage')
        timeline = Functions.get_monthly_time(df,selected)
        fig ,ax  = plt.subplots()
        ax.plot(timeline['time'], timeline['messages'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #daily timeline
        st.title('Daily Usage')
        timeline = Functions.get_daily_time(df,selected)
        fig, ax = plt.subplots();
        ax.plot(timeline['date'], timeline['messages'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #activity Maps
        st.title('Activity Maps')
        col1,col2 = st.columns(2)
        with col1:
            st.subheader('Activity Map By Month')
            months = Functions.get_map_by_month(df,selected)
            fig,ax = plt.subplots()
            ax.barh(months.index, months.values)
            st.pyplot(fig)

        with col2:
            st.subheader('Activity Map By Day')
            days = Functions.get_map_by_day(df,selected)
            fig, ax = plt.subplots()
            ax.barh(days.index,days.values)
            st.pyplot(fig)

        st.title('Weekly Activity Map')
        user_activity_map = Functions.get_map_by_week(df,selected)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_activity_map)
        st.pyplot(fig)

        if selected=='Overall':
            st.title('Most Busy Users')
            x,new_df = Functions.most_busy_users(df)
            col1,col2 = st.columns(2)

            with col1:
                fig, ax =plt.subplots()
                ax.barh(x.index,x.values)
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # sentimental Analysis
        st.title("Sentimental Analysis of Messages")
        col1, col2 = st.columns(2)
        sent_df, labels, sent_df2 = Functions.get_sentiments(df, selected)
        with col1:
            fig, ax = plt.subplots()
            ax.pie(sent_df[0], labels=labels, autopct="%0.2f")
            st.pyplot(fig)
        with col2:
            st.dataframe(sent_df2)

        #Emoji analysis
        st.title("Emoji analysis")
        emoji_df,labels = Functions.get_emoji(df,selected)
        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1].head(),labels=labels,autopct="%0.2f")
            st.pyplot(fig)

        #word cloud
        col1,col2 = st.columns(2)
        with col1:
            st.title('Word Cloud of Messages')
            word_c = Functions.get_word_cloud(df,selected)
            fig,ax = plt.subplots()
            ax.imshow(word_c)
            st.pyplot(fig)
        with col2:
            st.title('most common words')
            df_mcw,labels = Functions.get_words(df,selected)
            fig,ax = plt.subplots()
            ax.barh(labels, df_mcw[1])
            st.pyplot(fig)

