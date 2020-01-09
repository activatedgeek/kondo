from kondo.utils import exhaust_dict, to_argv, Nop


def test_empty():
  assert len(list(exhaust_dict({}))) == 0


def test_lists():
  test_dict = dict(
      x=[1, 2, 3],
      xten=[10, 20, 30],
      y=['a', 'b', 'c', 'd']
  )

  trials = list(exhaust_dict(test_dict))

  combs = 1
  for _, v in test_dict.items():
    combs = combs * len(v)

  assert len(trials) == combs

  assert test_dict.keys() == trials[0].keys()


def test_scalar_vals():
  test_dict = dict(
      x=[1, 2, 3],
      xten=[10, 20, 30],
      y=['a', 'b', 'c', 'd'],
      five=5,
      nine='9',
      two=2.0
  )

  trials = list(exhaust_dict(test_dict))

  combs = 1
  for _, v in test_dict.items():
    if isinstance(v, list):
      combs = combs * len(v)

  assert len(trials) == combs

  assert test_dict.keys() == trials[0].keys()


def test_nop():
  nop = Nop()

  nop.any_attr = 2
  nop.any_method()


def test_argv():
  trial = {
      'foo': 1,
      'bar': 'something',
      'foobar': True,
      'blah': None
  }

  argv = to_argv(trial)
  str_argv = ' '.join(argv)

  assert str_argv == '--foo=1 --bar=something --foobar'
  assert '--blah' not in str_argv

  assert '--foo=1' in argv
  assert '--bar=something' in argv
  assert '--foobar' in argv
  assert '--blah' not in argv


def test_argv2():
  trial = {
      'foo': 1,
      'bar': 'something',
      'foobar': False,
      'blah': None
  }

  argv = to_argv(trial)
  str_argv = ' '.join(argv)

  assert '--foobar' not in str_argv
  assert '--foobar' not in argv
