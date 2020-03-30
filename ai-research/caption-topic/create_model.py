import pandas as pd
import process_text
import gensim

import pickle
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--num-topics", help="Number of topics", type=int, default=5)
args = parser.parse_args()

# Using slightly modified ABC News headlines dataset: https://www.kaggle.com/therohk/million-headlines
headlines = pd.read_csv("headlines.csv")
headlines = headlines["title"]

# Tokenizing and Lemmatization
# For example, convert "australia is locked into war timetable opp" to ["australia", "be", "lock", "into", "war", "timetable", "opp"]
processed_titles = [process_text.lemmatize_sentence(title) for title in headlines]

# Create gensim dictionary and corpus
dictionary = gensim.corpora.Dictionary(processed_titles)
corpus = [dictionary.doc2bow(title) for title in processed_titles]

# Create and save Latent-Dirichlet-Allocation model
model = gensim.models.ldamodel.LdaModel(corpus, num_topics=args.num_topics, id2word=dictionary)

with open("dictionary.sav", "wb") as f:
    pickle.dump(dictionary, f)
with open("model.sav", "wb") as f:
    pickle.dump(model, f)

# Print topics found in corpus
print("Found the following topics in corpus:")
topics = model.print_topics(num_words=10)
for topic_num, topic in topics:
    print(topic)
