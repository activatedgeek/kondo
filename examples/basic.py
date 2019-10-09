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

  print('Generate trials online...')
  for name, trial in hparams.trials():
    exp = MyExp(**trial)

    print('Auto generated CLI args for', name, ':',
          ' '.join(hparams.to_argv(trial)))

    exp.run()

  print()

  print('Generate only "fixed_foo" trials online...')
  for _, trial in hparams.trials(groups=['fixed_foo']):
    exp = MyExp(**trial)
    exp.run()
