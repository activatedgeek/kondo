import os
import time
import inspect
from ruamel import yaml

from .param_types import ParamType


class HParams:
  def __init__(self, exp_class):
    self.exp_class = exp_class
    self._hparams = self.prep(exp_class)

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
    for group, spec in self.exp_class.spec_list():
      rvs = {
        k: v.sample(size=num).tolist() if isinstance(v, ParamType) else v
        for k, v in spec.items()
      }

      for t in range(num):
        t_rvs = {k: v[t] if isinstance(v, list) else v
                for k, v in rvs.items()}

        yield {**self._hparams, **t_rvs}, group

  def save_trials(self, trials_dir, num=1):
    trials_dir = os.path.abspath(trials_dir)
    os.makedirs(trials_dir, exist_ok=True)
    for trial, group in self.trials(num=num):
      name = '{}-{}-{}'.format(self.exp_class.__name__, group, time.time())
      t_dir = os.path.join(trials_dir, name)
      
      os.makedirs(t_dir, exist_ok=True)
      with open(os.path.join(t_dir, 'trial.yaml'), 'w') as f:
        trial['name'] = name
        trial['log_dir'] = t_dir
        trial['group'] = group
        yaml.safe_dump(trial, stream=f, default_flow_style=False)
