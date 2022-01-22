## How it works

At each step, the solver picks the word that has the highest probability of resulting
in a single letter hit.

Some TODOs

- [ ] The first step should use a different strategy (e.g. pick a word that will reduce the search space the most)
- [ ] The word list I'm using has a lot of words that Wordle considers as not valid. Need to find a better word list
- [ ] There is a bug where the solver runs out of guesses, which should not happen
- [ ] The solver's biggest weakness are words that only differ by a single letter. E.g. if the solver tries to solve the word "hails", it manages to guess ".ails" within 3 moves, but then takes a lot of steps to guess the first letter because there are too many possibilities (bails, fails, jails, mails, nails, pails, rails, sails, tails, wails)

## Guide

To run the solver:

```sh
python run.py
```

The solver will suggest the word to enter. After entering the suggested word,
enter the outcome (e.g. if everything is grey, then the outcome is `00000`).
The solver will then suggest the next word to enter.

Sample run (wordle 217):

```sh
outcome is string of format: (0|1|2){5}, where 0=grey, 1=yellow, 2=green

{'word': 'aeons', 'hit_probability': 0.9518155547179293}
outcome: 01010
{'word': 'inure', 'hit_probability': 0.8672199170124482}
outcome: 11002
{'word': 'minge', 'hit_probability': 0.43478260869565216}
outcome: 02202
{'word': 'wince', 'hit_probability': 0.5}
outcome: 22222
```

<img src="wordle217.png" />
