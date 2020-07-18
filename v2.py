import os
import xml.etree.cElementTree as ET
import pandas as pd

itunes_folder = os.path.expanduser('~' + os.sep + 'Music' + os.sep + 'iTunes')
tree = ET.ElementTree(file=os.path.join(itunes_folder, 'iTunes Music Library.xml'))
root = tree.getroot()

for i , child in enumerate(root[0]):
    if child.text == "Tracks":
        tracks = root[0][i]
        break

songdb = list()

for j in range(len(root[0][i+1])): # Loop for every song
    if j % 2 == 1: # every two is a song
        song_detail = root[0][i+1][j]
        Name_i = int()
        Artist_i = int()
        Album_i = int()
        PlayCount_i = int()
        for field_i, field in enumerate(song_detail):
            if field_i % 2 == 0 and field.text == 'Name':
                Name_i = field_i + 1
            if field_i % 2 == 0 and field.text == 'Artist':
                Artist_i = field_i + 1
            if field_i % 2 == 0 and field.text == 'Album':
                Album_i = field_i + 1
            if field_i % 2 == 0 and field.text == 'Play Count':
                PlayCount_i = field_i + 1
        song = dict()
        normal = True
        if PlayCount_i == 0:
            continue
        for field_i, field in enumerate(song_detail):
            if field_i == Name_i:
                tempsong = str()
                tempsong = field.text
                song['Name'] = tempsong.replace(' (Live)','').replace('(Live)','')
            if field_i == Artist_i:
                song['Artist'] = field.text
            if field_i == Album_i:
                song['Album'] = field.text
            if field_i == PlayCount_i:
                try:
                    testisint = int(field.text)
                except ValueError:
                    normal = False
                except TypeError:
                    pass
                if field.text == None:
                    song['Play Count'] = 0
                else:
                    song['Play Count'] = field.text

        if normal == True and song.get('Play Count') is not None:
            songdb.append(song)    

df = pd.DataFrame(songdb)
df['Play Count'] = df ['Play Count'].astype(int)
grouped=df.groupby(['Name','Artist']).agg({'Play Count':sum})
res = grouped.sort_values('Play Count', ascending=False)
print(res.head(30))

artistgroup = df.groupby('Artist').agg({'Play Count':sum})
artistres = artistgroup.sort_values('Play Count', ascending=False)
print(artistres.head(30))
