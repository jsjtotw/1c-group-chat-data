from whatstk import df_from_txt_whatsapp
import re
import regex
import pandas as pd
import numpy as np
import emoji
import plotly.express as px
from collections import Counter
import matplotlib.pyplot as plt
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
df = df_from_txt_whatsapp("WhatsApp Chat with AHS but it's 1C.txt")
df.username.unique()
df = df.dropna()
total_messages = df.shape[0]
media_messages = df[df['message'] == '<Media omitted>'].shape[0]
media_messages_df = df[df['message'] == '<Media omitted>']
messages_df = df.drop(media_messages_df.index)
def split_count(text):
    emoji_list = []
    data = regex.findall(r'\X', text)
    for word in data:
        if emoji.is_emoji(word):
            emoji_list.append(word)
    return emoji_list
messages_df["emoji"] = messages_df["message"].apply(split_count)
emojis = sum(messages_df['emoji'].str.len())
messages_df["emojicount"] = messages_df['emoji'].str.len()
URLPATTERN = r'(https?://\S+)'
messages_df['urlcount'] = messages_df.message.apply(lambda x: re.findall(URLPATTERN, x)).str.len()
links = np.sum(messages_df.urlcount)
messages_df['Letter_Count'] = messages_df['message'].apply(lambda s: len(s))
messages_df['Word_Count'] = messages_df['message'].apply(lambda s: len(s.split(' ')))
messages_df["Message_Count"] = 1
with open('data.txt', 'w') as file:
    file.write("Group Stats:\n")
    file.write(f"Messages: {total_messages}\n")
    file.write(f"Media: {media_messages}\n")
    file.write(f"Emojis: {emojis}\n")
    file.write(f"Links: {links}\n\n")
    l = messages_df.username.unique()
    for i in range(len(l)):
        req_df = messages_df[messages_df["username"] == l[i]]
        file.write(f"Stats of {l[i]} -\n")
        file.write(f"Messages Sent: {req_df.shape[0]}\n")
        words_per_message = (np.sum(req_df['Word_Count'])) / req_df.shape[0]
        file.write(f"Words per message: {words_per_message}\n")
        media = media_messages_df[media_messages_df['username'] == l[i]].shape[0]
        file.write(f"Media Messages Sent: {media}\n")
        emojis = sum(req_df['emoji'].str.len())
        file.write(f"Emojis Sent: {emojis}\n")
        links = sum(req_df["urlcount"])
        file.write(f"Links Sent: {links}\n")
        file.write("\n")