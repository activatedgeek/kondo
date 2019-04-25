import os
import random
from ruamel import yaml
import numpy as np
import torch
from tensorboardX import SummaryWriter


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
    self.init_logger()

  def init_logger(self):
    if self.log_dir:
      self._logging['tb'] = SummaryWriter(self.log_dir)

  @classmethod
  def load(exp_cls, config_file):
    with open(config_file, 'r') as f:
      config = yaml.safe_load(f)

    return exp_cls(**config)

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
