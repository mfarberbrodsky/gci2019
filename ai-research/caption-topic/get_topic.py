import argparse
import pickle
import process_text

parser = argparse.ArgumentParser()
parser.add_argument("text", help="Text to find topic of")
parser.add_argument("--dictionary", help="Custom dictionary path (optional)", default="dictionary.sav")
parser.add_argument("--model", help="Custom model path (optional)", default="model.sav")
args = parser.parse_args()

with open(args.dictionary, "rb") as f:
    dictionary = pickle.load(f)
with open(args.model, "rb") as f:
    model = pickle.load(f)

print("This sentence has the following topics:")
processed_text = dictionary.doc2bow(process_text.lemmatize_sentence(args.text))
topics = model.get_document_topics(processed_text)

for topic, probability in sorted(topics, key=lambda x: -x[1])[:5]:
    print("Topic {} (probability {}):".format(topic, probability))
    print(model.print_topic(topic, 10))
