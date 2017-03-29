import sciunit
import quantities as pq
#from neuronunit.capabilities import ProvidesLayerInfo
from hbp_validation_framework.versioning import Versioned

#class testColumn(sciunit.Model, ProvidesLayerInfo, Versioned):
class testColumn(sciunit.Model, Versioned):
    id = "9ade6831-a758-42be-a50e-d5cb65859c34"

    def __init__(self, name="testColumn", layer_info={}):
        self.layer_info = layer_info
        sciunit.Model.__init__(self, name=name)
        self.name = name
        self.description = "Dummy model for testing layer heights"
        self.set_layer_info_default()

    def set_layer_info(self, layer_info):
        self.layer_info = layer_info

    def set_layer_info_default(self):
        self.layer_info = { "Layer 1": {'height': {'value':'165 um'}},
                    "Layer 2": {'height': {'value':'149 um'}},
                    "Layer 3": {'height': {'value':'353 um'}},
                    "Layer 4": {'height': {'value':'190 um'}},
                    "Layer 5": {'height': {'value':'525 um'}},
                    "Layer 6": {'height': {'value':'700 um'}} }

    def get_layer_info(self):
        return self.layer_info
