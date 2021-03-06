# -*- coding: utf-8 -*-
# Part of bubble. See LICENSE file for full copyright and licensing details.


"""store: for getting and putting files in json format"""

import io
from . import BubbleKV

import simplejson as json

def no_enc_fun():
    pass


class JsonKV(BubbleKV):

    """store and retrieve a List of dictionaries in sqlite.
    """
    _encode = no_enc_fun
    _decode = no_enc_fun

    def __init(self, file_name, reset=False):
        BubbleKV.__init__(self,
                          name='JsonKV',
                          file_name=file_name,
                          reset=reset)
        self._can_dump_generator = True
        self.say('here')

    def _dump(self, data={}, full_data=True):
        self.say('dumping', verbosity=10)
        with io.open(self._file_name, 'w', encoding='utf8') as json_file:
            json.dump(data, json_file, ensure_ascii=False)

    def _encode_for_try(self, data={}):
        self.say('_encode_for_try', verbosity=10)
        json.dumps(data, ensure_ascii=False)

    def _load(self):
        jsonfile = open(self._file_name)
        content = jsonfile.read()
        self.say('content=' + content, verbosity=10001)
        try:
            res = json.loads(content)
            self.say('res:', stuff=res, verbosity=10001)
            return res
        except ValueError as ve:
            res = {}
            res['error'] = 'cannot decode json, ValueError'
            res['exception'] = str(ve)
            return res
