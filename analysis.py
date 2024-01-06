import pandas as pd
import requests
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
import re


POSITIVE_SCORE = []
NEGATIVE_SCORE = []
POLARITY_SCORE = []
SUBJECTIVITY_SCORE = []
AVERAGE_SENTENCE_LENGTH = []
PERCENTAGE_OF_COMPLEX_WORDS =[]
FOG_INDEX = []
AVG_NUMBER_OF_WORDS_PER_SENTENCE = []
COMPLEX_WORD_COUNT = []
WORD_COUNT = []
SYLLABLE_PER_WORD = []
PERSONAL_PRONOUNS = []
AVG_WORD_LENGTH = []

masterdict = []

# Performing Textual Analysis of Text
print("Performing Textual Analysis of link")
file_name = "Input_text.txt"
with open(file_name,"r",encoding='utf-8') as f:
    ti = f.read()
    tokenized_word = word_tokenize(ti)
    text = ti.split()

    # To format the sentence if there are words like "ain't", "can't" as nltk.tokenize cannot split it as the word itself, it splits it as ["ain","'","t"]. Clean separation of words and punctuations to prevent problems while removing Stopwords.
    def func(text): 
        alltext = []
        punc = ['.','?','!',',','"',"'",'(',')','[',']','{','}',';',':','“','”','’']
        word = ""
        for w in text:
            x = w[len(w)-1]
            x1 = w[0]
            x2 = w[len(w)-2]
            if (x2 == "'" or x2 == '’') and (x == 's'):
                for j in range(len(w)-2):
                    word = word+w[j]
                alltext.append(word)
                alltext.append(w[len(w)-2])
                alltext.append(w[len(w)-1])
            elif x in punc and x1 in punc and x2 in punc:
                alltext.append(w[0])
                for j in range(1,len(w)-2):
                    word = word+w[j]
                alltext.append(word)
                alltext.append(w[len(w)-2])
                alltext.append(w[len(w)-1])
            elif x2 in punc and x in punc:
                for j in range(len(w)-2):
                    word = word+w[j]
                alltext.append(word)
                alltext.append(w[len(w)-2])
                alltext.append(w[len(w)-1])
            elif x in punc and x1 in punc:
                alltext.append(w[0])
                for j in range(1,len(w)-1):
                    word = word+w[j]
                alltext.append(word)
                alltext.append(w[len(w)-1])
            elif x in punc:
                for j in range(len(w)-1):
                    word = word+w[j]
                alltext.append(word)
                alltext.append(w[len(w)-1])
            elif x1 in punc:
                for j in range(1,len(w)):
                    word = word+w[j]
                alltext.append(w[0])
                alltext.append(word)
            else:
                alltext.append(w)
            word = ""
        return alltext
        

    alltext = func(text)

    # Putting together all Stopwords
    Stopwords = ""
    with open("StopWords/StopWords_Auditor.txt", "r") as f:
        StopWords = f.read().upper()
    with open("StopWords/StopWords_Currencies.txt", "r") as f:
        StopWords = StopWords +" "+ f.read().upper()
    with open("StopWords/StopWords_DatesandNumbers.txt", "r") as f:
        StopWords = StopWords +" "+ f.read().upper()
    with open("StopWords/StopWords_Generic.txt", "r") as f:
        StopWords = StopWords +" "+ f.read().upper()
    with open("StopWords/StopWords_GenericLong.txt", "r") as f:
        StopWords = StopWords +" "+ f.read().upper()
    with open("StopWords/StopWords_Geographic.txt", "r") as f:
        StopWords = StopWords +" "+ f.read().upper()
    with open("StopWords/StopWords_Names.txt", "r") as f:
        StopWords = StopWords +" "+ f.read().upper()
    AllStopWords = word_tokenize(StopWords)


    # Removal of All Stopwords
    punc = ['.','?','!',',','"',"'",'(',')','[',']','{','}',';',':','“','”','’']
    filtered_sent = []
    text = ""
    for w in alltext:
        if w not in punc:
            if w.upper() not in AllStopWords:
                text = text +" "+ w
        else:
            text = text +" "+ w
    filtered_sent = word_tokenize(text)


    # Finding out the Positive Score, splitting words using nltk tokenizer as mentioned on docx
    pos_score = 0
    tokenized_pos_w = []
    with open("MasterDictionary/positive-words.txt", "r") as f:
        pos_w = f.read().upper()
        tokenized_pos_w = word_tokenize(pos_w)

    for w in filtered_sent:
        if w.upper() in tokenized_pos_w:
            pos_score += 1
            # Creating a MasterDictionary with all positive and negative words and such that the words are not in stopwords list as mentioned on docx
            if w not in masterdict:
                masterdict.append(w)
    POSITIVE_SCORE.append(pos_score)

    # Finding out the Negative Score, splitting words using nltk tokenizer as mentioned on docx
    neg_score = 0
    tokenized_neg_w = []
    with open("MasterDictionary/negative-words.txt", "r") as f:
        neg_w = f.read().upper()
        tokenized_neg_w = word_tokenize(neg_w)

    for w in filtered_sent:
        if w.upper() in tokenized_neg_w:
            neg_score += 1
            # Creating a MasterDictionary with all positive and negative words and such that the words are not in stopwords list as mentioned on docx
            if w not in masterdict:
                masterdict.append(w)
    NEGATIVE_SCORE.append(neg_score)

    # Finding out the Polarity Score
    polarity_score = (pos_score - neg_score)/( (pos_score + neg_score) + 0.000001)
    POLARITY_SCORE.append(polarity_score)

    # Finding out the Subjectivity Score
    subjectivity_score = (pos_score + neg_score)/((len(filtered_sent))+0.000001)
    SUBJECTIVITY_SCORE.append(subjectivity_score)



    # Finding out the Average Sentence Length
    sentence_count = len(sent_tokenize(ti))
    number_words = ti.split()
    avg_sent_length = len(number_words)/sentence_count
    AVERAGE_SENTENCE_LENGTH.append(avg_sent_length)

    # Finding out the Percentage of Complex Words and Fog Index
    vowels = ['a','e','i','o','u']
    complex_words = []
    vc = 0
    for w in alltext:
        for i in range(len(w)):
            if (w[i] in vowels):
                vc += 1
        if vc>2:
            complex_words.append(w)
        vc = 0
    pct_com_words = len(complex_words)/sentence_count
    PERCENTAGE_OF_COMPLEX_WORDS.append(pct_com_words)
    FOG_INDEX.append(0.4*(avg_sent_length+pct_com_words))

    # Finding out the Average Number of Words per Sentence
    AVG_NUMBER_OF_WORDS_PER_SENTENCE.append(avg_sent_length)

    # Finding out the Complex Word Count
    COMPLEX_WORD_COUNT.append(len(complex_words))


    # Finding out the Word Count after removing stopwords and punctuations as mentioned on docx
    punc = ['.','?','!',',','"',"'",'(',')','[',']','{','}',';',':','“','”','’']
    word_count = []
    text1 = text.split()
    for w in text1:
        if w not in punc:
            word_count.append(w)
    WORD_COUNT.append(len(word_count))


    # Finding out Syllable per Word with special care taken with words ending with "es" and "ed" as mentioned on docx
    vowels = ['a','e','i','o','u']
    syllables = 0
    vc = 0
    for w in alltext:
        for i in range(len(w)):
            if (w[i] in vowels):
                vc += 1
        syllables = vc
        if len(w) >= 2:
            temp1 = w[len(w)-1]
            temp2 = w[len(w)-2]
            temp = temp2+temp1
            if temp == "es" or temp == "ed":
                syllables = vc - 1
    SYLLABLE_PER_WORD.append(syllables/len(number_words))


    # Finding out Personal Pronouns with special care taken to exclude the country "US" as mentioned on docx
    pp_I = re.findall("I",ti)
    pp_we = re.findall("we",ti.lower())
    pp_my = re.findall("my",ti.lower())
    pp_ours = re.findall("ours",ti.lower())
    pp_us = re.findall("us",ti)
    PERSONAL_PRONOUNS.append((len(pp_I)+len(pp_my)+len(pp_we)+len(pp_ours)+len(pp_us)))


    # Finding out the Average Word Length
    punc = ['.','?','!',',','"',"'",'(',')','[',']','{','}',';',':','“','”','’']
    c = 0
    total_words = 0
    Total_words = []
    for w in number_words:
        if w not in punc:
            Total_words.append(w)
            for i in range(len(w)):
                c += 1
    AVG_WORD_LENGTH.append(c/len(number_words))

