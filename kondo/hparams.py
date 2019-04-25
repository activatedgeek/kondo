import os
import inspect
from ruamel import yaml

from .param_types import ParamType


class HParams:
  def __init__(self, exp_class, spec):
    self._hparams = self.prep(exp_class)
    self._spec = spec

  @property
  def hparams(self):
    return self._hparams

  @staticmethod
  def prep(cls):
    attribs = {}

    for sup_c in type.mro(cls)[::-1]:
      argspec = inspect.getargspec(getattr(sup_c, '__init__'))
      argsdict = dict(dict(zip(argspec.args[1:], argspec.defaults or [])))
      attribs = {**attribs, **argsdict}
    
    return attribs

  def sample(self):
    for trial in self.trials():
      return trial

  def trials(self, num=1):
    rvs = {
      k: v.sample(size=num).tolist() if isinstance(v, ParamType) else v
      for k, v in self._spec.items()
    }

    for t in range(num):
      t_rvs = {k: v[t] if isinstance(v, list) else v
               for k, v in rvs.items()}

      yield {**self._hparams, **t_rvs}

  def save_trials(self, trial_dir, num=1):
    os.makedirs(trial_dir, exist_ok=True)
    for i, trial in enumerate(self.trials(num=num)):
      with open(os.path.join(trial_dir, '{}.yaml'.format(i)), 'w') as f:
        yaml.safe_dump(trial, stream=f,
                       default_flow_style=False)