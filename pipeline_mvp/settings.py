import os
import logging

from dagster import (
    Field,
    String,
    resource,
    logger
)
import coloredlogs


class CMF(object):
    def __init__(self, location, event_id):
        self._location = location
        self._event_id = event_id

    def get_raw_data_dir(self):
        return os.path.join(self._location, self._event_id, 'GIS', '1_Original_Data')

    def get_final_data_dir(self):
        return os.path.join(self._location, self._event_id, 'GIS', '2_Active_Data')


@resource(config_schema={'location': Field(String),
                         'event_id': Field(String)})
def cmf_resource(context):
    return CMF(context.resource_config['location'], context.resource_config['event_id'])


@logger(
    {
        'log_level': Field(str, is_required=False, default_value='INFO'),
        'name': Field(str, is_required=False, default_value='dagster'),
    },
    description='Format logger',
)
def custom_console_logger(init_context):

    level = init_context.logger_config['log_level']
    name = init_context.logger_config['name']
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    # Note: if want to turn off Fiona warnings, then can make a separate logger from root,
    # and set root to error level
    dagster_logger = logging.getLoggerClass()(name, level=level)
    root_logger = logging.getLogger()
    for logger in [dagster_logger, root_logger]:
            coloredlogs.install(
            logger=logger,
            level=level,
            fmt=format,
            datefmt=date_format,
            field_styles={'levelname': {'color': 'blue'}, 'asctime': {'color': 'green'}, 'name': {'color': 'magenta'}},
            level_styles={'debug': {}, 'error': {'color': 'red'}},
        )

    # Stop overly verbose Python packages from logging too much
    logging.getLogger("fiona").setLevel(max(logging.WARNING, vars(logging)[level.upper()]))

    return dagster_logger
