# TODO(sanyam): Disables warnings from Tensorboard.
import warnings
warnings.filterwarnings('ignore', category=FutureWarning)

import os
import glob
from kondo import Spec, Experiment, HParams, RandIntType, ChoiceType


class MyExp(Experiment):
  def __init__(self, foo=100, bar='c', **kwargs):
    super().__init__(**kwargs)
    self.foo = foo
    self.bar = bar

  def run(self):
    print('Running experiment with foo={}, bar="{}".'.format(self.foo, self.bar))

  @staticmethod
  def spec_list():
    return [
      Spec(
        group='random',
        params=dict(
          foo=RandIntType(low=10, high=100),
          bar=ChoiceType(['a', 'b', 'c'])
        ),
        n_trials=3,
      ),
      Spec(
        group='fixed_foo',
        params=dict(
          foo=200,
          bar=ChoiceType(['a', 'b', 'c'])
        ),
        n_trials=3,
      )
    ]

if __name__ == "__main__":
  trials_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '.trials')

  hparams = HParams(MyExp)

  print('Generate trials online and save...')
  for trial in hparams.trials(trials_dir=trials_dir):
    exp = MyExp(**trial)
    exp.run()

  print()

  print('Run pre-generated trials...')
  for fname in glob.glob('{}/**/trial.yaml'.format(trials_dir)):
    exp = MyExp.load(fname)

    exp.run()

  print()

  print('Generate only "fixed_foo" trials online...')
  for trial in hparams.trials(groups=['fixed_foo']):
    exp = MyExp(**trial)
    exp.run()
