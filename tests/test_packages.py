from sysmon.packages import find_latest


def test_find_latest():
    versions = (
        '0.0.1',
        '0.0.10',
        '0.0.11',
        '0.1',
        '0.1.1',
        '1.0',
    )

    current = '0.0.9'

    current2, newest, newest_major, newest_minor = find_latest(current, versions)

    assert current2 == current
    assert newest == '1.0'
    assert newest_major == '0.1.1'
    assert newest_minor == '0.0.11'
