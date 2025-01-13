import pandas as pd
import requests
import zipfile
import io

data_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00275/Bike-Sharing-Dataset.zip"

# TODO: Extract the 'day.csv' file from the zip archive and load it into the data DataFrame.
zfile = zipfile.ZipFile(data_url)
f = zfile.open('day.csv')
data = pd.read_csv(f)
f.close()
zfile.close()

print(data.shape)