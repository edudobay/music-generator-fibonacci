#!/usr/bin/env python3
import numpy as np
import sys

def clamp(x, min, max):
    if x < min: return min
    if x > max: return max
    return x

def gen_fibonacci():
    a, b = 1, 1
    while True:
        yield a
        a, b = b, a + b

def random_lengths(amount, distribution):
    notelen, probs = np.array(distribution).T
    probs = (probs.astype(float) / probs.sum()).cumsum()
    x = np.random.uniform(0, 1, (amount,))
    return notelen[probs.searchsorted(x)]

def random_permutation_of_range(l):
    x = np.arange(l)
    y = x.copy()
    np.random.shuffle(y)
    return dict(zip(x, y))

def generate_music(
        output_file,
        music_length,
        lengths_distribution,
        bpm,
        ):
    import mingus.core.notes as notes
    from mingus.containers.note import Note
    from mingus.containers.track import Track
    from mingus.midi import midi_file_out

    t = Track()

    note_seed = 12

    s = random_permutation_of_range(9)

    def next_note(fib_seed, last_note):
        n = last_note + s[fib_seed % 9] - 4
        return int(clamp(n, 0, 24))

    note = note_seed

    for fib_seed, length in zip(gen_fibonacci(), random_lengths(music_length, lengths_distribution)):

        note = next_note(fib_seed, note)

        n = Note()
        n.from_int(note + 36)
        t.add_notes(n, length)

    midi_file_out.write_Track(output_file, t, bpm=bpm)

def main():
    DEFAULT_BPM = 84
    DEFAULT_MUSIC_LENGTH = 1000

    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('output_file')
    parser.add_argument('-b', '--bpm', type=int, default=DEFAULT_BPM)
    parser.add_argument('-l', '--length', type=int, default=DEFAULT_MUSIC_LENGTH)

    args = parser.parse_args()

    lengths_distribution = [
        (1, 0.3),
        (2, 0.4),
        (4, 0.3),
    ]

    generate_music(
        output_file=args.output_file,
        music_length=args.length,
        bpm=args.bpm,
        lengths_distribution=lengths_distribution,
    )

if __name__ == '__main__':
    main()
