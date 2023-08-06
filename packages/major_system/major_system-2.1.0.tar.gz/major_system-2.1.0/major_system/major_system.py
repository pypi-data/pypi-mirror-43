#!/usr/bin/env python3

import sys
import re
import itertools
import collections

__doc__ = """
Usage: {0} [options] <number>...
       {0} --version
       {0} --cmudict

<number>...                 Numbers to turn into words
                            If -, take <number>... from STDIN.

Options:
  -v, --version              Show version
  -M, --max-words=<number>   Maximum number of words to split into
                             [DEFAULT: 3]
  -m, --min-words=<number>   Minimum number of words to split into
                             [DEFAULT: 1]
  -b, --blacklist=<filename> File with a list of words to not use
  -d, --dict=<dictfile>      A custom phonetic dictionary (using the CMUdict
                             format)
  -e, --encoding=<encoding>  Encoding scheme of <dictfile>
                             For example, the CMU phonetic dictionary
                             needs 'latin-1' [DEFAULT: utf-8]
  -C, --cmudict              Send the entire included CMU phonetic dictionary
                             to STDOUT.  Good for starting your own custom
                             dictionary.
""".format(sys.argv[0])


from docopt import docopt


def arpabet_matches(number, phonemes):
  number = str(number)
  phoneme_index = 0
  phoneme_last_index = len(phonemes) - 1
  for digit in number:
    found_yet = False
    while not found_yet:

      # More digits, no more phonemes
      if phoneme_index > phoneme_last_index:
        return False

      cur_phoneme = phonemes[phoneme_index]

      # Found a phoneme matching `digit`
      if cur_phoneme in arpabet_phonemes(int(digit)):
        phoneme_index += 1
        found_yet = True

      # Found a phoneme that can be skipped
      elif cur_phoneme in arpabet_phonemes(None):
        phoneme_index += 1

      # Found an unskippable phoneme that doesn't match `digit`
      else:
        return False

  # Any remaining phonemes must be skippable
  for phoneme in phonemes[phoneme_index:]:
    if phoneme not in arpabet_phonemes(None):
      return False

  return True


def arpabet_phonemes(i):
  if i == 0:
    return ['S', 'Z']
  if i == 1:
    return ['T', 'D']
  if i == 2:
    return ['N']
  if i == 3:
    return ['M']
  if i == 4:
    return ['R', 'ER0', 'ER1', 'ER2']
  if i == 5:
    return ['L']
  if i == 6:
    return ['SH', 'JH', 'CH', 'ZH']
  if i == 7:
    return ['K', 'G']
  if i == 8:
    return ['F', 'V']
  if i == 9:
    return ['P', 'B']
  if i == None:
    return ['AA', 'AA0', 'AA1', 'AA2', 'AE', 'AE0', 'AE1', 'AE2', 'AH', 'AH0',
        'AH1', 'AH2', 'AO', 'AO0', 'AO1', 'AO2', 'AW', 'AW0', 'AW1', 'AW2',
        'AY', 'AY0', 'AY1', 'AY2', 'EH', 'EH0', 'EH1', 'EH2',
        'EY', 'EY0', 'EY1', 'EY2', 'HH', 'IH', 'IH0', 'IH1',
        'IH2', 'IY', 'IY0', 'IY1', 'IY2', 'OW0', 'OW1', 'OW2', 'OY', 'OY0',
        'OY1', 'OY2', 'UH', 'UH0', 'UH1', 'UH2', 'UW', 'UW0', 'UW1', 'UW2',
        'W', 'Y']
  raise ValueError("Expected a single digit or None")


def major_words(dictfile, number, blacklist=None, *, encoding='utf-8'):
  if blacklist == None:
    blacklist = []

  # If it's something that can only be iterated through once (like a file
  # pointer), reset to the beginning again
  if isinstance(dictfile, collections.Iterator):
    dictfile.seek(0)

  for line in dictfile:
    if isinstance(line, bytes):
      line = line.decode(encoding)

    # Skip comments and blank lines
    if line.startswith(';;;') or line.strip() == "":
      continue
    pieces = line.strip().split()
    if arpabet_matches(number, pieces[1:]):
      if pieces[0] not in blacklist:
        yield pieces[0]


