from kondo import HParams, Spec
from kondo.utils import Nop
from . import Experimental


def test_simple_attrs():
  exp = Experimental(seed=1)
  assert exp.seed == 1
  # assert not exp.cuda
  assert exp.log_dir is None
  assert isinstance(exp.logger, Nop)
  assert exp.log_interval == 100
  assert exp.ckpt_interval == 100
  assert isinstance(exp.params_acc, dict)
  assert len(exp.params_acc.keys()) == 1

  exp.params_acc = dict(newparam='newparam')

  assert len(exp.params_acc.keys()) == 2


def test_trial_count():
  hparams = HParams(Experimental)

  total_trials = sum([spec.n_trials for spec in Experimental.spec_list()])
  trial_count = 0
  for _ in hparams.trials():
    trial_count += 1

  assert trial_count == total_trials


def test_trial_unique_name():
  hparams = HParams(Experimental)

  total_trials = sum([spec.n_trials for spec in Experimental.spec_list()])
  trials = []
  for name, _ in hparams.trials():
    trials.append(name)

  assert len(set(trials)) == total_trials


def test_trial_filter():
  hparams = HParams(Experimental)

  for _, trial in hparams.trials(groups=['random']):
    assert 10 <= trial['foo'] <= 100
    assert trial['bar'] in ['a', 'b', 'c']
    assert trial['foobar'] - 2.0 < 1e-6

  for _, trial in hparams.trials(groups=['fixed_foo']):
    assert trial['foo'] == 200
    assert trial['bar'] in ['a', 'b', 'c']
    assert trial['foobar'] - 1.0 < 1e-6

  for _, trial in hparams.trials(groups=['limited_foobar']):
    assert trial['foo'] == 100
    assert trial['bar'] == 'c'
    assert 3.0 <= trial['foobar'] <= 4.0


def test_trial_ignore_filter():
  hparams = HParams(Experimental)

  for _, trial in hparams.trials(ignore_groups=['fixed_foo', 'limited_foobar']):
    assert 10 <= trial['foo'] <= 100
    assert trial['bar'] in ['a', 'b', 'c']
    assert trial['foobar'] - 2.0 < 1e-6

  for _, trial in hparams.trials(ignore_groups=['random', 'limited_foobar']):
    assert trial['foo'] == 200
    assert trial['bar'] in ['a', 'b', 'c']
    assert trial['foobar'] - 1.0 < 1e-6

  for _, trial in hparams.trials(ignore_groups=['random', 'fixed_foo']):
    assert trial['foo'] == 100
    assert trial['bar'] == 'c'
    assert 3.0 <= trial['foobar'] <= 4.0


def test_custom_spec_func():
  hparams = HParams(Experimental)

  def spec_list():
    return [
        Spec(
            group='custom',
            params=dict(
                foo=121,
                bar='e',
                foobar=2.0,
            ),
            n_trials=99,
        ),
    ]

  total_trials = sum([spec.n_trials for spec in spec_list()])
  trials = []
  for name, _ in hparams.trials(spec_func=spec_list):
    trials.append(name)

  assert len(set(trials)) == total_trials
