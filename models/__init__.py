import sciunit
import quantities as pq
from hbp_validation_framework.versioning import Versioned

class testCell(sciunit.Model, ProvidesLayerInfo, Versioned):
    id = "#####"

    def __init__(self, name="testCell", layer_info=[]):
        self.layer_info = layer_info
        sciunit.Model.__init__(self, name=name)
        self.name = name
        self.description = "Dummy cell for testing layer heights"

    def set_layer_info(self, layer_info):
        self.layer_info = layer_info

    def set_layer_info_default(self):
        self.layer_info = [ ["layer I", 150.0*pq.um],
                            ["layer II-III", 300.0*pq.um],
                            ["layer IV", 250.0*pq.um],
                            ["layer V", 425.0*pq.um],
                            ["layer VI", 675.0*pq.um] ]

    def get_layer_info(self):
        return self.layer_info
