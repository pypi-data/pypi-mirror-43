from .LazyUrlDataGetter import LazyUrlDataGetter
from .DataGetter import DataGetter


class LayersWrapper:
    """ The encapsulation of data layers
    Attributes:
        semantic_2d: a data_object.DataGetter object of sematic 2D
        dynamic_objects: a list of data_object.DataGetter objects of dynamic scenario
    """
    def __init__(self):
        self.semantic_2d = None
        self.dynamic_objects = []


class Dataset:
    """A dataset is the data unit which include different data layers.
    Attributes:
        id: identity of this dataset
        layers: layers in this dataset
    """
    def __init__(self, json_object):

        self.id = json_object["id"]
        self.layers = LayersWrapper()
        layers = json_object["layers"]
        if "semantic2D" in layers:
            self.layers.semantic_2d = DataGetter(layers["semantic2D"])
        if "dynamicObjects" in layers:
            self.dynamic_objects = []
            for dynamc_object in layers["dynamicObjects"]:
                self.layers.dynamic_objects.append(LazyUrlDataGetter(dynamc_object["url"]))

