import json
import os

from .validator import KomandPluginValidator


class JSONValidator(KomandPluginValidator):
    invalid_files = []

    def validate(self, spec):
        tests_dir = os.path.join(spec.directory, "tests")
        for path, _, files in os.walk(tests_dir):
            for name in files:
                if name.endswith(".json"):
                    with open(os.path.join(tests_dir, name)) as test:
                        try:
                            json.load(test)
                        except json.decoder.JSONDecodeError:
                            JSONValidator.invalid_files.append(name)
        if len(JSONValidator.invalid_files) > 0:
            raise Exception(f"The following test files are not in proper JSON format: {JSONValidator.invalid_files}")
