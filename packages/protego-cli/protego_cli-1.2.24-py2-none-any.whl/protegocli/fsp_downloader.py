import base64
import json
import requests


class FSPDownloader:
    '''This class downloads FSP bundle'''
    FSP_URL = "https://{protegoEndpoint}.execute-api.us-east-1.amazonaws.com/{protegoEndpointStage}/protego/api/accounts/{protegoAccountId}/fsp_bundle"
    FSP_MANIFEST_FILE_NAME = "manifest.json"

    def __init__(self, protego_account_id, fsp_token, fsp_version, logger):
        self._protego_account_id = protego_account_id
        self._logger = logger
        self.fsp_version = fsp_version
        self.__parse_fsp_token(fsp_token)

    def get_manifest(self):
        contents = self.__download()
        manifest = json.loads(contents)

        self._logger.debug('Manifest file: ' + str(manifest))

        return manifest

    def __download(self):
        fsp_url = FSPDownloader.FSP_URL.format(protegoEndpoint=self._endpointAPI,
                                               protegoEndpointStage=self._stage, protegoAccountId=self._protego_account_id)

        self._logger.info("Fetching required information ...")
        params = {"manifest": True}
        if self.fsp_version is not "latest":
            params["version"] = self.fsp_version

        request = requests.get(
            fsp_url, headers={'x-protego-fsp-token': self._token}, params=params)

        if request.status_code == 404:
            self._logger.error_and_exit("Fsp version Not found (version: " + self.fsp_version + ")")
        elif request.status_code == 401:
            self._logger.error_and_exit("Invalid fsp version: " + self.fsp_version)
        elif request.status_code == 500:
            self._logger.error_and_exit("Failed to get latest FSP version.")
        elif request.status_code != 200:
            self._logger.error_and_exit("Unexpected Error. Failed to get latest FSP version.\n" + str(request.status_code) + ": " + str(request.content))

        self._logger.debug('FSP bundle fetched successfully')
        return request.content

    def __parse_fsp_token(self, fsp_token):
        decoded_fsp_token = base64.b64decode(fsp_token)
        json_token = json.loads(decoded_fsp_token)
        self._endpointAPI = json_token.get('apiId', '')
        self._stage = json_token.get('stage', '')
        self._token = json_token.get('token', '')

        self._logger.debug('Endpoint: ' + self._endpointAPI)
        self._logger.debug('Stage: ' + self._stage)
        self._logger.debug('Token: ' + self._token)
