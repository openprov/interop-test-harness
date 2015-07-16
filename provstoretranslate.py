import json
import os.path
import requests
import shutil
import sys

from prov_interop import standards
from prov_interop.component import ConfigError
from prov_interop.converter import ConversionError
from prov_interop.provstore.converter import ProvStoreConverter
from prov_interop.provtranslator.converter import ProvTranslatorConverter

def create_dir(d):
    if os.path.isdir(d):
        shutil.rmtree(d)
    os.mkdir(d)

api_key = sys.argv[1]
in_file = "testcase1.json"
if (len(sys.argv)) > 2:
    in_file = sys.argv[2]

translator = ProvTranslatorConverter()
config={
    "url": "https://provenance.ecs.soton.ac.uk/validator/provapi/documents/",
    "input-formats": ["provn", "ttl", "trig", "provx", "json"],
    "output-formats": ["provn", "ttl", "trig", "provx", "json"]}
translator.configure(config)

store = ProvStoreConverter()
config={
    "url": "https://provenance.ecs.soton.ac.uk/store/api/v0/documents/",
    "api-key": api_key,
    "input-formats": ["provn", "ttl", "trig", "provx", "json"],
    "output-formats": ["provn", "ttl", "trig", "provx", "json"]}
store.configure(config)

converters = {"ProvTranslator": translator,
              "ProvStore": store}

outputs = "outputs"
create_dir(outputs)

# Convert in_file into every type of output document.
print("Running conversions from " + in_file)
for c in converters:
    print(c)
    converter = converters[c]
    for f in standards.FORMATS:
        print(" " + f)
        out_file = os.path.join(outputs, c + "." + f)
        converter.convert(in_file, out_file)

derived_outputs = "derived_outputs"
create_dir(derived_outputs)

# Convert every output from above into every type of output document.
# Include using ProvStore on ProvTranslator outputs and vice-versa.
for c in converters:
    print("Running conversions from " + outputs + " using " + c)
    converter = converters[c]
    for f in os.listdir(outputs):
        for out in standards.FORMATS:
            in_file = os.path.join(outputs, f)
            out_file = os.path.join(derived_outputs, f + "." + c + "." + out)
            try:
                converter.convert(in_file, out_file)
            except Exception as e:
                print("Problem from " + in_file + " to " + out_file)
                print(e)
