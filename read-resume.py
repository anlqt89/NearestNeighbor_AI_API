#To run this project, you need to have python 3.7+, nltk, docx, and json packages installed
import nltk
import json
from nltk.corpus import stopwords
from docx import Document
import string
import os
import pandas as pd

from resume_parser import resumeparse
data = resumeparse.read_file('Resume- Thu Nguyen.docx')
print(data)
finalRes= {data['designition'], data['skills'], data['designition'],data['designition'],data['designition']}
df = pd.DataFrame(finalRes)
df.to_csv("finRes.csv")
# ---------------------------------------------
# Get stop words set and punctuation set

# stop_words = set(stopwords.words('english'))
# punctuations = string.punctuation
# # ---------------------------------------------
# # Parse resume:
# def getDocxContent(filename):
#     document = Document(filename)
#     fullText = ""
#     for para in document.paragraphs:
#         fullText += para.text + " "

#     return fullText

# resume = getDocxContent("Resume- Thu Nguyen.docx")

# my_resume = nltk.word_tokenize(resume)
# final_resume = []

# for word in my_resume:
#     if word not in stop_words and word not in punctuations:
#         final_resume.append(word)
# # ---------------------------------------------
# print(final_resume)

# df = pd.DataFrame(final_resume)
# df.to_csv("skills.csv")
# # Opening JSON file
# f = open('jobs.json')
  
# # returns JSON object as a dictionary
# data = json.load(f)
  
# # Iterating through the json
# job = []
# final_job_description = []
# json_jobs = data['results']
# for i in range(len(json_jobs)):
#     words = nltk.word_tokenize(json_jobs[i]['description'])
#     for word in words:
#         if word not in stop_words and word not in punctuations and word != "–":
#             job.append(word)
#     final_job_description.append(job)
#     job = []


# # Closing file
# f.close()
# # ---------------------------------------------
# match  = 0
# match_list = []
# word_match =[]
# word_list = []
# for job in final_job_description:
#     for word in my_resume:
#         if word in job:
#             match += 1
#             word_match.append(word)
#     match_list.append(match)
#     word_list.append(word_match)
#     match = 0
#     word_match = []
# x = 0
# for num_match in match_list:
#     print('job ', x , 'has ' , num_match, "matches", word_list[x])
#     x += 1