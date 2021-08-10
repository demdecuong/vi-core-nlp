import pickle
import re

from nltk import ngrams
from datetime import datetime

def read(path):
    data = []
    with open(path, "r") as f:
        for line in f:
            data.append(line.replace('\n',''))
    return data

def save(data,path):
    textfile = open(path, "w")
    for element in data:
        textfile.write(element + "\n")


def read_dict(path):
    with open(path,'rb') as file:
        data = pickle.load(file)
    return data
    
def save_dict(data,path):
    with open(path, 'wb') as file:
        pickle.dump(data, file)

def get_ngram(sentence, n = 1):
    # sentence = tokenize(sentence)
    return ngrams(sentence.split(' '), n)

def tokenize(sentence):
    sent = sentence.replace('\n','').strip()
    sent = re.sub('(?<! )(?=[.,!?()])|(?<=[.,!?()])(?! )', r' ', sent)
    return sent


def padding_punct(s):
    s = s.replace('\n', '').strip()
    s = re.sub('([.,!?()]),"")', r' \1 ', s)
    s = re.sub('\s{2,}', ' ', s)
    return s

def convert_date_to_timestamp(date):
    '''
        date : [(thứ, dd,mm,yyyy)]
    '''
    _, day, month, year = date[0]
    if day == None:
        day = 1
    if month == None:
        month = datetime.now().month
    if year == None:
        year = datetime.now().year
    return datetime(
        year = year,
        month = month,
        day = day
    ).timestamp()

def convert_time_to_timestamp(time):
    '''
        time : (hh,mm)
    '''
    hour, minute = time
    now = datetime.now()
    
    if hour == None:
        hour = now.hour
    if minute == None:
        minute = now.minute
    return datetime(
        year = now.year,
        month = now.month,
        day = now.day,
        hour = hour,
        minute=minute
    ).timestamp()