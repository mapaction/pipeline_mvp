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
    df_adm0, df_adm1, df_adm2 = admin.read_in_admin_cod(raw_filename)
    admin.transform_admin_cod(df_adm0)
    admin.transform_admin_cod(df_adm1)
    admin.transform_admin_cod(df_adm2)
