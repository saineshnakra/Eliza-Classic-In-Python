import logging
import random
import re

log = logging.getLogger(__name__)

class Key:
    def __init__(self, word, weight, decomps):
        self.word = word  
        self.weight = weight  
        self.decomps = decomps 

class Decomp:
    def __init__(self, parts, save, reasmbs):
        self.parts = parts  
        self.save = save  
        self.reasmbs = reasmbs 
        self.next_reasmb_index = 0 

class Eliza:
    def __init__(self):
        self.initials = []  
        self.finals = []  
        self.quits = []  
        self.pres = {}  
        self.posts = {}  
        self.synons = {} 
        self.keys = {}  
        self.memory = [] 

    def load(self, path):
        """Load the script from the provided file."""
        key = None
        decomp = None
        with open(path) as file:
            for line in file:
                if not line.strip():
                    continue
                tag, content = [part.strip() for part in line.split(':')]
                if tag == 'initial':
                    self.initials.append(content)
                elif tag == 'final':
                    self.finals.append(content)
                elif tag == 'quit':
                    self.quits.append(content)
                elif tag == 'pre':
                    parts = content.split(' ')
                    self.pres[parts[0]] = parts[1:]
                elif tag == 'post':
                    parts = content.split(' ')
                    self.posts[parts[0]] = parts[1:]
                elif tag == 'synon':
                    parts = content.split(' ')
                    self.synons[parts[0]] = parts
                elif tag == 'key':
                    parts = content.split(' ')
                    word = parts[0]
                    weight = int(parts[1]) if len(parts) > 1 else 1
                    key = Key(word, weight, [])
                    self.keys[word] = key
                elif tag == 'decomp':
                    parts = content.split(' ')
                    save = False
                    if parts[0] == '$':
                        save = True
                        parts = parts[1:]
                    decomp = Decomp(parts, save, [])
                    key.decomps.append(decomp)
                elif tag == 'reasmb':
                    parts = content.split(' ')
                    decomp.reasmbs.append(parts)

        # A default key for fallback responses (handling 'none' case)
        if 'xnone' not in self.keys:
            self.keys['xnone'] = Key('xnone', 1, [
                Decomp(['*'], False, [
                    ['Can you tell me more about that?'],
                    ['Please go on.'],
                    ['What does that suggest to you?'],
                    ['I see. Can you elaborate on that?'],
                    ['That is interesting. Please continue.']
                ])
            ])

    def _match_decomp_r(self, parts, words, results):
        """Recursively match decomposition rules."""
        if not parts and not words:
            return True
        if not parts or (not words and parts != ['*']):
            return False
        if parts[0] == '*':
            for index in range(len(words), -1, -1):
                results.append(words[:index])
                if self._match_decomp_r(parts[1:], words[index:], results):
                    return True
                results.pop()
            return False
        elif parts[0].startswith('@'):
            root = parts[0][1:]
            if root not in self.synons:
                raise ValueError(f"Unknown synonym root {root}")
            if words[0].lower() not in self.synons[root]:
                return False
            results.append([words[0]])
            return self._match_decomp_r(parts[1:], words[1:], results)
        elif parts[0].lower() != words[0].lower():
            return False
        else:
            return self._match_decomp_r(parts[1:], words[1:], results)

    def _match_decomp(self, parts, words):
        """Match the decomposition rules against the input."""
        results = []
        if self._match_decomp_r(parts, words, results):
            return results
        return None

    def _next_reasmb(self, decomp):
        """Get the next reassembly rule."""
        index = decomp.next_reasmb_index
        result = decomp.reasmbs[index % len(decomp.reasmbs)]
        decomp.next_reasmb_index = index + 1
        return result

    def _reassemble(self, reasmb, results):
        """Reassemble the output using matched decomposition."""
        output = []
        for reword in reasmb:
            if not reword:
                continue
            if reword[0] == '(' and reword[-1] == ')':
                index = int(reword[1:-1])
                if index < 1 or index > len(results):
                    raise ValueError(f"Invalid result index {index}")
                insert = results[index - 1]
                for punct in [',', '.', ';']:
                    if punct in insert:
                        insert = insert[:insert.index(punct)]
                output.extend(insert)
            else:
                output.append(reword)
        return output

    def _sub(self, words, sub):
        """Apply pre- or post-substitutions to the input."""
        output = []
        for word in words:
            word_lower = word.lower()
            if word_lower in sub:
                output.extend(sub[word_lower])
            else:
                output.append(word)
        return output

    def _match_key(self, words, key):
        """Try to match the user input against a key's decompositions."""
        for decomp in key.decomps:
            results = self._match_decomp(decomp.parts, words)
            if results is None:
                continue
            results = [self._sub(words, self.posts) for words in results]
            reasmb = self._next_reasmb(decomp)
            if reasmb[0] == 'goto':
                goto_key = reasmb[1]
                if goto_key not in self.keys:
                    raise ValueError(f"Invalid goto key {goto_key}")
                return self._match_key(words, self.keys[goto_key])
            output = self._reassemble(reasmb, results)
            if decomp.save:
                self.memory.append(output)
                continue
            return output
        return None

    def respond(self, text):
        """Generate a response to the input text."""
        if text.lower() in self.quits:
            return None

        text = re.sub(r'\s*\.+\s*', ' . ', text)
        text = re.sub(r'\s*,+\s*', ' , ', text)
        text = re.sub(r'\s*;+\s*', ' ; ', text)

        words = [w for w in text.split(' ') if w]

        words = self._sub(words, self.pres)

        keys = [self.keys[w.lower()] for w in words if w.lower() in self.keys]
        keys = sorted(keys, key=lambda k: -k.weight)

        output = None

        for key in keys:
            output = self._match_key(words, key)
            if output:
                break
        
        if not output:
            output = self._next_reasmb(self.keys['xnone'].decomps[0])

        return " ".join(output)

    def initial(self):
        """Return a random initial greeting."""
        return random.choice(self.initials)

    def final(self):
        """Return a random final statement."""
        return random.choice(self.finals)

    def run(self):
        """Run the main conversation loop."""
        print(self.initial())
        while True:
            sent = input('> ')
            output = self.respond(sent)
            if output is None:
                break
            print(output)
        print(self.final())

def main():
    eliza = Eliza()
    eliza.load('doctor.txt')  # Load the script
    eliza.run()

if __name__ == '__main__':
    logging.basicConfig()
    main()
