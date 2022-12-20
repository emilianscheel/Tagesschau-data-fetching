# Themengebiete verwenden

```py
# Datenbank der Stichwörter der Themengebiete importieren
topics = json.loads(open("topics/topics.json", "r").read())
```

```py
# Erstellt eine neue Spalte „topic“ mit dem zugehörigen Themengebiet
for topic in topics:
    df.loc[(df.title.str.contains('|'.join(topics[topic]['keywords'])) | df.tags_full.str.contains('|'.join(topics[topic]['keywords']))), 'topic'] = topic
```
