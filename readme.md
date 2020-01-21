# Text Scoring
Grammatical scoring model created by AlephZero for CCExtractor, Google Code-In 2019.  
Uses the [grammar-check](https://github.com/viraja1/grammar-check) library.

## Usage
Run directly from command-line using `python score.py`:
```
Enter a sentence, or 'stop' to end: This are bad.
Number of errors: 1
Fraction of errors from the text: 0.3076923076923077
Final score: 69/100
Enter a sentence, or 'stop' to end: This is bad.
Number of errors: 0
Fraction of errors from the text: 0.0
Final score: 100/100
Enter a sentence, or 'stop' to end: 
```

Use a different language using the parameter `--language`, for example `--language ru` for Russian.