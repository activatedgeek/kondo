# TODO(sanyam): Disables warnings from Tensorboard.
import warnings
warnings.filterwarnings('ignore', category=FutureWarning)

from kondo import Spec, Experiment, HParams, RandIntType, ChoiceType  # pylint: disable=wrong-import-position


class MyExp(Experiment):
  def __init__(self, foo=100, bar='c', **kwargs):
    super().__init__(**kwargs)
    self.foo = foo
    self.bar = bar

  def run(self):
    print('Running experiment with foo={}, bar="{}".'.format(self.foo,
                                                             self.bar))

  @staticmethod
  def spec_list():
    return [
        Spec(
            group='random',
            params=dict(
                seed=20,
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
  hparams = HParams(MyExp)

  print('Generating trials online...\n')
  for name, trial in hparams.trials():
    MyExp(**trial).run()
    print()

  print('Generating only "fixed_foo" trials online...\n')
  for _, trial in hparams.trials(groups=['fixed_foo']):
    MyExp(**trial).run()
    print()
