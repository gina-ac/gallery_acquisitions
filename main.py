import pandas as pd

"""
This code prepares the original CSV file 
(https://corgis-edu.github.io/corgis/csv/tate/) 
for visualization in Tableau.
"""

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

'''Artist's age when Tate acquired artwork'''
def ageAtAcq():
    df["ageAtAcquisition"] = 0  # Creates new column
    for item in df.index:
        if df.loc[item, "artist.death.year"] == 0 \
                or df.loc[item, "artist.death.year"] >= df.loc[item, "metadata.acquisition date"]:  # Filters out artworks acquired after artist's death
            acquisitionYear = df["metadata.acquisition date"][item]
            birthYear = df["artist.birth.year"][item]
            difference = (acquisitionYear - birthYear)
            df.loc[item, "ageAtAcquisition"] = difference
ageAtAcq()

'''Years to Tate's post-humous acquisition of artwork'''
def yearsAfterDeath():
    df["yearsAfterDeath"] = 0  # Creates new column
    for item in df.index:
        if df.loc[item, "artist.death.year"] != 0 \
                and df.loc[item, "artist.death.year"] < df.loc[item, "metadata.acquisition date"]:  # Filters out living artists and artworks acquired before artist's death
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

