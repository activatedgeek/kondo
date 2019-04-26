import os
import glob
from kondo import Experiment, HParams, RandIntType, ChoiceType


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
      ('example', dict(
        foo=RandIntType(low=10, high=100),
        bar=ChoiceType(['a', 'b', 'c']),
      ))
    ]

if __name__ == "__main__":
  hparams = HParams(MyExp)

  print('Generating trials online')
  for trial, _ in hparams.trials(num=3):
    exp = MyExp(**trial)
    exp.run()

  print('Saving trials to file.')
  trials_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '.trials')
  hparams.save_trials(trials_dir, num=3)

  print('Run pre-generated trials.')
  for fname in glob.glob('{}/**/trial.yaml'.format(trials_dir)):
    trial, _ = MyExp.load(fname, run=False)

    exp = MyExp(**trial)
    exp.run()
