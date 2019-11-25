import os
import xml.etree.cElementTree as ET
import pandas as pd

itunes_folder = os.path.expanduser('~' + os.sep + 'Music' + os.sep + 'iTunes')
#itunes_folder = r'C:\Users\ckw\Music\iTunes'
songs = []
ArtistName = []
AlbumName = []
songcount = []
songname = []


tree = ET.ElementTree(file=os.path.join(itunes_folder, 'iTunes Music Library.xml'))
root = tree.getroot()

# i = 16

for i , child in enumerate(root[0]):
    if child.text == "Tracks":
        tracks = root[0][i]
        break

for j in range(len(root[0][i+1])): # Loop for every song
    if j % 2 == 1: # for every two element is a song
        column = []
        numele = len(root[0][i+1][j])
        songele = root[0][i+1][j]
        not_include = False
        for a in range(numele):
            if songele[a].text == 'Playlist Only':
                not_include = True
                break
            # elif songele[a].text == 'Matched':
            #     not_include = True
            #     break
            elif songele[a].text == '比對成功的 AAC 音訊檔':
                not_include = True
                break
            elif songele[a].text == 'Has Video':
                not_include = True
                break
            elif songele[a].text == 'Track ID':
                if len(songele[a+1].text) > 4:
                    # print(songele[a+1].text)
                    not_include = True
                    break

        if not_include == False:
            #_____________ Name _____________#
            have_name = False
            for a in range(numele):
                if songele[a].text == 'Name':
                    have_name = True
                    break
            for a in range(numele):
                if songele[a].text == 'Name':
                    songname.append(songele[a+1].text.replace(' (Live)',''))
                    break
            if have_name == False:
                songcount.append('')
            #_____________ Play Count _____________#
            have_count = False
            for a in range(numele):
                if songele[a].text == 'Play Count':
                    have_count = True
                    break
            for a in range(numele):
                if songele[a].text == 'Play Count' and have_count == True:
                    songcount.append(songele[a+1].text)
                    break
            if have_count == False:
                songcount.append('0')
            #_____________ Artist _____________#
            have_Artist = False
            for a in range(numele):
                if songele[a].text == 'Artist':
                    have_Artist = True
                    break
            for a in range(numele):
                if songele[a].text == 'Artist' and have_Artist == True:
                    ArtistName.append(songele[a+1].text)
                    break
            if have_Artist == False:
                ArtistName.append('')
            #_____________ Album _____________#
            have_Album = False
            for a in range(numele):
                if songele[a].text == 'Album':
                    have_Album = True
                    break
            for a in range(numele):
                if songele[a].text == 'Album':
                    AlbumName.append(songele[a+1].text)
                    break
            if have_Album == False:
                AlbumName.append('')

            # if len(column) == 1 and column[0].isdigit() is False:
            #     column.append('0')
            # if len(column) == 2:
            #     songs.append(column)
print (len(ArtistName), len(AlbumName), len(songcount), len(songname))
# total = 0
# for c, song in enumerate(songs):
#     print(c+1, song[0], song[1])
#     total += int(song[1])
# print('total:', total , 'average:', total/(c+1))

#print(songs)

df = pd.DataFrame({'name' : songname, 'artist' : ArtistName, 'album' : AlbumName, 'Play Count' : songcount })
df['Play Count'] = df ['Play Count'].astype(int)

# artist_column = pd.Series(ArtistName)
# album_column = pd.Series(AlbumName)
# df.insert(loc=2, column='artist', value=artist_column)
# df.insert(loc=3, column='album', value=album_column)

grouped=df.groupby(['name','artist']).agg({'Play Count':sum})
res = grouped.sort_values('Play Count', ascending=False)

# with pd.option_context('display.max_rows', 10, 'display.max_columns', None):  # more options can be specified also
#     print(res)
print(res.head(20))

# for loop for all songs = a
# inside a loop do b loop all song
# if match artist and song name after re.replace('live')
# count of b added to a
#
