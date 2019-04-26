import os
import random
from ruamel import yaml
import numpy as np
import torch
from tensorboardX import SummaryWriter

from .hparams import HParams

class Nop:
  """A NOP class. Give it anything."""
  def nop(self, *args, **kwargs):
    pass

  def __getattr__(self, _):
    return self.nop


class Experiment:
  def __init__(self,
               name=None,
               seed=None,
               cuda=True,
               log_dir=None,
               log_int=100,
               ckpt_int=100):

    self.name = name
    self.seed = self._set_seeds(seed)

    self.cuda = bool(cuda) and torch.cuda.is_available()
    self.dev = torch.device('cuda' if self.cuda else 'cpu')

    self._logging = self._prep_workspace(log_dir, log_int, ckpt_int)
    self._init_logger()

  def run():
    raise NotImplementedError

  @classmethod
  def generate(exp_cls, trials_dir, n_trials=0):
    if n_trials:
      hparams = HParams(exp_cls)
      hparams.save_trials(trials_dir, num=n_trials)

  @classmethod
  def load(exp_cls, trial_file, run=False):
    with open(trial_file, 'r') as f:
      trial = yaml.safe_load(f)
    
    try:
      group = trial.pop('group')
    except KeyError:
      group = None

    if not run:
      return trial, group

    exp = exp_cls(**trial)
    exp.run()

  @staticmethod
  def spec_list():
    # return []
    raise NotImplementedError

  @property
  def log_dir(self):
    return self._logging.get('log_dir')

  @property
  def log_interval(self):
    return self._logging.get('log_int')

  @property
  def ckpt_interval(self):
    return self._logging.get('ckpt_int')

  @property
  def tb(self):
    return self._logging.get('tb', Nop())

  def _set_seeds(self, seed):
    if seed:
      torch.manual_seed(seed)
      torch.cuda.manual_seed_all(seed)
      np.random.seed(seed)
      random.seed(seed)
    return seed

  def _init_logger(self):
    if self.log_dir:
      self._logging['tb'] = SummaryWriter(self.log_dir)

  def _prep_workspace(self, log_dir, log_int=100, ckpt_int=100):
    logging = {
      'log_int': log_int,
      'ckpt_int': ckpt_int,
    }

    if log_dir:
      log_dir = os.path.abspath(log_dir)
      logging['log_dir'] = log_dir

      os.makedirs(logging['log_dir'], exist_ok=True)

    return logging
