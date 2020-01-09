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
  ])

  n = 5
  s = set()
  for _, idx in spec.generate_trials(n):
    spec.ax.complete_trial(trial_index=idx, raw_data=100.0 * random.random())
    s.add(idx)

  assert len(s) == n

  os.remove('tmp.db')
