"""
Main script for running vaidation tests of hippocampus CA1 pyramidal neuron models

Author: Andrew P. Davison, CNRS
Date: February 2017
"""

import argparse
from datetime import datetime
from hbp_validation_framework import ValidationTestLibrary
from hbp_validation_framework.datastores import CollabDataStore
import models

parser = argparse.ArgumentParser()
parser.add_argument("model",
                    help="name of the model to test, e.g. Bianchi, Golding, KaliFreund or Migliore"),
parser.add_argument("test",
                    help="test configuration file (local path or URL)")
config = parser.parse_args()

# Load the model
model = getattr(models, config.model)()
print "----------------------------------------------"
print "Model name: ", model
print "----------------------------------------------"

# Load the test
# checks the test is registered with the Validation framework,
# if it is not, fail with instructions for registering,
# or offer to register it
# test_library = ValidationTestLibrary() # default url for HBP service
test_library = ValidationTestLibrary(username="shailesh") # default url for HBP service
test = test_library.get_validation_test(config.test)
print "----------------------------------------------"
print "Test name: ", test
print "----------------------------------------------"

# Run the test
score = test.judge(model, deep_error=True)
print "-----------------------"
print "Score: ", score
print "-----------------------"

# Register the result with the HBP Validation service
# This could be integrated into test.judge() if we extend sciunit appropriately
collab_folder = "{}_{}".format(config.model, datetime.now().strftime("%Y%m%d-%H%M%S"))
collab_storage = CollabDataStore(username="shailesh",
                                 collab_id="1771",
                                 base_folder=collab_folder)
#test_library.register(score, collab_storage)  # score already linked to test and model (I think)
test_library.register(score)
