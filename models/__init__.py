import sciunit
import quantities as pq
from neuronunit.capabilities import ProvidesLayerInfo
from hbp_validation_framework.versioning import Versioned

class testCell(sciunit.Model, ProvidesLayerInfo, Versioned):
    id = "9ade6831-a758-42be-a50e-d5cb65859c34"

    def __init__(self, name="testCell", layer_info={}):
        self.layer_info = layer_info
        sciunit.Model.__init__(self, name=name)
        self.name = name
        self.description = "Dummy cell for testing layer heights"
        self.set_layer_info_default()

    def set_layer_info(self, layer_info):
        self.layer_info = layer_info

    def set_layer_info_default(self):
        self.layer_info = { "layer_I": {'height': {'value':'150 um'}},
                            "layer_II-III": {'height': {'value':'300 um'}},
                            "layer_IV": {'height': {'value':'250 um'}},
                            "layer_V": {'height': {'value':'425 um'}},
                            "layer_VI": {'height': {'value':'675 um'}} }

    def get_layer_info(self):
        return self.layer_info
