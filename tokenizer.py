import argparse
from parse_cedict import parse_dictionary

parser = argparse.ArgumentParser(description="Chinese word tokenizer")
parser.add_argument("text", help="Text to tokenize")
args = parser.parse_args()

dictionary = parse_dictionary()

text = args.text
words = []

current_segment_start = 0
current_segment_end = 1
while current_segment_end < len(text):
    if text[current_segment_start:current_segment_end] in dictionary:
        words.append(text[current_segment_start:current_segment_end])
        current_segment_start = current_segment_end
        current_segment_end = current_segment_start + 1
    else:
        current_segment_end += 1

words.append(text[current_segment_start:current_segment_end])
print("Tokens:", words)
