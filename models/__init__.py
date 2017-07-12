import sciunit
from hbp_validation_framework.versioning import Versioned

#==============================================================================

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

#==============================================================================

class hippoCircuit(sciunit.Model, Versioned):
        id = "f25d05b2-2358-418b-8914-fe02a412ac74"

        def __init__(self, name="hippoCircuit", density_info={}):
            self.density_info = density_info
            sciunit.Model.__init__(self, name=name)
            self.name = name
            self.description = "Dummy model for testing cell densities"
            self.set_density_info_default()

        def set_density_info_default(self):
            self.density_info = { "density" : {"value" : "200 1/mm**3"}}

        def get_density_info(self):
            return self.density_info

#==============================================================================

class NeuroM_NeuriteLength(sciunit.Model, Versioned):

    id = ""

    def __init__(self, name='NeuriteLength', NeuriteLength_info={}):
        sciunit.Model.__init__(self, name=name)
        self.name = name
        self.description = "Dummy model for testing neurite length"
        self.set_NeuriteLength_info()
        self.set_NeuriteLength_info_default()

    def set_NeuriteLength_info(self):
        self.NeuriteLength_info = NeuriteLength_info

    def set_NeuriteLength_info_default(self):
        self.NeuriteLength_info = { 'NeuriteLength': {'mean': '50 um', 'std': '4 um'} }

    def get_NeuriteLength_info(self):
        return self.neuriteLength_info

#==============================================================================
