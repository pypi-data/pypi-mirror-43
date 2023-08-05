import json


class ManifestReader:
    '''Reads manifest file'''

    def __init__(self, manifest_data, logger):
        self._manifest_data = manifest_data
        self._logger = logger

    def get_python_layer_arn(self, region):
        if 'python-layer' not in self._manifest_data:
            self._logger.error_and_exit("Python layer not found in manifest. Please update your fsp version")

        if region is not None:
            if region not in self._manifest_data['python-layer']:
                self._logger.error_and_exit("Python layer not found for region " + str(region) + ". Please update your fsp version")
            return self._manifest_data['python-layer'][region]
        else:
            self._logger.debug("Get layers from all regions")
            return self._manifest_data['python-layer']
