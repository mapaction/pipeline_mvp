import os
import logging

from dagster import (
    Field,
    String,
    pipeline,
    resource,
    ModeDefinition
)


from pipeline_mvp.utils.utils import config_logger
from pipeline_mvp.admin import extract_admin_cod

config_logger()
logger = logging.getLogger(__name__)


class CMF(object):
    def __init__(self, location, event_id):
        self._location = location
        self._event_id = event_id

    def get_raw_data_dir(self):
        return os.path.join(self._location, self._event_id, 'GIS', '1_Original_Data')


@resource(config_schema={'location': Field(String),
                         'event_id': Field(String)})
def cmf_resource(context):
    return CMF(context.resource_config['location'], context.resource_config['event_id'])


@pipeline(
    mode_defs=[
        ModeDefinition(
            resource_defs={'cmf': cmf_resource}
        )
    ]
)
def pipeline_admin_cod():
    extract_admin_cod()
