import os
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
            self.density_info = { "density" : {"value" : "200 1000/mm3"}}

        def get_density_info(self):
            return self.density_info
    
#==============================================================================

#class neuroM_loader(sciunit.Model, cap.HandlesNeuroM, Versioned):
class neuroM_loader(sciunit.Model, Versioned):
        id = "3957bc1c-4a22-40ca-9ad6-879f75403219"

        def __init__(self, name="neuroM_loader", model_path=None, soma_diameter={}):
            self.soma_diameter = soma_diameter
            sciunit.Model.__init__(self, name=name)
            self.name = name
            self.description = "Model for loading morphologies via NeuroM"
            if model_path == None:
                print "Please specify the path to the morphology file or the directory as the last parameter!"
                print "Example Syntax1: python run_tests.py neuroM_loader https://validation.brainsimulation.eu/tests/7 ./files/1-1-DE-rep-ax-cor.swc"
                print "Example Syntax2: python run_tests.py neuroM_loader https://validation.brainsimulation.eu/tests/7 ./files"
                quit()
            if os.path.isdir(model_path):
                print "Directory"
                quit()
            self.morph_path = model_path
            self.set_soma_diameter_info()

        def set_soma_diameter_info(self):
            import neurom as nm
            nrn = nm.load_neuron(self.morph_path)
            soma_radius = nm.get('soma_radii', nrn, neurite_type=nm.SOMA)
            value = str(soma_radius[0]*2) + " um"
            self.soma_diameter = { "diameter" : {"value" : value}}

        def get_soma_diameter_info(self):
            return self.soma_diameter
        
#==============================================================================

class NeuroM_NeuriteLength(sciunit.Model, Versioned):

    id = "afc85429-0db2-4414-8fc7-3ed5781a5019"

    def __init__(self, name='NeuriteLength', model_path=None, cell_part=None,
                 cell_feature_name='terminal_path_lengths_per_neurite', NeuriteLength_info={}):

        sciunit.Model.__init__(self, name=name)
        self.name = name
        self.description = "Model for testing neurite (euclidean) length"
        self.NeuriteLength_info = NeuriteLength_info

        if model_path == None:
            print "Please specify the path to the morphology file or the directory"
            quit()
        if os.path.isdir(model_path):
            print "Directory"
            quit()

        if cell_part not in ['SOMA', 'AXON', 'APICAL_DENDRITE', 'BASAL_DENDRITE']:
            print "Please, specify a valid cell part: 'SOMA', 'AXON', 'APICAL_DENDRITE', 'BASAL_DENDRITE'"
            quit()

        self.morph_path = model_path
        self.cell_part = cell_part
        self.cell_feature_name = cell_feature_name
        self.set_NeuriteLength_info()

    def set_NeuriteLength_info(self):
        import neurom as nm
        nrn = nm.load_neuron(self.morph_path)
        feature_value = nm.get(self.cell_feature_name, nrn, neurite_type=eval('nm.'+self.cell_part))
        self.NeuriteLength_info = feature_value

    def get_NeuriteLength_info(self):
        return self.NeuriteLength_info

#==============================================================================

class CA1Layers_NeuritePathDistance(sciunit.Model, Versioned):

    id = "bb06ab0a-685c-4f0f-b078-195cd947639f"

    def __init__(self, name='CA1Layers_NeuritePathDistance', CA1LayersNeuritePathDistance_info={}):
        self.CA1LayersNeuritePathDistance_info = CA1LayersNeuritePathDistance_info
        sciunit.Model.__init__(self, name=name)
        self.name = name
        self.description = "Dummy model to test neurite path-distances across CA1 layers"
        self.set_CA1LayersNeuritePathDistance_info_default()

    def set_CA1LayersNeuritePathDistance_info_default(self):
        self.CA1LayersNeuritePathDistance_info = { "SLM": {'PathDistance': {'value':'120 um'}},
						    "SR": {'PathDistance': {'value':'280 um'}},
						    "SP": {'PathDistance': {'value':'40 um'}},
						    "SO": {'PathDistance': {'value':'100 um'}}
						  }

    def get_CA1LayersNeuritePathDistance_info(self):
        return self.CA1LayersNeuritePathDistance_info

#==============================================================================

class CA1_laminar_distribution_synapses(sciunit.Model, Versioned):

    id = ""
    version = "Project42-EPFL-v0.1"

    import bluepy
    from bluepy.v2.enums import Synapse
    from voxcell import VoxelData, RegionMap

    import json

    def __init__(self, name="CA1_laminar_distribution_synapses", CA1_laminar_distribution_synapses_info={}):

	'''
	# Model releases on Julia/Juron clusters
	circuit_path = '/work/pra098/pra09801/CircuitRelease/r2017.06b/CircuitConfig'
	volume_path = '/work/pra098/pra09801/CircuitRelease/r2017.06b/volume/volume.nrrd'
	hierarchy_path = '/work/pra098/pra09801/CircuitRelease/r2017.06b/volume/hierarchy.json'

        self.circuit = bluepy.Circuit(circuit_path)
        self.annotation = VoxelData.load_nrrd(volume_path)
        self.region_map = RegionMap.from_json(hierarchy_path)
	'''

        sciunit.Model.__init__(self, name=name)
        self.name = name
        self.description = "HBP Hippocampus's output to test synapses distribution across CA1 layers"
	self.CA1_laminar_distribution_synapses_info = CA1_laminar_distribution_synapses_info
        self.set_CA1_laminar_distribution_synapses_info_default()


    def set_CA1_laminar_distribution_synapses_info_default(self):
        model_prediction_path = "./model_predictions/CA1_laminar_distribution_synapses_HBPmod.json" 
	json_data=open(model_prediction_path).read()
        self.CA1_laminar_distribution_synapses_info = json.loads(json_data)


    def get_CA1_laminar_distribution_synapses_info(self):
        return self.CA1_laminar_distribution_synapses_info

