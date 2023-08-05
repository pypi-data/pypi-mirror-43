
from dlpipeline.utilities.dlp_base import DLPBase


class DLPAugmentor(DLPBase):
  def __init__(self, *, default_do_augmentation=True, **kwargs):
    self._do_augment = default_do_augmentation

  def apply(self, arg_data, **kwargs) -> dict:
    if self._do_augment:
      return self.pipeline_function(arg_data, **kwargs)

    return {'data': arg_data}

  def build(self, **kwargs):
    pass

  @property
  def do_augment(self):
    return self._do_augment

  @do_augment.setter
  def do_augment(self, value):
    self._do_augment = value
