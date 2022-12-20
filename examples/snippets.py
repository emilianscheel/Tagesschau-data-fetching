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