def phrases_from_partition(dictfile, partition, blacklist=None, *,
    encoding='utf-8'):
  if blacklist == None:
    blacklist = []
  word_collection = []
  for part in partition:
    words = major_words(dictfile, part, blacklist, encoding=encoding)
    word_collection.append(words)
  for tup in itertools.product(*word_collection):
    yield " ".join(tup)


def phrases(dictfile, number, max_words=None, min_words=None,
    blacklist=None, *, verbosity=2, encoding='utf-8'):
  if blacklist == None:
    blacklist = []
  for partition in partitions(number, max_words, min_words):
    if verbosity > 1:
      for part in partition[:-1]:
        print(part, end=", ")
      print(partition[-1])
    for phrase in phrases_from_partition(dictfile, partition, blacklist,
        encoding=encoding):
      yield phrase


def ordered_tuples(tuple_length, num_elts):
  if tuple_length == 1:
    for i in range(1, num_elts):
      yield (i,)
  else:
    for tup in ordered_tuples(tuple_length - 1, num_elts):
      for i in range(tup[-1] + 1, num_elts):
        yield tup + (i,)


def partitions(arr, max_partitions=None, min_partitions=None):
  arr = str(arr)
  has_max = False
  try:
    has_max = True
    max_partitions = int(max_partitions)
  except (TypeError, ValueError) as e:
    has_max = False
  has_min = False
  try:
    has_min = True
    min_partitions = int(min_partitions)
  except (TypeError, ValueError) as e:
    has_min = False

  if has_max and max_partitions < 1:
    return []
  if has_min and has_max and min_partitions > max_partitions:
    return []
  num_elts = len(arr)

  to_return = []
  # length 1
  if not (has_min and min_partitions > 1):
    to_return = [[arr]]
  # higher lengths
  for partition_length in range(2, num_elts + 1):
    if has_max and partition_length > max_partitions:
      continue
    if has_min and partition_length < min_partitions:
      continue
    tuple_length = partition_length - 1
    for tup in ordered_tuples(tuple_length, num_elts):
      partition = []
      partition.append(arr[0:tup[0]])
      for i in range(0, tuple_length - 1):
        partition.append(arr[tup[i]:tup[i + 1]])
      partition.append(arr[tup[-1]:num_elts])
      to_return.append(partition)
  return to_return


def main():
  args = docopt(__doc__, version='2.1.0')

  if args['--cmudict']:
    import pkg_resources
    print(pkg_resources.resource_string("major_system",
        "cmu_phonetic_dictionary/cmudict-0.7b").decode('latin-1'))
    exit(0)

  # TODO Add distinct encodings for blacklist and dictionary files
  encoding = args['--encoding']

  # TODO Add an option to read the blacklist from disk instead of storing it
  # all in memory (probably better for giant blacklists)
  blacklist = []
  blacklist_filename = args['--blacklist']
  if blacklist_filename != None:
    try:
      with open(blacklist_filename, 'r', encoding=encoding) as blacklist_file:
        blacklist = [line.strip() for line in blacklist_file]
    except FileNotFoundError as e:
      print("Give a file full of words to the -b flag.")
      print("No file named {} is readable.".format(blacklist_filename))
      exit(1)

  dict_filename = args['--dict']
  if dict_filename != None:
    try:
      dictfile = open(dict_filename, 'r', encoding=encoding)
    except FileNotFoundError as e:
      print("Give a phonetic dictionary formatted like CMUdict to the -d flag.")
      print("No file at '{}'.".format(dict_filename))
      exit(1)
  else:
    import pkg_resources
    dictfile = pkg_resources.resource_stream("major_system",
        "cmu_phonetic_dictionary/cmudict-0.7b")
    encoding = 'latin-1'

  for number in args['<number>']:
    print("{}:".format(number))
    for phrase in phrases(dictfile, number, args['--max-words'],
        args['--min-words'], blacklist, encoding=encoding):
      print("  " + phrase.strip())


if __name__ == "__main__":
  main()
