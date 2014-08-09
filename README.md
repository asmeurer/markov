## Generate Markov Text from your Hangouts Chat

This uses https://github.com/TehMillhouse/PyMarkovChain to generate random
sentences from your Google Hangouts chat using Markov Chains.

### How to use

You need to go to https://www.google.com/settings/takeout/custom and download
your hangouts as json. Then go in and find the chat you are interested in. For
me, it was the most recent one, so (in Python)

```py
>>> import json
>>> from os.path import expanduser
>>> a = json.load(open(expanduser('~/Downloads/asmeurer@gmail.com-20140504T004644Z-Hangouts/Hangouts/Hangouts.json')))
>>> b = a['conversation_state']
>>> c = b[-1] # You'll want to look at the elements of b to get the chat you are interested in
>>> json.dump(c['event'], open("hangouts.json")) # To this directory
```

Then run

```bash
$ ./markov.py
```

to generate a sentence. You can also supply a seed like,

```bash
$ ./markov.py you are
```
