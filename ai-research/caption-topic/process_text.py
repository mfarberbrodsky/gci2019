import nltk
from nltk.corpus import wordnet

nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")

lemmatizer = nltk.stem.WordNetLemmatizer()


def pos_tag_to_lemma_tag(tag):
    mapping = {"J": wordnet.ADJ, "V": wordnet.VERB, "N": wordnet.NOUN, "R": wordnet.ADV}
    return mapping.get(tag[0], wordnet.NOUN)


def lemmatize_sentence(sentence):
    return [lemmatizer.lemmatize(word, pos_tag_to_lemma_tag(tag)) for word, tag in nltk.pos_tag(nltk.word_tokenize(sentence))]
