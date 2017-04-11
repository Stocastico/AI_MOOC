import os
from random import shuffle
import pandas as pd
import string
from sklearn.linear_model import SGDClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

train_path = "../resource/asnlib/public/aclImdb/train/" # use terminal to ls files under this directory
test_path = "../resource/asnlib/public/imdb_te.csv" # test data for grade evaluation
stopwords_path = "../resource/asnlib/public/aclImdb/stopwords.en.txt" # file containing common stopwords
stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself',
             'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself',
             'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that',
             'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
             'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as',
             'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through',
             'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off',
             'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how',
             'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only',
             'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 'd',
             'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', 'couldn', 'didn', 'doesn', 'hadn', 'hasn', 'haven',
             'isn', 'ma', 'mightn', 'mustn', 'needn', 'shan', 'shouldn', 'wasn', 'weren', 'won', 'wouldn']

def imdb_data_preprocess(inpath, outpath="./", name="imdb_tr.csv", mix=False):
  '''Implement this module to extract
  and combine text files under train_path directory into 
    imdb_tr.csv. Each text file in train_path should be stored 
    as a row in imdb_tr.csv. And imdb_tr.csv should have two 
    columns, "text" and label'''

  inpath = os.path.abspath(inpath) 
  outpath = os.path.abspath(outpath)

  # create out file
  with open(os.path.join(outpath,name), 'w', encoding='utf8') as f:
    # write header
    f.write("row_number,text,polarity\n")
    # initialize output string
    out = []
    # This uses the 3-argument version of str.maketrans
    # with arguments (x, y, z) where 'x' and 'y'
    # must be equal-length strings and characters in 'x'
    # are replaced by characters in 'y'. 'z'
    # is a string (string.punctuation here)
    # where each character in the string is mapped
    # to None
    s = ''
    translator = s.maketrans('', '', string.punctuation)
    # now read all files. First positive...
    for filename in os.listdir(os.path.join(inpath, "pos")):
      with open(os.path.join(inpath, "pos", filename), 'r', encoding='utf8') as tmp:
        s = tmp.read().translate(translator)
        out.append(s + ", 1")
    # ...then negative
    for filename in os.listdir(os.path.join(inpath, "neg")):
      with open(os.path.join(inpath, "neg", filename), 'r', encoding='utf8') as tmp:
        s = tmp.read().translate(translator)
        out.append(s + ", 0")
    if mix: # shuffle
      shuffle(out)
    # and finally write to file, adding row numbers
    row = 0
    for line in out:
      f.write(str(row) + ", " + line + '\n')
      row += 1
  

def imdb_remove_stopwords(inFile, outFile, stopFile):
  ''' Remove all stopwords from file inFile and write the filtered file to
  outFile'''
  # Read all stopwords
  #with open(stopFile, 'r', encoding='utf8') as f:
  #  stopwords = set(f.read().splitlines())
  # Open files 
  with open(inFile, 'r', encoding='utf8') as inF, open(outFile, 'w', encoding='utf8') as outF:
    #header = inF.readline()
    #outF.write(header + '\n')
    for line in iter(inF):
      text = ' '.join([word for word in line.split() if word not in stopwords])
      outF.write(text + '\n')

def file_to_bigram(inFile):
    ''' Read a csv file and create a unigram model out of it '''
    # Read Input file
    df = pd.read_csv(inFile, header = 0)
    text = df['text'].tolist()
    # Create bigrams 
    bigrams = zip(text, text[1:])
    return X

def unigram_classifier(text, y, test_text):
    ''' create a unigram classifier using SGD. Text is our training data, polarity
        contain the target values. From the input file we will create a 
        document-term matrix '''
    # Create unigram DTM 
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(text)
    # Create and train classifier
    clf = SGDClassifier(loss = 'hinge', penalty = 'l1')
    clf.fit(X, y)
    # Now prepare test data
    X_test = vectorizer.transform(test_text)
    # Perform prediction
    predictions = clf.predict(X_test)
    return predictions

