from unittest import mock

from pipeline_mvp.utils import utils


@mock.patch('pipeline_mvp.utils.utils.time')
@mock.patch('pipeline_mvp.utils.utils.os')
def test_get_file_age(mock_os, mock_time):
    """
    Check that a 3600 s difference between now and the file create time returns exactly 1
    """
    mock_time.time.return_value = 3600
    mock_os.path.getatime.return_value = 0
    assert utils.get_file_age_days('') == 1
