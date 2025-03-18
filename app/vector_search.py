import numpy as np
import pandas as pd
import pathlib
import textwrap
from collections import defaultdict
import google.generativeai as genai
from api_keys import Password

books=pd.read_csv('app/data/book_cleaned.csv')
def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

genai.configure(api_key=Password.password)


for m in genai.list_models():
    if 'embedContent' in m.supported_generation_methods: # Shows possible models to use to embedd text
        print(m.name)


model='models/text-embedding-004'


def embedding(model,df): # creates a new column of vector embedding of the column['tagged_description'].
    df['embedding']= df['tagged_description'].apply(make_embedded(model))
    return df

def analyse_text(model,text):
    vector=genai.embed_content(model=model,content=text,task_type='classification')
    return vector

def recommendation(query:str,num_recommendations):
    sol=analyse_text(model,query)
    min,index=float('inf'),0
    options=[[float('inf'),0] for _ in range(num_recommendations)]
    print(options)
    for ind in range(len(vect_df)):


        dist=0
        if books['average_rating'].iloc[ind]< 4:
            continue
        for i,value in enumerate(vect_df.iloc[ind]):
            dist+= (sol['embedding'][i]-value)**2


        dist=np.sqrt(dist)

        if dist>= options[len(options)-1][0]:
            continue
        else:
            i = len(options)-1
            temp=[]

            while i>=0 and options[i][0]> dist:
                temp.append(options[i])
                i-=1
                options.pop()

            options.append([dist,ind])
            for i in range(num_recommendations-len(options)):
                options.append(temp[len(temp)-1-i])




        if dist<min:
            min=dist
            index=ind
    return options
newbooks=pd.read_csv('app/data/newbooks.csv',encoding='utf-8')
vect_df=pd.read_csv('app/data/vectors.csv',header=None)



"""min,index=float('inf'),0
print(type(newbooks['embedding'][0]))
for ind in range(len(vect_df)):


    dist=0
    for i,value in enumerate(vect_df.iloc[ind]):
        dist+= (sol['embedding'][i]-value)**2


    dist=np.sqrt(dist)


    if dist<min:
        min=dist
        index=ind

"""


results= pd.DataFrame(recommendation('Magic school ',10),columns=['distance','index'])
books.iloc[results['index']]