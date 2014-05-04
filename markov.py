#!/usr/bin/env python

import json

from pymarkovchain import MarkovChain

def get_hangouts_text():
    # Should just be one conversation from 'conversation_state'
    with open('hangouts.json') as f:
        j = json.load(f)

    text = []
    for item in j:
        if 'chat_message' in item:
            for segment in item['chat_message']['segment']:
                text.append(segment['text'])
        if 'conversation_rename' in item:
            # Only add the new name. The old name was already added
            text.append(item['conversation_rename']['new_name'])

    return text

def main():
    # Create an instance of the markov chain. By default, it uses MarkovChain.py's location to
    # store and load its database files to. You probably want to give it another location, like so:
    mc = MarkovChain("./markov")

    # To generate the markov chain's language model, in case it's not present
    mc.generateDatabase('\n'.join(get_hangouts_text()))
    # To let the markov chain generate some text, execute
    print(mc.generateString())

if __name__ == '__main__':
    main()
