import re
import pandas as pd
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials


class Main(object):
    def __init__(self):
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('pellaton-0cb87179e701.json', scope)
        gc = gspread.authorize(credentials)
        spreadsheet = gc.open_by_url('https://docs.google.com/spreadsheets/d/1om9buTxyZ1QKTZFavoePHPwkiiS1zJC69NIeI7C5uj4/edit?usp=sharing')
        entities_df = self.get_google_sheet(spreadsheet, 0)
        segments_df = self.get_google_sheet(spreadsheet, 1)
        export = {'segments': [], 'entities': []}
        entities_dict = dict()
        for i, r in entities_df.iterrows():
            e = Entity(r)
            if e._name not in entities_dict:
                entities_dict[e._name] = e._name
            else:
                print(f'Entity {e._name} is not unique!')
            for v in e.variations:
                if v not in entities_dict:
                    entities_dict[v] = e._name
                else:
                    print(f'Variation {v} is not unique!')
            export['entities'].append(e.to_object())
        for _, r in segments_df.iterrows():
            s = Segment(r, entities_dict)
            export['segments'].append(s.to_object())
        with open('pellaton.json', 'w') as outfile:
            json.dump(export, outfile, indent=4)

    def get_google_sheet(self, spreadsheet:gspread.Spreadsheet, sheet:int):
        worksheet = spreadsheet.get_worksheet(sheet)
        data = worksheet.get_all_values()
        headers = data.pop(0)
        df = pd.DataFrame(data, columns=headers)
        return df

    def parse_entity(self, r:pd.Series) -> object:
        return {}

class Entity(object):
    def __init__(self, r: pd.Series):
        self._name = r['name']
        self._type = r['type']
        self.variations = []
        if not pd.isnull(r['variations']) and r['variations'].strip() != '':
            self.variations = re.split(r'\s*;\s*', str(r['variations']))
        self.wikidata = None if pd.isnull(r['wikidata']) else r['wikidata'].strip()
        self.sapa = None if pd.isnull(r['sapa']) else r['sapa'].strip()
        self.image = None if pd.isnull(r['image']) else r['image'].strip()

    def to_object(self) -> object:
        r = {'name': self._name, 'type': self._type}
        if self.variations:
            r['variations'] = self.variations
        if self.wikidata:
            r['wikidata'] = self.wikidata
        if self.sapa:
            r['sapa'] = self.sapa
        if self.image:
            r['image'] = self.image
        return r

class Segment(object):

    def __init__(self, r: pd.Series, entities_dict: dict):
        self.start = r['start']
        self.text = r['text']
        self.entities = [] 
        if not pd.isnull(r['entities']):
            for e in re.split(r'\s*;\s*', str(r['entities'])):
                if e in entities_dict:
                    self.entities.append(entities_dict[e])
                else:
                    print(f'Entity {e} not found!')

    def to_object(self) -> object:
        r = {'start': self.start}
        if self.text:
            r['text'] = self.text
        if len(self.entities) > 0:
            r['entities'] = self.entities
        return r

if __name__ == '__main__':
    m = Main()