def bigram_classifier(text, y, test_text):
    ''' create a bigram classifier using SGD. Text is our training data, polarity
        contain the target values. From the input file we will create a 
        document-term matrix '''
    # Create unigram DTM 
    bigram_vectorizer = CountVectorizer(ngram_range=(1,2), 
                                        token_pattern=r'\b\w+\b', min_df=1)
    X = bigram_vectorizer.fit_transform(text)
    # Create and train classifier
    clf = SGDClassifier(loss = 'hinge', penalty = 'l1')
    clf.fit(X, y)
    # Now prepare test data
    X_test = bigram_vectorizer.transform(test_text)
    # Perform prediction
    predictions = clf.predict(X_test)
    return predictions

def unigram_tfidf_classifier(text, y, test_text):
    ''' create a unigram tf-idf classifier using SGD. Text is our training data, polarity
        contain the target values. From the input file we will create a 
        document-term matrix '''
    # Create unigram DTM 
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(text)
    # Create and train classifier
    clf = SGDClassifier(loss = 'hinge', penalty = 'l1')
    clf.fit(X, y)
    # Now prepare test data
    X_test = vectorizer.transform(test_text)
    # Perform prediction
    predictions = clf.predict(X_test)
    return predictions

def bigram_tfidf_classifier(text, y, test_text):
    ''' create a bigram classifier using SGD. Text is our training data, polarity
        contain the target values. From the input file we will create a 
        document-term matrix '''

    # Create unigram DTM 
    bigram_vectorizer = TfidfVectorizer(ngram_range=(1,2), 
                                        token_pattern=r'\b\w+\b', min_df=1)
    X = bigram_vectorizer.fit_transform(text)
    # Create and train classifier
    clf = SGDClassifier(loss = 'hinge', penalty = 'l1')
    clf.fit(X, y)
    # Now prepare test data
    X_test = bigram_vectorizer.transform(test_text)
    # Perform prediction
    predictions = clf.predict(X_test)
    return predictions

def write_output(outputFile, values):
    ''' Write some values to an output file. one value per line'''
    with open(outputFile, 'w', encoding='utf8') as outF:
        for v in values:
            outF.write(str(v) + '\n')
  
if __name__ == "__main__":
    ''' prepare data '''
    if not os.path.isfile('./imdb_tr.csv'):
        imdb_data_preprocess(train_path, './', 'imdb_tr0.csv', True)
        imdb_remove_stopwords('./imdb_tr0.csv', './imdb_tr.csv', stopwords_path)

    ''' extract data from csv '''
    df = pd.read_csv('./imdb_tr.csv', header = 0, encoding='latin-1')
    y = df['polarity'].values
    train_text = df['text'].values
    dfTest = pd.read_csv(test_path, header = 0, encoding='latin-1')
    test_text = dfTest['text'].values

    '''train a SGD classifier using unigram representation,
    predict sentiments on imdb_te.csv, and write output to
    unigram.output.txt'''
    prediction = unigram_classifier(train_text, y, test_text)
    write_output('unigram.output.txt', prediction)
    
    '''train a SGD classifier using bigram representation,
    predict sentiments on imdb_te.csv, and write output to
    unigram.output.txt'''
    prediction2 = bigram_classifier(train_text, y, test_text)
    write_output('bigram.output.txt', prediction2)
     
    '''train a SGD classifier using unigram representation
    with tf-idf, predict sentiments on imdb_te.csv, and write 
    output to unigram.output.txt'''
    prediction3 = unigram_tfidf_classifier(train_text, y, test_text)
    write_output('unigramtfidf.output.txt', prediction3)
    
    '''train a SGD classifier using bigram representation
    with tf-idf, predict sentiments on imdb_te.csv, and write 
    output to unigram.output.txt'''
    prediction4 = bigram_tfidf_classifier(train_text, y, test_text)
    write_output('bigramtfidf.output.txt', prediction4)