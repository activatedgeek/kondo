from kondo import HParams, Spec
from . import Experimental

def test_hparams():
  hparams = HParams(Experimental)

  for param in ['foo', 'bar', 'foobar']:
    assert param in hparams.hparams


def test_argv():
  trial = {
      'foo': 1,
      'bar': 'something',
      'foobar': True,
      'blah': None
  }

  argv = HParams.to_argv(trial)
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

  argv = HParams.to_argv(trial)
  str_argv = ' '.join(argv)

  assert '--foobar' not in str_argv
  assert '--foobar' not in argv


def test_exhaustive_spec():
  spec = Spec(
      group='exhaustive_spec',
      params=dict(
          foo=[1, 2, 3, 4],
          bar=['x', 'y', 'z'],
          foobar=['a', 'b', 'c'],
          const=99,
      ),
      exhaustive=True
  )

  count = 0
  for _, trial in spec.resolve():
    assert trial['const'] == 99

    count += 1

  assert count == 36
