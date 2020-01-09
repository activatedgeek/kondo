from kondo import HParams, Spec
from . import Experimental


def test_hparams():
  hparams = HParams(Experimental)

  for param in ['foo', 'bar', 'foobar']:
    assert param in hparams.hparams


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
