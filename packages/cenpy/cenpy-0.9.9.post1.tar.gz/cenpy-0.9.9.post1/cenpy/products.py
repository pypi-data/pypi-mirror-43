from .base import Connection
from .tiger import FTPConnection

class _Product(object):
    def _resolve_geo_in_geo(self, block=None, blockgroup=None, tract=None, 
                                  county=None, county_subdivision=None, place=None, 
                                  state=None):
        if (block is not None):
        ...

class _Decennial2000(object):
    def __init__(self):
        self._features = Connection('2000sf1')
        self._geometry = FTPConnection('2000sf1')

    def get(self, variables=None, geometry=True, **geo):
        geography_specification = self._resolve_geo_in_geo(**geo)





