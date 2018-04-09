import mingus.core.notes as notes
from mingus.containers.Note import Note
from mingus.containers.Track import Track
from mingus.midi import MidiFileOut
import numpy as np
import sys

def fib():
    a, b = 1, 1
    while True:
        yield a
        a, b = b, a + b

def lengths(n, dist):
    notelen, probs = np.array(dist).T
    probs = (probs.astype(float) / probs.sum()).cumsum()
    x = np.random.uniform(0, 1, (n,))
    return notelen[probs.searchsorted(x)]

dist = [
    ( 1, 3),
    ( 2, 4),
    ( 4, 3),
]

def clamp(x, min, max):
    if x < min: return min
    if x > max: return max
    return x

t = Track()

def scramble(l):
    x = np.arange(l)
    y = x.copy()
    np.random.shuffle(y)
    return dict(zip(x, y))

note = 12
s = scramble(9)
for _, f, l in zip(range(1000), fib(), lengths(1000, dist)):
    note, lastnote = (note + s[f % 9] - 4), note
    note = int(clamp(note, 0, 24))
    n = Note()
    n.from_int(note + 36)
    t.add_notes(n, l)

fname = sys.argv[1]
MidiFileOut.write_Track(fname, t, bpm=84)

