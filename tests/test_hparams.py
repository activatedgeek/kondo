from kondo import HParams
from . import Experimental

def test_hparams():
  hparams = HParams(Experimental)

  for param in ['foo', 'bar', 'foobar']:
    assert param in hparams.hparams


def test_argv():
  trial = {
      'foo': 1,
      'bar': 'something',
      'foobar': False,
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
