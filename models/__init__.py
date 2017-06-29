import sciunit
import quantities as pq
#from neuronunit.capabilities import ProvidesLayerInfo
from hbp_validation_framework.versioning import Versioned
#import morphounit.capabilities as cap

#==============================================================================

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

#==============================================================================

#class hippoCircuit(sciunit.Model, cap.ProvidesDensityInfo, Versioned):
class hippoCircuit(sciunit.Model, Versioned):
        id = "f25d05b2-2358-418b-8914-fe02a412ac74"

        def __init__(self, name="hippoCircuit", density_info={}):
            self.density_info = density_info
            sciunit.Model.__init__(self, name=name)
            self.name = name
            self.description = "Dummy model for testing cell densities"
            self.set_density_info_default()

        def set_density_info_default(self):
            self.density_info = { "density" : {"value" : "200 1000/mm3"}}

        def get_density_info(self):
            return self.density_info

#==============================================================================

#class neuroM_loader(sciunit.Model, cap.HandlesNeuroM, Versioned):
class neuroM_loader(sciunit.Model, Versioned):
        id = "3957bc1c-4a22-40ca-9ad6-879f75403219"

        def __init__(self, name="neuroM_loader", soma_diameter={}):
            self.soma_diameter = soma_diameter
            sciunit.Model.__init__(self, name=name)
            self.name = name
            self.description = "Model for loading morphologies via NeuroM"
            self.set_soma_diameter_info()

        def set_soma_diameter_info(self):
            import neurom as nm
            # remove hardcoding
            morph_path = '/home/shailesh/Work/NeuroM/1-1-DE-rep-ax-cor.swc'
            nrn = nm.load_neuron(morph_path)
            soma_radius = nm.get('soma_radii', nrn, neurite_type=nm.SOMA)
            value = str(soma_radius[0]*2) + " um"
            self.soma_diameter = { "diameter" : {"value" : value}}

        def get_soma_diameter_info(self):
            return self.soma_diameter

#==============================================================================
