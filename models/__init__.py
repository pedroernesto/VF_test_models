import sciunit
import os
import json

from datetime import datetime

# ==============================================================================


class hippoCircuit(sciunit.Model):

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
    
# ==============================================================================

# class neuroM_loader(sciunit.Model, cap.HandlesNeuroM, Versioned):
class neuroM_loader(sciunit.Model):

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
        
# ==============================================================================


class NeuroM_MorphStats(sciunit.Model):
    """A class to interact with morphology files via the morphometrics-NeuroM's API (morph_stats)"""

    # model_instance_uuid = "421e6a79-80b1-4d2f-8c43-b2f37bfc1cfc"  # environment="prod"
    model_instance_uuid = "cba18d6d-a60c-491d-bc8f-09114d127aac"  # environment="dev"

    def __init__(self, model_name='NeuroM_MorphStats', morph_path=None,
                 config_path=None, morph_stats_file=None, base_directory='.'):

        sciunit.Model.__init__(self, name=model_name)
        self.description = "A class to interact with morphology files via the morphometrics-NeuroM's API (morph_stats)"
        self.version = model_name

        self.morph_path = morph_path
        self.config_path = config_path

        # Defining output directory
        self.morph_stats_output = os.path.join(base_directory, 'validation_results', 'neuroM_morph_softChecks',
                                             self.version, datetime.now().strftime("%Y%m%d-%H%M%S"))

        self.output_file = os.path.join(self.morph_stats_output, morph_stats_file)

        self.morph_feature_info = self.set_morph_feature_info()

    def set_morph_feature_info(self):
        """
        Must return a dictionary of the form:
        {"cell1_ID": { 'cell_part_1': {'morph_feature_name_11': {'value': 'X11 units_str'},
                                       'morph_feature_name_12': {'value': 'X12 units_str'},
                                        ... },
                       'cell_part_2': {'morph_feature_name_21': {'value': 'X21 units_str'},
                                       'morph_feature_name_22': {'value': 'X22 units_str'},
                                        ... },
                       ... }
         "cell2_ID": { 'cell_part_1': {'morph_feature_name_11': {'value': 'Y11 units_str'},
                                       'morph_feature_name_12': {'value': 'Y12 units_str'},
                                        ... },
                       'cell_part_2': {'morph_feature_name_21': {'value': 'Y21 units_str'},
                                       'morph_feature_name_22': {'value': 'Y22 units_str'},
                                        ... },
                       ... }
        ... }
        """

        # create output directory
        if not os.path.exists(self.morph_stats_output):
            os.makedirs(self.morph_stats_output)

        try:
            os.system('morph_stats -C {} -o {} {}'.format(self.config_path, self.output_file, self.morph_path))
        except IOError:
            print "Please specify the paths to the morphology directory and configuration file for morph_stats"

        # Correcting cell's ID, given by some neuroM versions:
        # omitting enclosing directory's name  and file's extension
        with open(self.output_file, 'r') as fp:
            mod_prediction = json.load(fp)
        for key0, dict0 in mod_prediction.items():  # Dict. with cell's morph_path-features dict. pairs for each cell
            cell_ID = (key0.split("/")[-1]).split(".")[0]
            del mod_prediction[key0]
            mod_prediction.update({cell_ID: dict0})

        # Saving NeuroM's morph_stats output in a formatted json-file
        with open(self.output_file, 'w') as fp:
            json.dump(mod_prediction, fp, sort_keys=True, indent=4)

        return mod_prediction

    def get_morph_feature_info(self):
        return self.morph_feature_info

