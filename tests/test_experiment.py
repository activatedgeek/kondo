from kondo import HParams
from . import Experimental


def test_trial_count():
  hparams = HParams(Experimental)

  total_trials = sum([spec.n_trials for spec in Experimental.spec_list()])
  trial_count = 0
  for _ in hparams.trials():
    trial_count += 1

  assert trial_count == total_trials


def test_trial_filter():
  hparams = HParams(Experimental)

  for trial in hparams.trials(groups=['random']):
    assert 10 <= trial['foo'] <= 100
    assert trial['bar'] in ['a', 'b', 'c']
    assert trial['foobar'] - 2.0 < 1e-6

  for trial in hparams.trials(groups=['fixed_foo']):
    assert trial['foo'] == 200
    assert trial['bar'] in ['a', 'b', 'c']
    assert trial['foobar'] - 1.0 < 1e-6

  for trial in hparams.trials(groups=['limited_foobar']):
    assert trial['foo'] == 100
    assert trial['bar'] == 'c'
    assert 3.0 <= trial['foobar'] <= 4.0


def test_trial_ignore_filter():
  hparams = HParams(Experimental)

  for trial in hparams.trials(ignore_groups=['fixed_foo', 'limited_foobar']):
    assert 10 <= trial['foo'] <= 100
    assert trial['bar'] in ['a', 'b', 'c']
    assert trial['foobar'] - 2.0 < 1e-6

  for trial in hparams.trials(ignore_groups=['random', 'limited_foobar']):
    assert trial['foo'] == 200
    assert trial['bar'] in ['a', 'b', 'c']
    assert trial['foobar'] - 1.0 < 1e-6

  for trial in hparams.trials(ignore_groups=['random', 'fixed_foo']):
    assert trial['foo'] == 100
    assert trial['bar'] == 'c'
    assert 3.0 <= trial['foobar'] <= 4.0
