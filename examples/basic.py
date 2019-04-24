from kondo import Experiment, HParams, RandIntType, ChoiceType


class MyExp(Experiment):
  def __init__(self, foo=100, bar='c', **kwargs):
    super(MyExp, self).__init__(**kwargs)
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

  for trial in hparams.trials(num=3):
    exp = MyExp(**trial)
    exp.run()
