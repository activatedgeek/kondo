import os
import glob
from kondo import Spec, Experiment, HParams
from kondo import ChoiceType, RandIntType, UniformType, NormalType


class Experimental(Experiment):
  def __init__(self, foo=100, bar='c', foobar=0., **kwargs):
    super().__init__(**kwargs)
    self.foo = foo
    self.bar = bar
    self.foobar = foobar

  def run(self):
    # Do some real stuff here?
    pass

  @staticmethod
  def spec_list():
    return [
        Spec(
            group='random',
            params=dict(
                foo=RandIntType(low=10, high=100),
                bar=ChoiceType(['a', 'b', 'c']),
                foobar=2.0,
            ),
            n_trials=2,
        ),
        Spec(
            group='fixed_foo',
            params=dict(
                foo=200,
                bar=ChoiceType(['a', 'b', 'c'])
            ),
            n_trials=3,
        ),
        Spec(
            group='limited_foobar',
            params=dict(
                foobar=UniformType(low=3.0, high=4.0),
            ),
            n_trials=4,
        ),
    ]
