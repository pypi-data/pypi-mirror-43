from major_system import major_system as ms
import pytest

@pytest.fixture
def dictfile():
  return ['abc', 'dog', 'Cat', 'tag', 'toggle', 'at', 'yell', 'well',
      'what', 'tall', 'deal', 'gill', 'gal', 'ick', 'sail', 'sole',
      'seal']

@pytest.fixture
def phonetic_dictfile():
  return [
    'BABYSITTER  B EY1 B IY0 S IH2 T ER0',
    'BABYSITTERS  B EY1 B IY0 S IH2 T ER0 Z',
    'BABYSITTING  B EY1 B IY0 S IH2 T IH0 NG',
    'BACA  B AE1 K AH0',
    'BACALL  B AH0 K AO1 L',
    'BACARDI  B AH0 K AA1 R D IY0',
    'BACCALAUREATE  B AE2 K AH0 L AO1 R IY0 AH0 T',
    'DON  D AA1 N',
    'DAWN  D AO1 N',
    'DAUN  D AO1 N',
    'DUNFORD  D AH1 N F ER0 D',
    'DUNG  D AH1 NG',
    'DUNGAN  D AH1 NG G AH0 N',
    'DUNGEON  D AH1 N JH AH0 N',
    'DUNGEONS  D AH1 N JH AH0 N Z',
    'DUNGEY  D AH1 N JH IY0',
    'DUNHAM  D AH1 N AH0 M',
    'DUNHILL  D AH1 N HH IH2 L',
    'FUTONS  F UW1 T AA0 N Z',
    'FUTRAL  F AH1 T R AH0 L',
    'FUTRELL  F Y UW0 T R EH1 L',
    'FUTTERMAN  F AH1 T ER0 M AH0 N',
    'FUTURE  F Y UW1 CH ER0',
  ]


def assert_equal_except_order(left, right):
  assert len(left) == len(right)
  for i in left:
    assert i in right

def test_partitions():
  assert ms.partitions("a") == [["a"]]
  assert ms.partitions("ab") == [["ab"], ["a", "b"]]
  assert ms.partitions("abc") == [["abc"], ["a", "bc"], ["ab", "c"], ["a", "b", "c"]]
  assert ms.partitions("abcd") == [["abcd"], ["a", "bcd"], ["ab", "cd"], ["abc", "d"], ["a", "b", "cd"], ["a", "bc", "d"], ["ab", "c", "d"], ["a", "b", "c", "d"]]
  assert ms.partitions("a", 0) == []
  assert ms.partitions("ab", 1) == [["ab"]]
  assert ms.partitions("abc", 0) == []
  assert ms.partitions("abc", 1) == [["abc"]]
  assert ms.partitions("abc", 2) == [["abc"], ["a", "bc"], ["ab", "c"]]
  assert ms.partitions("abc", 3) == [["abc"], ["a", "bc"], ["ab", "c"], ["a", "b", "c"]]
  assert ms.partitions("abc", 4) == [["abc"], ["a", "bc"], ["ab", "c"], ["a", "b", "c"]]
  assert ms.partitions("abc", 5) == [["abc"], ["a", "bc"], ["ab", "c"], ["a", "b", "c"]]
  assert ms.partitions("abc", 6) == [["abc"], ["a", "bc"], ["ab", "c"], ["a", "b", "c"]]
  assert ms.partitions("abc", 7) == [["abc"], ["a", "bc"], ["ab", "c"], ["a", "b", "c"]]
  assert ms.partitions("abc", None) == [["abc"], ["a", "bc"], ["ab", "c"], ["a", "b", "c"]]
  assert ms.partitions("abcd") == [["abcd"], ["a", "bcd"], ["ab", "cd"], ["abc", "d"], ["a", "b", "cd"], ["a", "bc", "d"], ["ab", "c", "d"], ["a", "b", "c", "d"]]


