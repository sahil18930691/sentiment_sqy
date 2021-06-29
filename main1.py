import joblib
import re
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from flask import Flask, request
import json
import gunicorn

app = Flask(__name__)

'''
def print_plot(index):
    example = df[df.index == index][['Comments', 'sentiment']].values[0]
    if len(example) > 0:
        print(example[0])  
        print('Comments:', example[1])
print_plot(25)
print_plot(9993)
'''

REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;.#]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_.]')
#STOPWORDS = set(stopwords.words('english'))

def clean_text(text):
    """
        text: a string
        
        return: modified initial string
    """
    text = BeautifulSoup(text, "lxml").text # HTML decoding
    text = text.lower() # lowercase text
    text = REPLACE_BY_SPACE_RE.sub(' ', text) # replace REPLACE_BY_SPACE_RE symbols by space in text
    text = BAD_SYMBOLS_RE.sub('', text)# delete symbols which are in BAD_SYMBOLS_RE from text
    #text = ' '.join(word for word in text.split() if word not in STOPWORDS) # delete stopwors from text
    return text


loaded_model = joblib.load("model_10k_data.sav")


'''
df1 = pd.read_csv('test24feb.csv')
#df1['sentiment'] = df1.apply(lambda _: '', axis=1)
#print(df1)
#df1 = df1[df.columns]
df1 = df1.drop("sentiment",axis = 1)
#df1 = df1.fillna("")
df1 = df1.replace(['^\s+$'], np.nan, regex = True)
df1 = df1.dropna()
#print(df1['Comments'])

#df1.to_csv('check_blanks.csv')
#print(df1['Comments'])

#df1 = df1.dropna()
#df1 = df1.dropna(how='any', inplace=True)


df1['Comments'] = df1['Comments'].apply(clean_text)


#df1[~df1.Comments.str.contains(".")]
#print(df1)

df12 = df1['Comments']

loaded_model = joblib.load("model_10k_data.sav")


y_pred = loaded_model.predict(df12)
#print(y_pred)
df1['sentiment'] = y_pred 
df1 = df1.replace(['^\s+$'], np.nan, regex = True)
df1 = df1.dropna()
#c = df1.loc[text_empty].index
#print(df1['Comments'])
df1['sentiment1']=df1["sentiment"]
df1["sentiment1"].replace({"positive": "1", "negative": "2","other": "3", "neutral": "4"}, inplace=True)
#df1.to_csv('result_28_July_2021.csv')
print(df1.head())

'''
@app.route('/leadactivitysentiment', methods=['POST'])


def leadactivitysentiment():
    try:
        json_ = request.json
        test = pd.DataFrame(json_)
        test = test.drop("sentiment",axis = 1)
        test = test.replace(['^\s+$'], np.nan, regex = True)
        test = test.dropna()
        test['Comments'] = test['Comments'].apply(clean_text)
        df12 = test['Comments']
        y_pred = loaded_model.predict(df12)
        test['sentiment'] = y_pred 
        test = test.replace(['^\s+$'], np.nan, regex = True)
        test = test.dropna()
        test['sentiment1']=test["sentiment"]
        test["sentiment1"].replace({"positive": "1", "negative": "2","other": "3", "neutral": "4"}, inplace=True)
        test = test[['RecNo','Comments','sentiment','sentiment1']]
        orient="records"
        result = test.to_json(orient = orient)
        return(result)
        
        
    except:
        return('Error')    


if __name__ == '__main__':
    try:
        port = int(sys.argv[1]) 
    except:
        port = 3000

app.run(port=port, debug=True)  
