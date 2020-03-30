import argparse
import grammar_check

parser = argparse.ArgumentParser(description="Text Scoring")
parser.add_argument("--language", help="Language of words, english by default", default="en")
parser.add_argument("--sentence", help="Sentence to score")
args = parser.parse_args()

tool = grammar_check.LanguageTool(args.language)


def get_scores(text):
    """Checks the sentence for errors, and returns two scores: number of errors in the sentence, and the fraction of errors from the sentence based on length"""
    errors = tool.check(text)

    num_errors = len(errors)
    error_fraction = sum(error.errorlength for error in errors) / len(text)
    return num_errors, error_fraction


def print_scores(text):
    num_errors, error_fraction = get_scores(text)
    print("Number of errors: {}\nFraction of errors from the text: {}\nFinal score: {}/100".format(num_errors, error_fraction, int((1 - error_fraction) * 100)))


if args.sentence:
    print_scores(args.sentence)
else:
    sentence = input("Enter a sentence, or 'stop' to end: ")
    while sentence != "stop":
        print_scores(sentence)
        sentence = input("Enter a sentence, or 'stop' to end: ")