def test_major_words(dictfile, phonetic_dictfile):
  with open("cmu_phonetic_dictionary/cmudict-0.7b", "r", encoding="latin-1") as f:
    expected = [
      'AD-HOC', 'ADACHI', 'ADAK', 'ADWEEK', 'ATCO', 'ATEK', 'ATICO',
      'ATTACK', 'ATTIC', 'ATTICA', 'DAC', 'DACHAU', 'DACK', 'DAG',
      'DAGG', 'DAGGY', 'DAGUE', 'DAK', 'DAK(1)', 'DAKE', 'DAYCO',
      'DEAK', 'DEC', 'DECAY', 'DECCA', 'DECH', 'DECK', 'DECO', 'DECOU',
      'DECOY', 'DEEG', 'DEGAS(1)', 'DEHECQ', 'DEIKE', 'DEKAY', 'DHAKA',
      'DHAKA(1)', 'DHAKA(2)', 'DIC', 'DICK', 'DICKE', 'DICKEY', 'DICKIE',
      'DICKY', 'DIECK', 'DIEGO', 'DIG', 'DIGGA', 'DIKE', 'DK', 'DOAK',
      'DOC', 'DOCIE', 'DOCK', 'DOG', 'DOGGIE', 'DOGGY', 'DOIG', 'DOKE',
      'DOKEY', 'DOOGIE', 'DOUG', 'DOUGIE', 'DUC', 'DUCA', 'DUCK', 'DUCKY',
      'DUG', 'DUGO', 'DUGUAY', 'DUK', 'DUKE', 'DUQUE', 'DWECK', 'DYCK',
      'DYCO', 'DYK', 'DYKE', 'EDICK', 'EYETECH', 'HADDOCK', 'HAJDUK',
      'HAYDOCK', 'HAYDUK', 'HEADACHE', 'HEDTKE', 'HEDWIG', 'HEDWIGA',
      'HETTICK', 'HIDEAKI', 'HIGH-TECH', 'HIGHTECH', 'HODAK', 'HOUDEK',
      'HOWTEK', 'HUDAK', 'HUDEC', 'HUDEK', 'HUDOCK', 'HYDOCK', 'IDEC',
      'INDICA', 'ITEK', 'ODAIKO', 'OUTGO', 'OUTTAKE(1)', 'PTAK', 'TAC',
      'TACK', 'TACKE', 'TACKY', 'TACO', 'TAEGU', 'TAG', 'TAGG', 'TAGGE',
      'TAGUE', 'TAIKO', 'TAK', 'TAKAO', 'TAKE', 'TAKEI', 'TAKEO',
      'TAKI', 'TAKIHYO', 'TAKU', 'TALK', 'TALKIE', 'TALKY', 'TAUKE',
      'TEAC', 'TEAC(1)', 'TEAGUE', 'TEAK', 'TEC', 'TECH', 'TECHIE',
      'TECK', 'TECO', 'TEGGE', 'TEICH', 'TEIG', 'TEK', 'TIC', 'TICK',
      'TIG', 'TIGHE', 'TIGUE', 'TIKE', 'TIKI', 'TOCCO', 'TOCK', 'TOGA',
      'TOGO', 'TOKAI', 'TOKIO', 'TOKUO', 'TOKYO', 'TOKYU', 'TOOK',
      'TOOKE', 'TOYKO', 'TUCK', 'TUCKEY', 'TUG', 'TUK', 'TWEAK', 'TWIG',
      'TWIGG', 'TWIGGY', 'TWOHIG', 'TYCO', 'TYKE', 'T_A_C(1)', 'UDAGAWA',
      'UTECH', 'UTICA', 'UTICA(1)', 'UTKE', 'UTTECH', 'WEDIG', 'WEIDIG',
      'WEITEK', 'WIDICK', 'WITCO', 'WITTIG', 'WITTKE', 'WITUCKI',
      'WOODKE', 'WUTTKE', 'YUTAKA',
    ]
    assert [x for x in ms.major_words(f, 17, True)] == expected

  assert [x for x in ms.major_words(phonetic_dictfile, 12, True)] == ['DON', "DAWN", "DAUN"]
  assert [x for x in ms.major_words(phonetic_dictfile, 12, True, ['DAWN'])] == ['DON', "DAUN"]
  assert [x for x in ms.major_words(phonetic_dictfile, 12, True, ['DAWN', 'DON'])] == ["DAUN"]
  assert [x for x in ms.major_words(phonetic_dictfile, 12, True, ['DAWN', 'DON', 'DAUN'])] == []

  assert [x for x in ms.major_words(dictfile, 17)] == ["dog", 'tag']
  assert [x for x in ms.major_words(dictfile, 175)] == ["toggle"]
  assert [x for x in ms.major_words(dictfile, 8)] == []
  assert [x for x in ms.major_words(dictfile, 5)] == ['yell', 'well']
  assert [x for x in ms.major_words(dictfile, "17")] == ["dog", 'tag']
  assert [x for x in ms.major_words(dictfile, "175")] == ["toggle"]
  assert [x for x in ms.major_words(dictfile, "8")] == []
  assert [x for x in ms.major_words(dictfile, "5")] == ['yell', 'well']
  assert [x for x in ms.major_words(dictfile, "05")] == ['sail', 'sole', 'seal']


