from abc import abstractmethod


class DLPBase(object):

  def __call__(self, arg_data, **kwargs):
    return self.apply(arg_data, **kwargs)

  def apply(self, arg_data, **kwargs) -> dict:
    ret = self.pipeline_function(arg_data, **kwargs)

    assert isinstance(ret, dict)

    return ret

  @abstractmethod
  def pipeline_function(self, arg_data, **kwargs) -> dict:
    pass

  @abstractmethod
  def build(self, **kwargs):
    pass


