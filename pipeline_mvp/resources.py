import os

from dagster import (
    Field,
    String,
    resource
)


class CMF(object):
    def __init__(self, location, event_id, iso3):
        self._location = location
        self._event_id = event_id
        self.iso3 = iso3

    def get_raw_data_dir(self):
        return os.path.join(self._location, self._event_id, 'GIS', '1_Original_Data')

    def get_final_data_dir(self):
        return os.path.join(self._location, self._event_id, 'GIS', '2_Active_Data')


@resource(config_schema={'location': Field(String),
                         'event_id': Field(String),
                         'iso3': Field(String)
                         })
def cmf_resource(context):
    return CMF(location=context.resource_config['location'],
               event_id=context.resource_config['event_id'],
               iso3=context.resource_config['iso3'])
