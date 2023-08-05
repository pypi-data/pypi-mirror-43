import tensorflow_hub as hub



def get_hub_sizes(C):
  module_specification = hub.load_module_spec(C.embedding_module)
  height, width = hub.get_expected_image_size(module_specification)
  depth = hub.get_num_image_channels(module_specification)

  return {'height':height,
                     'width':width,
                     'depth':depth}