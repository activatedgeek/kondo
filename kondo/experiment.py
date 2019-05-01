import os
import random
from ruamel import yaml
from typing import Optional, Union, List, Tuple
import numpy as np
import torch
from torch.utils.tensorboard import SummaryWriter

from .hparams import HParams

class Nop:
  """A NOP class. Give it anything."""
  def nop(self, *args, **kwargs):
    pass

  def __getattr__(self, _):
    return self.nop


class Experiment:
  def __init__(self,
               name: Optional[str] = None,
               seed: Optional[int] = None,
               cuda: bool = True,
               log_dir: Optional[str] = None,
               log_int: int = 100,
               ckpt_int: int = 100):

    self.name = name
    self.seed = self._set_seeds(seed)

    self.cuda = bool(cuda) and torch.cuda.is_available()
    self.dev = torch.device('cuda' if self.cuda else 'cpu')

    self._logging = self._prep_workspace(log_dir, log_int, ckpt_int)
    self._init_logger()

  def run():
    raise NotImplementedError

  @classmethod
  def generate(exp_cls, trials_dir: str):
    hparams = HParams(exp_cls)
    hparams.save_trials(trials_dir)

  @classmethod
  def load(exp_cls, trial_file: str, run: bool = False):
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
  def spec_list() -> List[Tuple[str, int, dict]]:
    '''
    A list of tuples contains group string, number of
    trials, config dictionary. See examples.
    '''
    raise NotImplementedError

  @property
  def log_dir(self) -> Optional[str]:
    return self._logging.get('log_dir')

  @property
  def log_interval(self) -> int:
    return self._logging.get('log_int')

  @property
  def ckpt_interval(self) -> int:
    return self._logging.get('ckpt_int')

  @property
  def tb(self) -> Union[SummaryWriter, Nop]:
    return self._logging.get('tb', Nop())

  def _set_seeds(self, seed: Optional[int]) -> Optional[int]:
    if seed:
      torch.manual_seed(seed)
      torch.cuda.manual_seed_all(seed)
      np.random.seed(seed)
      random.seed(seed)
    return seed

  def _init_logger(self):
    if self.log_dir:
      self._logging['tb'] = SummaryWriter(self.log_dir)

  def _prep_workspace(self, log_dir: str, log_int: int = 100, ckpt_int: int = 100) -> dict:
    logging = {
      'log_int': log_int,
      'ckpt_int': ckpt_int,
    }

    if log_dir:
      log_dir = os.path.abspath(log_dir)
      logging['log_dir'] = log_dir

      os.makedirs(logging['log_dir'], exist_ok=True)

    return logging
