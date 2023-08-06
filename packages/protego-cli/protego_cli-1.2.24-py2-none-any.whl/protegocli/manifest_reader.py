import json


class ManifestReader:
    '''Reads manifest file'''

    def __init__(self, manifest_data, logger):
        self._manifest_data = manifest_data
        self._logger = logger

    def get_layer_arn(self, region, runtime_name):
        ret = {}

        if runtime_name is None:
            runtime_names = ["python", "nodejs"]
        else:
            runtime_names = [runtime_name]

        for r_name in runtime_names:
            runtime_key = r_name + "-layer"  # python-layer / nodejs-layer

            if runtime_key not in self._manifest_data:
                self._logger.error_and_exit(str(r_name) + " layer not found in manifest. Please update your fsp version")

            if region is not None:
                if region not in self._manifest_data[runtime_key]:
                    self._logger.error_and_exit(str(r_name) + " layer not found for region " + str(region) + ". Please update your fsp version")

                ret.setdefault(runtime_key, {})[region] = self._manifest_data[runtime_key][region]
            else:
                ret[runtime_key] = self._manifest_data[runtime_key]
        return ret
