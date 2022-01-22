import json
import random

alpha = 'abcdefghijklmnopqrstuvwxyz'

blacklist = [
        'kioea', 'seora', 'wuzzy', 'fldxt', 'jough',
        'musha', 'japyx', 'aoife', 'zoque', 'aueto',
        'oreas', 'khuzi', 'linge', 'luite', 'aotes',
        'pinge', 'digne',
        ]

def index_by_length(words):
    index = {}
    for w in words:
        l = len(w)
        if l in index:
            index[l].add(w)
        else:
            index[l] = {w}

    return index

def index_by_contain_letter(words):
    index = {}
    for w in words:
        for a in alpha:
            if a in w:
                if a in index:
                    index[a].add(w)
                else:
                    index[a] = {w}
    return index

def index_by_letter_position(n, index_letters):
    index = {}
    for a in alpha:
        words = index_letters[a]
        for w in words:
            for i in list(range(n)):
                if w[i] == a:
                    if a in index:
                        if i in index[a]:
                            index[a][i].add(w)
                        else:
                            index[a][i] = {w}
                    else:
                        index[a] = { i: {w} }

    return index

def analyze_guess(n, index_letters, state, guess):
    result = {
        'word': guess,
    }

    hit = set()
    for a in guess:
        if a in state['hits']:
            continue
        hit |= (state['candidates'] & index_letters[a])

    result['hit_probability'] = len(hit)/len(state['candidates'])
    return result

def extract_outcome(n, guess, outcome):
    result = {
        '0': [],
        '1': [],
        '2': [],
            }

    for i in list(range(n)):
        if outcome[i] == '0':
            result['0'].append(guess[i])
        elif outcome[i] == '1':
            result['1'].append([guess[i], i])
        elif outcome[i] == '2':
            result['2'].append([guess[i], i])

    return result

def update_state(n, index_letters, index_position, current, guess, outcome):
    outcome = extract_outcome(n, guess, outcome)

    current['used'] |= set(guess)
    for a in outcome['1']:
        current['hits'] |= set(a[0])
    for a in outcome['2']:
        current['hits'] |= set(a[0])

    for a in outcome['0']:
        current['candidates'] &= (current['candidates'] - index_letters[a])
    for a in outcome['1']:
        current['candidates'] &= index_letters[a[0]]
        current['candidates'] &= (current['candidates'] - index_position[a[0]][a[1]])
    for a in outcome['2']:
        current['candidates'] &= index_letters[a[0]]
        current['candidates'] &= index_position[a[0]][a[1]]

def suggest(n, index_letters, opening, current):
    results = []
    if len(current['used']) == 0:
        results = opening
        results = [r for r in results if r['word'] not in blacklist]
    else:
        for g in current['candidates']:
            if g in blacklist:
                continue
            results.append(analyze_guess(n, index_letters, current, g))

    guesses = sorted(results, key=lambda r: r['hit_probability'], reverse=True)
    if len(guesses) == 0:
        return None

    if len(current['used']) == 0:
        guesses = [r for r in guesses if r['hit_probability'] > 0.94]
        return random.choice(guesses)

    return guesses[0]

def calculate_outcome(n, guess, wotd):
    outcome = ['0', '0', '0', '0', '0']
    guess = list(guess)
    wotd = list(wotd)

    for i in list(range(n)):
        if guess[i] == wotd[i]:
            outcome[i] = '2'
            wotd[i] = '.'
            guess[i] = '.'

    for i in list(range(n)):
        if outcome[i] == '2':
            continue

        k = ''.join(wotd).find(guess[i])
        if k != -1:
            outcome[i] = '1'
            guess[i] = '.'
            wotd[k] = '.'

    return ''.join(outcome)

def main():
    with open('words_dictionary.json') as f:
        words = set(json.load(f).keys())

    index_length = index_by_length(words)
    words = set(list(index_length[5])[:100000])
    words = set([w for w in words if w not in blacklist])

    index_letters = index_by_contain_letter(words)
    index_position = index_by_letter_position(5, index_letters)

    with open('opening_stats.json') as g:
        opening = json.load(g)

    #wotds = []
    #for i in range(1000):
    #    wotds.append(random.choice(list(words)))

    #i = 0
    #while i < len(wotds):
    #    state = {
    #        'candidates': words.copy(),
    #        'used': set(),
    #        'hits': set(),
    #    }

    #    wotd = wotds[i]

    #    attempts = 0
    #    outcome = '00000'
    #    suggestion = None
    #    moves = []

    #    while outcome != '22222':
    #        suggestion = suggest(5, index_letters, opening, state)
    #        # If for some reason suggestion is empty (this is a bug),
    #        # just retry with another opening
    #        if suggestion is None:
    #            break

    #        moves.append(suggestion['word'])

    #        outcome = calculate_outcome(5, suggestion['word'], wotd)
    #        update_state(5, index_letters, index_position, state, suggestion['word'], outcome)
    #        attempts += 1

    #    if suggestion is None:
    #        print('{}: {}'.format(wotd, 'failed'))
    #        i += 1
    #        continue

    #    print('{}: {} ({})'.format(wotd, attempts, ' -> '.join(moves)))
    #    i += 1

    print('outcome is string of format: (0|1|2){5}, where 0=grey, 1=yellow, 2=green')
    print()

    state = {
        'candidates': words.copy(),
        'used': set(),
        'hits': set(),
    }

    suggestion = suggest(5, index_letters, opening, state)
    print(suggestion)

    while len(state['candidates']) > 1:
        outcome = input('outcome: ')
        update_state(5, index_letters, index_position, state, suggestion['word'], outcome)

        suggestion = suggest(5, index_letters, opening, state)
        print(suggestion)

if __name__ == "__main__":
    main()
