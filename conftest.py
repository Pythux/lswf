import sys

test_disk_dir = '/tmp/test_lswf/on_disk'
test_ram_dir = '/tmp/test_lswf/on_ram'


def pytest_configure():
    sys._called_from_test = True
    from lswf.service.init import init_if_needed, disk_dir, ram_dir
    if test_disk_dir != disk_dir or test_ram_dir != ram_dir:
        raise SystemError('not test dir wtf', disk_dir, ram_dir)
    init_if_needed()


def pytest_unconfigure():
    import shutil
    from lswf.service.init import disk_dir, ram_dir
    if test_disk_dir != disk_dir or test_ram_dir != ram_dir:
        raise SystemError('not test dir wtf', disk_dir, ram_dir)
    shutil.rmtree('/tmp/test_lswf')


# https://docs.pytest.org/en/2.7.3/plugins.html

# def pytest_runtest_setup(item):
#     # called for running each test

# def pytest_runtest_teardown(item, nextitem):
#     # called after pytest_runtest_call.
