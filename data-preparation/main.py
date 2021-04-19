
import re
from datetime import datetime
import spacy
import csv
import pandas
from pandas import DataFrame

def parse_ner(text):
    nlp = spacy.load("de_core_news_sm")
    doc = nlp(text)

    # more info can be extracted such as: e.start_char, e.end_char
    ents = [(e.text, e.label_) for e in doc.ents] # returns a list of tuples [(Zurich, LOC), (Ursula, PER) ...]
    return ents

def get_sec(time_str):
    time_str = time_str.replace("("," ").replace(")"," ").strip()
    if len(time_str.split(':')) == 2:
        m, s = time_str.split(':')
        return int(m) * 60 + int(s)
    else:
        h, m, s = time_str.split(':')
        return int(h)*3600 + int(m) * 60 + int(s)

def extract_unique_entities(text_split_on_timestamp, print=False):
    all_entities = dict()
    for count, paragraph in enumerate(text_split_on_timestamp):
        if count % 10 == 0:
            print(count)
        entities_found = parse_ner(paragraph)
        for ent in entities_found:
            all_entities[ent] = all_entities.get(ent, 0) + 1

    if print:
        with open('all_named_entities.csv', 'w') as f:
            for key in all_entities.keys():
                f.write("%s,%s,%s\n" % (key[0], key[1], all_entities[key]))

def extract_entities_per_paragraph(text_split_on_timestamp):

    entities_list_all_paragraphs = []
    for count, paragraph in enumerate(text_split_on_timestamp):
        if count % 10 == 0:
            print(count)
        entities_found = parse_ner(paragraph)
        entities_processed = []
        for entity in entities_found:
            name = entity[0]
            entities_processed.append(name)
        entities_names_concat = ';'.join(entities_processed)
        entities_list_all_paragraphs.append(entities_names_concat)

    return entities_list_all_paragraphs

def preprocess_text(paragraph):
    paragraph = paragraph.replace("[Anm. Transkription:", "(").replace("]",")").replace("(unv.)", "(?)")
    return paragraph

def prepare_and_annotate_paragraphs(text_split_on_timestamp, res_timestamps):
    res_timestamps.insert(0, "(00:00)")
    print(len(text_split_on_timestamp), len(res_timestamps))
    preprocessed_paragraphs = []
    for paragraph in text_split_on_timestamp:
        preprocessed_paragraphs.append(preprocess_text(paragraph))
    entities_list_all_paragraphs = extract_entities_per_paragraph(text_split_on_timestamp)

    df = DataFrame({'Start': res_timestamps, 'Content': preprocessed_paragraphs, 'Entities': entities_list_all_paragraphs})
    df.to_excel("time_segmented_content_entities.xlsx", sheet_name='sheet1', index=False)

def get_timestamps_statistics(res_timestamps):
    paragraph_lengths = []
    i, j = 0,1
    while j < len(res_timestamps):
        tdelta = get_sec(res_timestamps[j]) - get_sec(res_timestamps[i])
        paragraph_lengths.append(tdelta)
        j+=1
        i+=1
    print('\n Timestamps statistics:')
    print("AVG diff length (s):", sum(paragraph_lengths)/len(paragraph_lengths), paragraph_lengths)

def read_file(filename):
    with open(filename, 'r', encoding = 'utf-16') as file:
        text = file.read()

    # Remove all intermediate timestamps (usually appear together with a comment in the middle of a sentence/paragraph)
    text = re.sub("\(unv., .{2}:.{2}\)", "(?)", text)
    text = re.sub(", .{2}:.{2}]", "]", text)

    text_split_on_timestamp = re.compile(r'\(.{2}:.{2}\)|\(.{1}:.{2}:.{2}\)').split(text)
    print("Nr paragraphs: ",len(text_split_on_timestamp))
    #extract_unique_entities(text_split_on_timestamp, print=True)

    res_timestamps = re.findall(r'\(.{2}:.{2}\)|\(.{1}:.{2}:.{2}\)', text)
    print("Nr timestamps: ", len(res_timestamps), res_timestamps)

    prepare_and_annotate_paragraphs(text_split_on_timestamp, res_timestamps)


if __name__ == '__main__':
    filename = "20192705_Pellaton_Ausdruckstanz_unkorrigiert.txt"
    read_file(filename)
