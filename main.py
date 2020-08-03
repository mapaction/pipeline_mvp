from dagster import (
    pipeline,
    ModeDefinition,
)

from pipeline_mvp import settings, admin


@pipeline(
    mode_defs=[
        ModeDefinition(
            resource_defs={'cmf': settings.cmf_resource},
            logger_defs={'custom_console_logger': settings.custom_console_logger}
        )
    ]
)
def pipeline_admin_cod():
    raw_filename = admin.extract_admin_cod()
    admin.transform_admin0_cod(raw_filename)
    admin.transform_admin1_cod(raw_filename)
    admin.transform_admin2_cod(raw_filename)
