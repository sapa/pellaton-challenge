## Data Preparation

This module contains the code to pre-process the interview transcripts. It also has the code to generate word clouds. Note that the original rtf files were converted to txt first, e.g. by using https://convertio.co/rtf-txt/.

### Requirements
- SpaCy for NLP functionalities, see https://spacy.io/usage.
```
pip install spacy
```
and the pre-trained german model:
```
python -m spacy download de_core_news_sm
```

- Pandas
```
pip install pandas
```
- NLTK
```
pip install nltk
```
- wordcloud

```
pip install wordcloud
```

### Usage

There are two files:
1. **main.py** contains the functions for: 
   - extract_unique_entities(): extracting all uniques entities and their frequency from the text
    - prepare_and_annotate_paragraphs(): gets as input list of paragraph texts and list of timestamps. For each paragraph Named Entities are extracted and pre-processing is applied to the paragraph text. Preprocessing includes:
    ```
   paragraph.replace("[Anm. Transkription:", "(").replace("]",")").replace("(unv.)", "(?)").replace("unv.", "?")
    ``` 
2. **topic_modelling_word_clouds.py** contains the functions for: 
   - filter_stopwords(): expands the nltk basic list of stopwords with some custom words that will be ignored when performing further NLP tasks, filters the text, reuturns the stop words list and filtered text
   - generate_wordcloud(): uses library to generate a wordcloud from the text and provided list of the stopwords; text input is the original text, lower-cased; wordcloud visuals stored in folder /outputs