def test_phrases_from_partition(dictfile):
  partitions = [[175], [17, 5], [1, 75], [1, 7, 5], [15], [7], [1, 5], [1],
      [5],]
  expected_phrases_list = [
    ['toggle'],
    ['dog yell', 'dog well', 'tag yell', 'tag well'],
    ['at gill', 'at gal', 'what gill', 'what gal'],
    ['at ick yell', 'at ick well', 'what ick yell', 'what ick well'],
    ['tall', 'deal'],
    ['ick'],
    ['at yell', 'at well', 'what yell', 'what well'],
    ['at', 'what'],
    ['yell', 'well'],
  ]
  for partition, expected_phrases in zip(partitions, expected_phrases_list):
    phrases = [x for x in ms.phrases_from_partition(dictfile, partition)]
    assert phrases == expected_phrases
    as_strings = [str(x) for x in partition]
    phrases = [x for x in ms.phrases_from_partition(dictfile, as_strings)]
    assert phrases == expected_phrases


def test_arpabet_matches():
  assert not ms.arpabet_matches("17", ['D', 'AO1', 'G', 'Z'])
  assert ms.arpabet_matches("17", ['D', 'AO1', 'G'])
  assert ms.arpabet_matches("56201", ['IH2', 'L', 'UW1', 'ZH', 'AH0', 'N', 'AH0', 'S', 'T'])
  assert not ms.arpabet_matches("56201", ['IH2', 'L', 'UW1', 'ZH', 'AH0', 'N', 'AH0', 'S', 'T', 'S'])
  assert ms.arpabet_matches("17", ['D', 'AH0', 'G'])
  assert not ms.arpabet_matches("171", ['D', 'AH0', 'G'])


def test_phrases(dictfile):
  for fifteen in [15, '15']:
    phrases = [x for x in ms.phrases(dictfile, fifteen)]
    assert phrases == [
      'tall', 'deal', 'at yell', 'at well', 'what yell', 'what well'
    ]
  
  for one75 in [175, '175']:
    phrases = [x for x in ms.phrases(dictfile, one75)]
    assert set(phrases) == set([
      'toggle',
      'dog yell', 'dog well', 'tag yell', 'tag well',
      'at gill', 'at gal', 'what gill', 'what gal',
      'at ick yell', 'at ick well', 'what ick yell',
      'what ick well',
    ])

  for fifteen in [15, '15']:
    phrases = [x for x in ms.phrases(dictfile, fifteen, 1)]
    assert phrases == [
      'tall', 'deal',
    ]

  for one75 in [175, '175']:
    phrases = [x for x in ms.phrases(dictfile, one75, 3)]
    assert set(phrases) == set([
      'toggle',
      'dog yell', 'dog well', 'tag yell', 'tag well',
      'at gill', 'at gal', 'what gill', 'what gal',
      'at ick yell', 'at ick well', 'what ick yell',
      'what ick well',
    ])
    phrases = [x for x in ms.phrases(dictfile, one75, 2)]
    assert set(phrases) == set([
      'toggle',
      'dog yell', 'dog well', 'tag yell', 'tag well',
      'at gill', 'at gal', 'what gill', 'what gal',
    ])
    phrases = [x for x in ms.phrases(dictfile, one75, 1)]
    assert set(phrases) == set([
      'toggle',
    ])
    phrases = [x for x in ms.phrases(dictfile, one75, 0)]
    assert set(phrases) == set([
    ])

    phrases = [x for x in ms.phrases(dictfile, "705")]
    assert set(phrases) == set([
      'ick sail', 'ick sole', 'ick seal'
    ])
