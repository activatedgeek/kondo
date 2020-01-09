import os
from ax.service.ax_client import AxClient
from ax.storage.sqa_store.structs import DBSettings
from ax.core.types import TParameterization
from ax.storage.sqa_store.db import init_engine_and_session_factory, get_engine, create_all_tables
from typing import Optional, List, Generator, Tuple


class ParamSpec:
  '''Parameter spec to generate trials.

  This class uses the Adaptive Experimentation Platform (ax.dev)
  under the hood to run BayesOpt for parameter tuning. It relies
  on an SQLite based storage backend for generation and result
  reporting. Each trial is assigned an ID for lookup later.
  '''
  def __init__(self, name: str, db_path: str,
               parameters: Optional[List[TParameterization]] = None):
    if not os.path.isfile(db_path):
      init_engine_and_session_factory(url=f'sqlite:///{db_path}')
      create_all_tables(get_engine())

    self.name = name
    self.ax = AxClient(enforce_sequential_optimization=False,
                       verbose_logging=False,
                       db_settings=DBSettings(url=f'sqlite:///{db_path}'))

    if self.ax._experiment is None:
      try:
        self.ax.create_experiment(name=name, parameters=parameters)
      except ValueError:
        self.ax.load_experiment_from_database(name)

  @property
  def experiment(self):
    return self.ax.experiment

  def generate_trials(self, n: int = 1) \
    -> Generator[Tuple[dict, int], None, None]:
    for _ in range(n):
      yield self.ax.get_next_trial()
