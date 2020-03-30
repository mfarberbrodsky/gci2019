# Topic Modeling

"[AI][Hard] Find out a way to get a current topic based on captions and implement it." task solution created by AlephZero for CCExtractor, Google-Code-In 2019.
## Usage
First, install the necessary requirements:
```shell script
pip3 install -r requirements.txt
```
Then, either create the model using `create_model.py`, or use the provided saved model and dictionary at `model.sav` and `dictionary.sav`.

To find the topic of some caption / text, run
```shell script
python3 get_topic.py "this is some sentence"
```
or
```shell script
python3 get_topic.py "this is some sentence" --model model_path_here --dictionary dictionary_path_here
```
replacing model_path_here with the path of your custom model.

## Research - the model

The data used for this model is a slightly modified version of https://www.kaggle.com/therohk/million-headlines, a dataset of 1,000,000 article headings from ABC news.

The data was preprocessed using lemmatization (each word is converted to its root word, for example running -> run, are -> be, geese -> goose).

After that a Latent-Dirichlet-Allocation (LDA) model was created using that preprocessed corpus.
LDA is run with some number of topics (configurable through the command-line parameter `--num_topics` of `create_model.py`, by default 5 topics in model.sav).
The LDA algorithm then creates topics, based on prominent keywords in the corpus.

## References

I used these articles as reference:

https://towardsdatascience.com/topic-modeling-and-latent-dirichlet-allocation-in-python-9bf156893c24
https://monkeylearn.com/topic-analysis/