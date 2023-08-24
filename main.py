import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

'''Load file into DataFrame'''
df = pd.read_csv('../tate.csv')

'''Add an ID to each row'''
df.insert(0, 'itemID', 0)  # Creates new column for IDs

i = 0
for item in df.index:
    df.loc[item, 'itemID'] = i
    i = i + 1

pd.set_option('display.max_columns', 20)

# print(df.info())
# print(df.head(20))

'''Create dataframe of IDs and mediums'''
itemID = []
mediums = []
for row in df.index:
    mediumStr = df["data.medium"][row]
    mediumStr = mediumStr.replace(", and ", ", ")
    mediumStr = mediumStr.replace(" and ", ", ")
    mediumArr = mediumStr.split(", ")

    for medium in mediumArr:
        medium = medium.capitalize()  # Formats medium for readability
        itemID.append(df['itemID'][row])
        mediums.append(medium)

data = {'itemID': itemID, 'mediums': mediums}

dfm = pd.DataFrame(data)

'''Save DataFrame to CSV'''
dfm.to_csv('tate_mediums.csv', index=False)

# print(dfm.info())
# print(dfm.head(20))

# '''Create string of mediums'''
# mediums = ""
# for row in df.index:
#     items = df["data.medium"][row]
#     mediums += items
#     mediums += ", "
#
# '''Split string into array'''
# mediums = mediums.split(", ")
#
# '''Create set of unique mediums'''
# uniqueMediums = set(mediums)
#
# '''Create dictionary of mediums and their counts'''
# mediumCounts = {'medium':[], 'count':[]}
#
# for medium in uniqueMediums:
#     medium = medium.capitalize()  # Formats medium for readability
#     count = mediums.count(medium)  # Counts frequency of each medium
#     mediumCounts['medium'].append(medium)
#     mediumCounts['count'].append(count)
#
# '''Load dictionary into DataFrame'''
# mc = pd.DataFrame(mediumCounts)
# mc.sort_values(by='medium', inplace=True)  # Sorts alphabetically for readability
#
# '''Add an ID to each row'''
# mc.insert(0, 'mediumID', 0)  # Creates new column for IDs
#
# i = 0
# for row in mc.index:
#     mc.loc[row, 'mediumID'] = i
#     i = i + 1
#
# '''Save DataFrame to CSV'''
# mc.to_csv('tate_mediums.csv', index=False)
#
# '''Select top 10 mediums for bar graph'''
# mc.sort_values(by='count', ascending=False, inplace=True)  # Sorts mediums by count
# mc = mc.head(10)  # Selects the top 10 mediums
# mc.sort_values(by='count', ascending=True, inplace=True)  # Sorts mediums in ascending order for plotting
#
# '''Create horizontal bar graph with labels'''
# x = np.array(mc['medium'])
# y = np.array(mc['count'])
#
# bar_container = plt.barh(x, y, color='#1f77b4')
#
# plt.title("Top 10 Mediums")
# plt.xlabel("Pieces")
#
# plt.bar_label(bar_container)  # Adds value labels to bars
#
# plt.show()

'''Artist's age when Tate acquired piece'''
def ageAtAcq():
    df["ageAtAcquisition"] = 0  # Creates new column
    for item in df.index:
        if df.loc[item, "artist.death.year"] == 0 \
                or df.loc[item, "artist.death.year"] >= df.loc[item, "metadata.acquisition date"]:  # Filters out pieces acquired after artist's death
            acquisitionYear = df["metadata.acquisition date"][item]
            birthYear = df["artist.birth.year"][item]
            difference = (acquisitionYear - birthYear)
            df.loc[item, "ageAtAcquisition"] = difference
ageAtAcq()

'''Years after artist's death when Tate acquired piece'''
def yearsAfterDeath():
    df["yearsAfterDeath"] = 0  # Creates new column
    for item in df.index:
        if df.loc[item, "artist.death.year"] != 0 \
                and df.loc[item, "artist.death.year"] < df.loc[item, "metadata.acquisition date"]:  # Filters out living artists and pieces acquired before artist's death
            acquisitionYear = df["metadata.acquisition date"][item]
            deathYear = df["artist.death.year"][item]
            difference = (acquisitionYear - deathYear)
            df.loc[item, "yearsAfterDeath"] = difference
yearsAfterDeath()

'''Source of acquisition'''
def acqSource():
    df["acquisitionSource"] = ""  # Creates new column
    for item in df.index:
        source = df["metadata.credit"][item]
        source = source.split(" ", 1)
        firstWord = str(source[0])  # Keeps first word only for easier categorization
        df.loc[item, "acquisitionSource"] = firstWord
acqSource()

'''Remove periods and spaces from column names'''
for col in df.columns:
    if "." in col:
        txt = col.replace(".", " ")
        txtList = txt.split(" ")
        txtTuple = []
        for txt in txtList:
            txt = str(txt)
            txt = txt.capitalize()  # Capitalizes for readability
            txtTuple.append(txt)
        txtTuple = tuple(txtTuple)
        txt = "".join(txtTuple)
        df.rename(columns={col: txt}, inplace=True)

'''Save DataFrame to CSV'''
df.to_csv('tate.csv', index=False)


# '''test'''
# df = pd.read_csv('tate_new.csv')
#
# print(df.info())
# print(df.head(20))
# pd.set_option('display.max_columns', 20)
# print(df[['ageAtAcquisition', 'MetadataAcquisitionDate', 'ArtistDeathYear', 'yearsAfterDeath', 'acquisitionSource']].head(50))

