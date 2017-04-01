import os
from random import shuffle

train_path = "../resource/asnlib/public/aclImdb/train/" # use terminal to ls files under this directory
test_path = "../resource/asnlib/public/imdb_te.csv" # test data for grade evaluation
stopwords_path = "../resource/asnlib/public/aclImdb/stopwords.en.txt" # file containing common stopwords


def imdb_data_preprocess(inpath, outpath="./", name="imdb_tr.csv", mix=False):
  '''Implement this module to extract
  and combine text files under train_path directory into 
    imdb_tr.csv. Each text file in train_path should be stored 
    as a row in imdb_tr.csv. And imdb_tr.csv should have two 
    columns, "text" and label'''

  inpath = os.path.abspath(inpath) + '/'
  outpath = os.path.abspath(outpath) + '/'

  # create out file
  with open(outpath + name, 'w') as f:
    # write header
    f.write("row_number, text, polarity\n")
    # initialize output string
    out = []
    # now read all files. First positive...
    for filename in os.listdir(inpath + "pos"):
      with open(inpath + "pos/" + filename, 'r') as tmp:
        out.append(tmp.read() + ", 1\n")
    # ...then negative
    for filename in os.listdir(inpath + "neg"):
      with open(inpath + "neg/" + filename, 'r') as tmp:
        out.append(tmp.read() + ", 0\n")
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
  with open(stopFile, 'r') as f:
    stopwords = set(f.read())
  # Open files 
  with open(inFile, 'r') as inF, open(outFile, 'w') as outF:
    for line in iter(inF):
      text = ' '.join([word for word in line.split() if word not in stopwords])
      outF.write(text + '\n')
  
if __name__ == "__main__":
  ''' prepare data '''
  imdb_data_preprocess(train_path, './', 'imdb_tr0.csv', True)
  imdb_remove_stopwords('./imdb_tr0.csv', './imdb_tr.csv', stopwords_path)

  '''train a SGD classifier using unigram representation,
    predict sentiments on imdb_te.csv, and write output to
    unigram.output.txt'''
    
  '''train a SGD classifier using bigram representation,
    predict sentiments on imdb_te.csv, and write output to
    unigram.output.txt'''
     
  '''train a SGD classifier using unigram representation
     with tf-idf, predict sentiments on imdb_te.csv, and write 
     output to unigram.output.txt'''
    
  '''train a SGD classifier using bigram representation
     with tf-idf, predict sentiments on imdb_te.csv, and write 
     output to unigram.output.txt'''
  pass