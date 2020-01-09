import os
import random
from kondo.spec import ParamSpec


def test_paramspec():
  spec = ParamSpec('test', 'tmp.db', parameters=[
      dict(
          name="a",
          type="range",
          bounds=[1e-5, 1.0]
      ),
      dict(
          name="b",
          type="range",
          bounds=[1e-5, 1.0]
      )
  ], objective_name='result')

  n = 5
  s = set()
  for _, idx in spec.generate_trials(n):
    s.add(idx)

  results = [
      dict(id=idx, metrics=dict(result=100.0 * random.random()))
      for idx in range(n)
  ]
  spec.complete_trials(results)

  assert len(s) == n

  s = set()
  for _, idx in spec.get_trials():
    s.add(idx)

  assert len(s) == n

  os.remove('tmp.db')
