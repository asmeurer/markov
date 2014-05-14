#!/usr/bin/env python

import json
from pprint import pprint
from collections import defaultdict
import sys
import os
import re

from pymarkovchain import MarkovChain

link_re = re.compile(r'https?://\S*')

def delete_links(text):
    return link_re.sub('', text)

def get_hangouts_text():
    # Should just be one conversation from 'conversation_state'
    with open('hangouts.json') as f:
        j = json.load(f)

    empty = defaultdict(list)

    text = []
    for item in j:
        if 'chat_message' in item:
            try:
                for segment in item['chat_message']['message_content'].get('segment', []):
                    if 'text' in segment:
                        text.append(segment['text'])
            except KeyError:
                pprint(item)
                raise
        if 'conversation_rename' in item:
            # Only add the new name. The old name was already added
            text.append(item['conversation_rename']['new_name'])

    return text

def main():
    # Regenerate the model only if the database or this file are newer. We
    # need to check this here because MarkovChain creates an empty database if
    # none exists.
    regen = (not os.path.exists('./markov') or os.path.getmtime('markov') <
        os.path.getmtime('hangouts.json') or os.path.getmtime('markov') <
        os.path.getmtime(__file__))

    # Create an instance of the markov chain. By default, it uses MarkovChain.py's location to
    # store and load its database files to. You probably want to give it another location, like so:
    mc = MarkovChain("./markov")

    if regen:
        text = '\n'.join(get_hangouts_text())
        text = delete_links(text)
        print(text)
        mc.generateDatabase(text)

    # To let the markov chain generate some text, execute
    if len(sys.argv) > 1:
        print(mc.generateStringWithSeed(' '.join(sys.argv[1:])))
    else:
        print(mc.generateString())


if __name__ == '__main__':
    main()
