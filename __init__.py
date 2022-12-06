from pyresparser import ResumeParser
import os
from docx import Document
import numpy as np
import pandas as pd
import nltk
from nltk.corpus import stopwords
import string
from nltk.corpus import stopwords
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from ftfy import fix_text
from sklearn.neighbors import NearestNeighbors
from resume_parser import resumeparse
import json
from collections.abc import Iterable

# app.run()
# filename = "Resume- Thu Nguyen.docx"
def run_ai(filename):
  stop_words  = set(stopwords.words('english'))

  #get job decription list
  df =pd.read_csv('jobList.csv') 
  df['test']=df['Job_Description'].apply(lambda x: ' '.join([word for word in str(x).split() if len(word)>2 and word not in (stop_words)]))

  #read resume
  # ---------------------------------------------
  # Parse resume:

  #combine skills
  data = resumeparse.read_file(filename)
  datalist = list(data.values())

  skills=[]
  for i in range(3, len(datalist)):
    if isinstance(datalist[i], Iterable):
        for word in datalist[i]:
          skills.append(word)

  #Begin AI
  def ngrams(string, n=3):
      string = fix_text(string) # fix text
      string = string.encode("ascii", errors="ignore").decode() #remove non ascii chars
      string = string.lower()
      chars_to_remove = [")","(",".","|","[","]","{","}","'"]
      rx = '[' + re.escape(''.join(chars_to_remove)) + ']'
      string = re.sub(rx, '', string)
      string = string.replace('&', 'and')
      string = string.replace(',', ' ')
      string = string.replace('-', ' ')
      string = string.title() # normalise case - capital at start of each word
      string = re.sub(' +',' ',string).strip() # get rid of multiple spaces and replace with a single
      string = ' '+ string +' ' # pad names for ngrams...
      string = re.sub(r'[,-./]|\sBD',r'', string)
      ngrams = zip(*[string[i:] for i in range(n)])
      return [''.join(ngram) for ngram in ngrams]


  #convert to 2D dimension
  vectorizer = TfidfVectorizer(min_df=1, analyzer=ngrams, lowercase=False)
  tfidf = vectorizer.fit_transform(skills) #document-term matrix.

  # print(tfidf)

  #base line for skills
  test1 = (df['test'].values.astype('U')) #Tes

  nbrs = NearestNeighbors(n_neighbors=1, n_jobs=-1).fit(tfidf) #plot the skills

    #plot job description 
  def getNearestN(query):
    queryTFIDF_ = vectorizer.transform(query)
    distances, indices = nbrs.kneighbors(queryTFIDF_)
    return distances, indices

  # print("---------------------------")
  distances, indices = getNearestN(test1) #distances: distance between skills and jobs_desc, indices: positions of jobs_desc
  # #round up the matching score
  # test = list(test) 

      
  matches = []

  for i,j in enumerate(indices):
      dist=round(distances[i][0],4)
      temp = [dist]
      matches.append(temp)

  matches = pd.DataFrame(matches, columns=['Match confidence'])
  # matches = pd.DataFrame(indices, columns=['Match confidence'])

  df['match']=matches['Match confidence']

  df1=df.sort_values('match')

  df1 = df1[['match', 'url', 'Position', 'Company', 'Location', 'Job_Description']]
  df1 = df1[0:10]

  finFile = pd.DataFrame(df1)
  res = json.dumps(finFile.to_dict('records'), indent=4)

  with open("top10.json", "w") as outfile:
      outfile.write(res)

  with open('top10.json', 'r') as openfile:
      json_object = json.load(openfile)

  return json_object