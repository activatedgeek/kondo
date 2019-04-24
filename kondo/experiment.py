import os
import random
import numpy as np
import torch
from tensorboardX import SummaryWriter


class Experiment:
  def __init__(self,
               name=None,
               seed=None,
               cuda=True,
               ws_dir=None,
               log_int=100,
               ckpt_int=100):

    self.name = name
    self.seed = self._set_seeds(seed)

    self.cuda = bool(cuda) and torch.cuda.is_available()
    self.dev = torch.device('cuda' if self.cuda else 'cpu')

    self._logging = self._prep_workspace(ws_dir, log_int, ckpt_int)
    self._logging['logger'] = self.init_logger()

  def init_logger(self):
    if self.log_dir:
      return SummaryWriter(self.log_dir)

  @property
  def ws_dir(self):
    return self._logging.get('ws_dir')

  @property
  def log_dir(self):
    return self._logging.get('log_dir')

  @property
  def ckpt_dir(self):
    return self._logging.get('ckpt_dir')

  @property
  def logger(self):
    return self._logging.get('logger')

  def _set_seeds(self, seed):
    if seed:
      torch.manual_seed(seed)
      torch.cuda.manual_seed_all(seed)
      np.random.seed(seed)
      random.seed(seed)
    return seed

  def _prep_workspace(self, ws_dir, log_int=100, ckpt_int=100):
    logging = {
      'log_int': log_int,
      'ckpt_int': ckpt_int,
    }

    if ws_dir:
      ws_dir = os.path.abspath(ws_dir)
      logging['ws_dir'] = ws_dir
      logging['log_dir'] = os.path.join(ws_dir, 'log')
      logging['ckpt_dir'] = os.path.join(ws_dir, 'ckpt')

      os.makedirs(logging['log_dir'], exist_ok=True)
      os.makedirs(logging['ckpt_dir'], exist_ok=True)

    return logging
