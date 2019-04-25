import os
from kondo import Experiment, HParams, RandIntType, ChoiceType


class MyExp(Experiment):
  def __init__(self, foo=100, bar='c', **kwargs):
    super().__init__(**kwargs)
    self.foo = foo
    self.bar = bar

  def run(self):
    print('Running experiment with foo={}, bar="{}".'.format(self.foo, self.bar))


if __name__ == "__main__":
  spec = dict(
    foo=RandIntType(low=10, high=100),
    bar=ChoiceType(['a', 'b', 'c']),
  )
  
  hparams = HParams(MyExp, spec)

  trials_dir = os.path.join(os.path.dirname(__file__), '.trials')
  hparams.save_trials(trials_dir, num=3)

  for fname in os.listdir(trials_dir):
    fname = os.path.join(trials_dir, fname)
    trial = MyExp.load(fname)
    trial.run()
