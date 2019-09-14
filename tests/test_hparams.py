from kondo import HParams
from . import Experimental

def test_hparams():
  hparams = HParams(Experimental)

  for param in ['foo', 'bar', 'foobar']:
    assert param in hparams.hparams
