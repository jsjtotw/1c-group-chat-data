from whatstk import df_from_txt_whatsapp
import re
import regex
import pandas as pd
import numpy as np
import emoji
import plotly.express as px
from collections import Counter
import matplotlib.pyplot as plt
import plotly.io as pio
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
text = " ".join(review for review in messages_df.message)
with open('data.txt', 'w', encoding='utf-8') as file:
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
total_emojis_list = list(set([a for b in messages_df.emoji for a in b]))
total_emojis = len(total_emojis_list)
total_emojis_list = list([a for b in messages_df.emoji for a in b])
emoji_dict = dict(Counter(total_emojis_list))
emoji_dict = sorted(emoji_dict.items(), key=lambda x: x[1], reverse=True)
emoji_df = pd.DataFrame(emoji_dict, columns=['emoji', 'count'])
emoji_df.to_csv('data_emoji.txt', index=False)
fig = px.pie(emoji_df, values='count', names='emoji')
fig.update_traces(textposition='inside', textinfo='percent+label')
fig.write_image("emoji_dis_img/emoji_distribution.png")
l = messages_df.username.unique()
for i in range(len(l)):
    dummy_df = messages_df[messages_df['username'] == l[i]]
    total_emojis_list = list([a for b in dummy_df.emoji for a in b])
    emoji_dict = dict(Counter(total_emojis_list))
    emoji_dict = sorted(emoji_dict.items(), key=lambda x: x[1], reverse=True)
    author_emoji_df = pd.DataFrame(emoji_dict, columns=['emoji', 'count'])
    fig = px.pie(author_emoji_df, values='count', names='emoji')
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.write_image(f"emoji_dis_img/emoji_distribution_{l[i]}.png")
def f(i):
    l = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return l[i]
day_df = pd.DataFrame(messages_df["message"])
day_df['day_of_date'] = messages_df['date'].dt.weekday
day_df['day_of_date'] = day_df["day_of_date"].apply(f)
day_df["messagecount"] = 1
day = day_df.groupby("day_of_date").sum()
day.reset_index(inplace=True)
fig = px.line_polar(day, r='messagecount', theta='day_of_date', line_close=True)
fig.update_traces(fill='toself')
fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
        )
    ),
    showlegend=False
)
pio.write_image(fig, 'polar_plot.png')
date_df = messages_df.groupby("date").sum()
date_df.reset_index(inplace=True)
fig = px.line(date_df, x="date", y="Message_Count")
fig.update_xaxes(nticks=20)
fig.write_image("figure1.png")
date_df["rolling"] = date_df["Message_Count"].rolling(30).mean()
fig = px.line(date_df, x="date", y="rolling")
fig.update_xaxes(nticks=20)
fig.write_image("figure2.png")
auth = messages_df.groupby("username").sum()
auth.reset_index(inplace=True)
fig = px.bar(auth, y="username", x="Message_Count", orientation="h",
             title="Messages sent per user"
            )
fig.write_image("figure3.png")
messages_df['Time'] = messages_df['date'].dt.time
messages_df['Time'].value_counts().head(10).plot.barh()
plt.xlabel('Number of messages')
plt.ylabel('Time')
plt.savefig('top_10_times.png')
messages_df['date'].value_counts().head(10).plot.barh()
plt.xlabel('Number of Messages')
plt.ylabel('date')
plt.savefig('message_counts.png')
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
stopwords = set(STOPWORDS)
stopwords.update(["ra", "ga", "na", "ani", "em", "ki", "ah", "ha", "la", "eh", "ne", "le", "ni", "lo", "Ma", "Haa", "ni"])
wordcloud = WordCloud(stopwords=stopwords, background_color="white").generate(text)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.savefig('wordcloud.png')