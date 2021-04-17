import re
from datetime import datetime
import spacy
import csv
import pandas
from pandas import DataFrame
import nltk
import ssl
import matplotlib.pyplot as plt
from wordcloud import WordCloud

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
#nltk.download()
from nltk.corpus import stopwords

def get_tokens(text):
    nlp = spacy.load("de_core_news_sm")
    doc = nlp(text)

    # document level e.start_char, e.end_char,
    words = [token.text for token in doc]
    return words

def filter_stopwords(text):
    stop_words = set(stopwords.words('german'))

    word_tokens = get_tokens(text)
    filtered_sentences = [w for w in word_tokens if not w in stop_words]

    stop_words.add("ja")
    stop_words.add("eben")
    stop_words.add("eigentlich")
    stop_words.add("immer")
    stop_words.add("einfach")
    stop_words.add("ganz")
    stop_words.add("schon")
    stop_words.add("mehr")
    stop_words.add("natürlich")

    stop_words.add("glaube")
    stop_words.add("sachen")
    stop_words.add("mal")
    stop_words.add("gehabt")
    stop_words.add("gibt")
    stop_words.add("genau")
    stop_words.add("viele")
    stop_words.add("irgendwie")
    stop_words.add("beispiel")
    stop_words.add("wirklich")
    stop_words.add("konnte")
    stop_words.add("macht")
    stop_words.add("quasi")
    stop_words.add("worden")

    stop_words.add("gemacht")
    stop_words.add("gekommen")
    stop_words.add("wahrscheinlich")
    stop_words.add("sagen")
    stop_words.add("gegeben")
    stop_words.add("gegangen")
    stop_words.add("vielleicht")

    stop_words.add("kommt")
    stop_words.add("eher")
    stop_words.add("sieht")
    stop_words.add("grosse")
    stop_words.add("halt")
    stop_words.add("nie")
    stop_words.add("irgendetwas")

    stop_words.add("beim")
    stop_words.add("gerade")
    stop_words.add("meisten")
    stop_words.add("gekannt")
    stop_words.add("grossen")
    stop_words.add("gab")
    stop_words.add("konnten")
    stop_words.add("i")

    stop_words.add("überhaupt")
    stop_words.add("p")
    stop_words.add("nein")

    stop_words.add("darum")
    stop_words.add("sicher")
    stop_words.add("sei")
    stop_words.add("irgendwann")
    stop_words.add("geworden")

    return stop_words, filtered_sentences

def generate_wordcloud(text, stopwords, plot_title):
    wordcloud = WordCloud(width=800, height=800,
                          background_color='white',
                          stopwords=stopwords,
                          min_font_size=10).generate(text)

    # plot the WordCloud image
    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)

    plt.savefig(plot_title)
    #plt.show()

def read_file(filename):

    # Use a breakpoint in the code line below to debug your script.
    with open(filename, 'r', encoding = 'utf-16') as file:
        text = file.read()

    text = re.sub("\(unv., .{2}:.{2}\)", "(?)", text)
    text = re.sub(", .{2}:.{2}]", "]", text)
    text = text.replace("[Anm. Transkription:", "(").replace("]",")").replace("(unv.)", "(?)")
    text = text.lower()

    text_split_on_timestamp = re.compile(r'\(.{2}:.{2}\)|\(.{1}:.{2}:.{2}\)').split(text)
    print("Nr paragraphs: ", len(text_split_on_timestamp))
    stop_words, filtered_sentences = filter_stopwords(text)
    generate_wordcloud(text, stop_words, "outputs/wordcloud_full_text.png")

    for i in range(10):
        generate_wordcloud(text_split_on_timestamp[i], stop_words, "outputs/wordcloud_full_text_{}.png".format(str(i)))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    filename = "20192705_Pellaton_Ausdruckstanz_unkorrigiert.txt"
    read_file(filename)