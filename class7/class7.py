import pandas as pd
import matplotlib.pyplot as plt
import re

data = {"ID":range(100),"Score":[10]*2+[20]*3+[30]*5+[50]*15+[60]*20+[70]*25+[80]*15 +[90]*8 +[100,100,5,5,0,0,5000]}

df = pd.DataFrame(data)
print(df)

print(df.shape)
print(df.dtypes)
print(df.describe())

df['Score'].plot.hist(bins=300, edgecolor='black')
plt.show()

#Without the last score of 5000. 
df['Score'][:-1].plot.hist(bins=300, edgecolor='black')
plt.show()

q1 = df["Score"].quantile(0.25)
q3 = df["Score"].quantile(0.75)
iqr = q3 - q1

# Use the equation above to replace None
lower = None
upper = None

print(lower)
print(upper)

df_score_cleaned = df[(df["Score"] >= lower) & (df["Score"] <= upper)]

mean = df["Score"].mean()
std = df["Score"].std()

# Use the equation above to replace None
z_scores = (df['Score'] - mean) / std

print(z_scores)

iqr_threshold = 1.5
zscore_threshold = 3

data = {"ID":range(4),"Message":["Now Here  "," now here ", "  NOW HERE", "Now   here"]}
df = pd.DataFrame(data)
print(df)

# Strip Whitespace
df["Message"] = df["Message"].str.strip()
print(df)
# Convert to Lowercase
df["Message"] = df["Message"].str.lower() 
print(df)

# removing repeated whitespace between words?
print(df["Message"].str.replace(' ',''))

#Difference between "" vs r""
print("a\nb") #a    b
print(r"a\tb") # a\tb

#One or more consecutive whitespace characters
pattern = r"\s+"

#One or more consecutive non-whitespace characters
pattern = r"\S+"

re.sub(r"\s+", " ", "Hi     there") 
re.findall(r"\S+", "Hi there") 


import re

def clean_text(text):
    text = text.strip()
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text

df["Message"] = df["Message"].apply(clean_text)

links = ["Visit https://example.com for more info", "My link: www.github.com/mylink/", "Visit http://www.google.com/search"]
data = pd.Series(links)

print(data)

def replace_url(text):
    text = re.sub(r"https?://\S+|www\.\S+", "URL", text)
    return text
# Remove URLs
data = data.apply(replace_url)
print(data)