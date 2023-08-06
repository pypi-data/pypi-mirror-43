# essay_scorer

An automated essay scorer for english language learner essays.

## Description

Extracts a set of linguistic features and compares them to a model trained on over 3000 essays to predict the score on a 40 point scale. 

## Installation

`pip install essay-scorer`

## Usage/Tutorial

### Command line usage

Accepts either a directory of `.txt` files or a single `.txt` file.

(You'll have to locate the bin where the script is saved by pip to use the command line like this.)

**For a directory of text files**
`python3 essay_scorer.py path/to/essays/`

*Bonus*
`python3 essay_scorer.py path/to/essays/ >> output.csv`

**For a single text file**
`python3 essay_scorer.py path/to/essays/test.txt`

### Importing in a python script

```
import essay_scorer

text = open('test.txt', 'r').read()
feat_set = essay_scorer.get_feats(text)
pred_score = essay_scorer.gbr_model.predict(feats)[0]
print('predicted score', pred_score)
```
## About
This automated essay scoring system is based on [Travis Moore's master's thesis work](https://github.com/travismoore3/aes_system).

Moore's master's thesis, which lays the theoretical groundwork for this project can be found [here](https://scholarsarchive.byu.edu/cgi/viewcontent.cgi?article=7835&context=etd).

This model is best used on english learner essays that are between 140-300 words. Due to the distribution of scores in the model, this model tends to make better predictions around the median of actual scores from the dataset which seems to be around 20. There is more variance in predictions of outlier scores.

The model itself is a `GradientBoostingRegressor` model.  Here are the parameters and results of it testing itself on its own data:

```
`model.fit` results:
GradientBoostingRegressor(alpha=0.9, criterion='friedman_mse', init=None,
             learning_rate=0.02, loss='ls', max_depth=4, max_features=0.3,
             max_leaf_nodes=None, min_impurity_decrease=0.0,
             min_impurity_split=None, min_samples_leaf=9,
             min_samples_split=2, min_weight_fraction_leaf=0.0,
             n_estimators=500, n_iter_no_change=None, presort='auto',
             random_state=0, subsample=1.0, tol=0.0001,
             validation_fraction=0.1, verbose=0, warm_start=False)
Mean Absolute Error:
Train error:	2.360482423992901
Test error:	2.32169958721344

r2 scores of both train/test:
r2_train:	0.8341340712062068
r2_test:	0.8575492864872207
```

## License

GNU GPLv3 - see LICENSE file for details.2

## Contact

`@mkylemartin` on Twitter, GitHub


## Note

The pickled data file in this version does not include the age_bracket or language_id. The 49 features extracted are the following (in alphabetical order).
```
['ari', # readability index
 'avg_len_word',  	# average word length
 'cli', # readability measure
 'conjunctions', 
 'cttr', # corrected type to token ratio
 'dcrs', # dale chall readability score
 'determiners', 
 'dw', # difficult words
 'english_usage', # number of english words used
 'fkg', # flesch_kincaid_grade
 'fre',  # flesch_reading_ease
 'function_ttr', 
 'gf', # gunning_fog
 'grammar_chk', # checks for 2000+ grammar errors
 'lwf', # linsear_write_formula
 'n_bigram_lemma_types', 
 'n_bigram_lemmas', 
 'n_trigram_lemma_types',
 'n_trigram_lemmas', 
 'ncontent_words', 
 'nfunction_words', 
 'nlemma_types',
 'nlemmas', 
 'noun_ttr', 
 'num_tokens', 
 'num_types', 
 'pct_rel_trigrams',
 'pct_transitions', 
 'rank_avg', 
 'rank_total', 
 's1',  # negation stages (the next several features)
 's1a', 
 's1b', 
 's1c',
 's2', 
 's2a', 
 's2b', 
 's2c', 
 's3', 
 's3a', 
 's3b', 
 's3c', 
 's4', 
 's4a',
 's4b', 
 's4c', 
 'sent_density', # average words per sentence
 'spelling_perc',  # what percentage of words spelled correctly
 'ttr' # type token ratio ]
```


 
 
 
 
 
 
 
 
 
 
 
 
 
 