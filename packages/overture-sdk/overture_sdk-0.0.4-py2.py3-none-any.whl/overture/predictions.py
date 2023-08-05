__author__ = "Dario Incalza <dario@overture.ai"
__copyright__ = "Copyright 2018, Overture"
__version__ = "0.0.1"
__maintainer__ = "Dario Incalza"
__email__ = "dario@overture.ai"

from abc import ABCMeta, abstractmethod
import requests
from overture.errors import RestApiError
import base64, json


class Request(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self, apikey=None, model_id=None):
        self.baseapi = "https://models.overture.ai"
        self.__apikey = apikey
        self.__model_id = model_id

        if not self.__apikey:
            raise AttributeError("API Key cannot be None")

        if not self.__model_id:
            raise AttributeError("Model ID cannot be None")

    @abstractmethod
    def _url(self):
        pass

    @abstractmethod
    def predict(self, image):
        pass

    @abstractmethod
    def predict_batch(self, images):
        pass

    def _encode_image(self, filename):
        with open(filename, "rb") as image_file:
            encoded_string = base64.urlsafe_b64encode(image_file.read()).decode("utf-8")

        return encoded_string

    def _filename_to_payload(self, filename):
        b64_image = self._encode_image(filename)
        payload = dict()
        payload[filename] = b64_image
        return payload

    def _filenames_to_payload(self, filenames):
        payload = dict()
        for fn in filenames:
            payload[fn] = self._encode_image(fn)
        return payload

    def _get_header(self):
        return {'Content-Type': 'application/json', 'x-api-key': self.__apikey}

    def validate(self):

        if not self.__apikey:
            raise AttributeError("Please set your API key before executing the request")

        if not self.__model_id:
            raise AttributeError("Please set your model id before executing the request")


class Classification(Request):

    def __init__(self):
        super().__init__()

    def _url(self):
        return self.baseapi + "/predict/image/classification"

    def predict_batch(self, filenames):

        self.validate()

        if not isinstance(filenames, (list,)):
            raise AttributeError("images should be of type 'list")

        if len(filenames) == 0:
            raise AttributeError("images should be a filename list with a length greater than 0")

        r = requests.post(self._url(), headers=self._get_header(), json={
            'model_id': str(self.__model_id),
            'images': self._filenames_to_payload(filenames),
        })

        if r.status_code is not 200:
            raise RestApiError(r.json(), r.status_code)

        return json.loads(r.text)

    def predict(self, filename):

        self.validate()

        r = requests.post(self._url(), headers=self._get_header(), json={
            'model_id': str(self.__model_id),
            'images': self._filename_to_payload(filename)

        })

        if r.status_code is not 200:
            raise RestApiError(r.json(), r.status_code)

        return json.loads(r.text)


class FaceRecognition(Request):

    def __init__(self):
        super().__init__()

    def _url(self):
        return self.baseapi + "/predict/image/facerecognition"

    def predict_batch(self, filenames):

        self.validate()

        if not isinstance(filenames, (list,)):
            raise AttributeError("images should be of type 'list")

        if len(filenames) == 0:
            raise AttributeError("images should be a filename list with a length greater than 0")

        r = requests.post(self._url(), headers=self._get_header(), json={
            'model_id': str(self.__model_id),
            'images': self._filenames_to_payload(filenames),
        })

        if r.status_code is not 200:
            raise RestApiError(r.json(), r.status_code)

        return json.loads(r.text)

    def predict(self, filename):

        self.validate()

        r = requests.post(self._url(), headers=self._get_header(), json={
            'model_id': str(self.__model_id),
            'images': self._filename_to_payload(filename)

        })

        if r.status_code is not 200:
            raise RestApiError(r.json(), r.status_code)

        return json.loads(r.text)


class ObjectDetection(Request):

    def __init__(self):
        super().__init__()

    def _url(self):
        return self.baseapi + "/predict/image/objectdetection"

    def predict_batch(self, filenames):

        self.validate()

        if not isinstance(filenames, (list,)):
            raise AttributeError("images should be of type 'list")

        if len(filenames) == 0:
            raise AttributeError("images should be a filename list with a length greater than 0")

        r = requests.post(self._url(), headers=self._get_header(), json={
            'model_id': str(self.__model_id),
            'images': self._filenames_to_payload(filenames),
        })

        if r.status_code is not 200:
            raise RestApiError(r.json(), r.status_code)

        return json.loads(r.text)

    def predict(self, filename):

        self.validate()

        r = requests.post(self._url(), headers=self._get_header(), json={
            'model_id': str(self.__model_id),
            'images': self._filename_to_payload(filename)

        })

        if r.status_code is not 200:
            raise RestApiError(r.json(), r.status_code)

        return json.loads(r.text)