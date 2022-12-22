keywords = topics["Ukraine-Krieg"]["keywords"]


def addTopics(row):
    for topic in topics:
        keywords = topics[topic]["keywords"]

        if any(keyword in row.title for keyword in keywords) or any(keyword in row.tags_full for keyword in keywords):
            return topic


df['topic'] = df.apply(addTopics, axis=1)


# groupby day
"""
df = (df.date.dt.floor('d')
       .value_counts()
       .rename_axis('date')
       .reset_index(name='count')
       .sort_values('date'))
"""


# filter when article is between two dates
"""
df_range3 = df[(df["datetime"].between(np.datetime64("2022-07-16 00:00:00"), np.datetime64("2022-10-27 00:00:00")))]
"""

# is equal to
"""
df_range1 = df.loc[(df['date'] >= "2022-07-16") & (df['date'] <= "2022-10-27")]
"""


# use dark theme (automatically)
"""
plt.style.use('dark_background') # or 'default'
"""


# use dark theme (manually)
"""
plt.rcParams.update({'text.color': "white",
                     'axes.labelcolor': "white",
                     "xtick.color": "white",
                     "ytick.color": "white"})


fig, ax = plt.subplots()
fig.set_facecolor('black')
ax.set_facecolor('black')

df.plot(kind="bar", ax=ax)
"""
