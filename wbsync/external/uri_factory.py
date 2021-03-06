"""
"""
import pickle
import os
from abc import ABC, abstractmethod

URIS_FILE = os.path.join(os.getcwd(), 'uris.pkl')

class URIFactory(ABC):

    @abstractmethod
    def get_uri(self, label) -> str:
        """ Gets the uri for a label.

       Parameters
       ----------
       str: label
           Label to find a uri.

       Returns
       -------
       :str: uri
           Uri that corresponds to the label
       """

    @abstractmethod
    def post_uri(self, label, wb_uri) -> None:
        """ Posts the uri for a label.

          Parameters
          ----------
          str: label
              Label that corresponds to the new uri.

          wb_uri: label
              Uri for the label .
          """

class URIFactoryMock(URIFactory):
    class __URIFactoryMock():
        def __init__(self):
            if not os.path.isfile(URIS_FILE):
                with open(URIS_FILE, 'wb') as f:
                    pickle.dump({}, f)

            with open(URIS_FILE, 'rb') as f:
                try:
                    self.state = pickle.load(f)
                except EOFError:
                    self.state = {}

    instance = None

    def __init__(self):
        if not URIFactoryMock.instance:
            URIFactoryMock.instance = URIFactoryMock.__URIFactoryMock()


    def get_uri(self, label):
        return URIFactoryMock.instance.state[label] \
            if label in URIFactoryMock.instance.state else None

    def post_uri(self, label, wb_uri):
        URIFactoryMock.instance.state[label] = wb_uri
        with open(URIS_FILE, 'wb') as f:
            pickle.dump(URIFactoryMock.instance.state, f)

    def reset_factory(self):
        URIFactoryMock.instance.state = {}
        with open(URIS_FILE, 'wb') as f:
            pickle.dump(URIFactoryMock.instance.state, f)
