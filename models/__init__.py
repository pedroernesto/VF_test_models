import os, sys
import sciunit
from hbp_validation_framework.versioning import Versioned

import json

#==============================================================================

class hippoCircuit(sciunit.Model, Versioned):
        instance_id = "f25d05b2-2358-418b-8914-fe02a412ac74"

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
        instance_id = "3957bc1c-4a22-40ca-9ad6-879f75403219"

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

class NeuroM_MorphStats(sciunit.Model, Versioned):
    """A class to interact with morphology files via the morphometrics-NeuroM's API (morph_stats)"""

    instance_id = "afc85429-0db2-4414-8fc7-3ed5781a5019"
    # model_instance_uuid =  # prod

    def __init__(self, name='NeuroM_stats', models_path=None, config_file=None, output_file=None):

        sciunit.Model.__init__(self, name=name)
        self.description = "A class to interact with morphology files via the morphometrics-NeuroM's API (morph_stats)"
        self.name = name
        # model_path = ~/Bureau/str-fs_pv-20170919/030225-5-PV-rep-cor.swc
        self.morph_path = models_path
        self.model_pred_path = "./models/model_predictions/NeuroM_MorphStats_predictions_new.json"
        self.morph_feature_info = self.set_morph_feature_info()

    def set_morph_feature_info(self):
        """
        Must return a dictionary of the form:
        {"cell1_ID": { "cell_part_1": {"morph_feature_name_11': {'value': 'X11 some_unit'},
                                       "morph_feature_name_12': {'value': 'X12 some_unit'},
                                        ... }
                       "cell_part_2": {'morph_feature_name_21': {'value': 'X21 some_unit'},
                                       'morph_feature_name_22': {'value': 'X22 some_unit'},
                                        ... }
                       ... }
         "cell2_ID": { "cell_part_1": {"morph_feature_name_11': {'value': 'Y11 some_unit'},
                                       "morph_feature_name_12': {'value': 'Y12 some_unit'},
                                        ... }
                       "cell_part_2": {'morph_feature_name_21': {'value': 'Y21 some_unit'},
                                       'morph_feature_name_22': {'value': 'Y22 some_unit'},
                                        ... }
                       ... }
        ... }
        """

        try:
            os.system('morph_stats -C morph_stats_config.yaml ./str-fs_pv-20170919 -o '
                      './models/model_predictions/NeuroM_MorphStats_predictions_new.json')
        except IOError:
            print "Please specify the path to the morphology file or the directory"


        with open(self.model_pred_path, 'r') as fp:
            mod_prediction = json.load(fp)
        fp.close()

        # Regrouping all soma's features-values pairs into a unique 'soma' key inside mood_prediction
        for dict1 in mod_prediction.values():  # Set of cell's part-features dictionary pairs for each cell
            soma_features = dict()
            for key, val in dict1.items():
                if key.find('soma') == -1:
                    continue
                soma_features.update({key: val})
                del dict1[key]
                dict1.update({"soma": soma_features})

        # Adding the right units and converting feature values to strings
        dim_um = ['radius', 'radii', 'diameter', 'length', 'distance', 'extent']
        for dict1 in mod_prediction.values():  # Dict. with cell's part-feature dictionary pairs for each cell
            for dict2 in dict1.values():  # Dict. with feature name-value pairs for each cell part:
                                          # soma, apical_dendrite, basal_dendrite or axon
                for key, val in dict2.items():
                    if any(sub_str in key for sub_str in ['radius', 'radii']):
                        del dict2[key]
                        val *= 2
                        key = key.replace('radius', 'diameter')
                        key = key.replace('radii', 'diameter')
                    if any(sub_str in key for sub_str in dim_um):
                        dict2[key] = dict(value=str(val)+' um')
                    else:
                        dict2[key] = dict(value=str(val))

        return mod_prediction

    def get_morph_feature_info(self):
        return self.morph_feature_info

#==============================================================================

class CA1Layers_NeuritePathDistance(sciunit.Model, Versioned):

    instance_id = "bb06ab0a-685c-4f0f-b078-195cd947639f"
    # model_instance_uuid = # prod

    def __init__(self, name='CA1Layers_NeuritePathDistance', CA1LayersNeuritePathDistance_info={}):
        self.CA1LayersNeuritePathDistance_info = CA1LayersNeuritePathDistance_info
        sciunit.Model.__init__(self, name=name)
        self.name = name
        self.description = "Dummy model to test neurite path-distances across CA1 layers"
        self.set_CA1LayersNeuritePathDistance_info_default()

    def set_CA1LayersNeuritePathDistance_info_default(self):
        self.CA1LayersNeuritePathDistance_info = {"SLM": {'PathDistance': {'value':'120 um'}},
                                                  "SR": {'PathDistance': {'value':'280 um'}},
                                                  "SP": {'PathDistance': {'value':'40 um'}},
                                                  "SO": {'PathDistance': {'value':'100 um'}}
                                                 }

    def get_CA1LayersNeuritePathDistance_info(self):
        return self.CA1LayersNeuritePathDistance_info

#==============================================================================

class CA1_laminar_distribution_synapses(sciunit.Model, Versioned):

    # instance_id = "ede4c9ef-970b-4431-9f5b-cf0ca96c77e3" # dev
    model_instance_uuid = "d8f3333c-476d-4807-b433-c9fb68251514" # prod

    def __init__(self, name="CA1_laminar_distribution_synapses", CA1_laminar_distribution_synapses_info={}):

        sciunit.Model.__init__(self, name=name)
        self.name = name
        self.description = "HBP Hippocampus CA1's output to test synapses distribution across CA1 layers"
        self.CA1_laminar_distribution_synapses_info = CA1_laminar_distribution_synapses_info
        self.set_CA1_laminar_distribution_synapses_info_default()

    def set_CA1_laminar_distribution_synapses_info_default(self):
        model_prediction_path = "./models/model_predictions/CA1_laminar_distribution_synapses_HBPmod.json"
        with open(model_prediction_path, 'r') as fp:
            data = json.load(fp)
        self.CA1_laminar_distribution_synapses_info = data

    def get_CA1_laminar_distribution_synapses_info(self):
        return self.CA1_laminar_distribution_synapses_info