# Creating a MasterDictionary with all positive and negative words and such that the words are not in stopwords list as mentioned on docx
allmasterdict =""
for i in range(len(masterdict)):
    allmasterdict = allmasterdict + masterdict[i]+"\n"

with open("MasterDictionary/masterdictionary.txt","w",encoding='utf-8') as f:
    f.write(allmasterdict)


# Creating a New Dataframe
dfnew = pd.DataFrame() 
  
# Creating into columns 
dfnew['POSITIVE SCORE'] = POSITIVE_SCORE
dfnew['NEGATIVE SCORE'] = NEGATIVE_SCORE
dfnew['POLARITY SCORE'] = POLARITY_SCORE
dfnew['SUBJECTIVITY SCORE'] = SUBJECTIVITY_SCORE
dfnew['AVG SENTENCE LENGTH'] = AVERAGE_SENTENCE_LENGTH
dfnew['PERCENTAGE OF COMPLEX WORDS'] = PERCENTAGE_OF_COMPLEX_WORDS
dfnew['FOG INDEX'] = FOG_INDEX
dfnew['AVERAGE NUMBER OF WORDS PER SENTENCE'] = AVG_NUMBER_OF_WORDS_PER_SENTENCE
dfnew['COMPLEX WORD COUNT'] = COMPLEX_WORD_COUNT
dfnew['WORD COUNT'] = WORD_COUNT
dfnew['SYLLABLE PER WORD'] = SYLLABLE_PER_WORD
dfnew['PERSONAL PRONOUNS'] = PERSONAL_PRONOUNS
dfnew['AVG WORD LENGTH'] = AVG_WORD_LENGTH
  
# Converting to excel 
dfnew.to_excel('Output Data Structure.xlsx', index = False)