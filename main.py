from dagster import (
    pipeline,
    ModeDefinition,
)

from pipeline_mvp import settings, resources, admin


@pipeline(
    mode_defs=[
        ModeDefinition(
            resource_defs={'cmf': resources.cmf_resource},
            logger_defs={'custom_console_logger': settings.custom_console_logger}
        )
    ]
)
def pipeline_admin_cod():
    raw_filename = admin.extract_admin_cod()
    df_adm_list = admin.read_in_admin_cod(raw_filename)
    for df_adm in df_adm_list:
        admin.transform_admin_cod(df_adm)
