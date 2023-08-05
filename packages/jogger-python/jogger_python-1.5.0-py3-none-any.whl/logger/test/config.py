from logger.config import LoggerConfig

def assert_eq(name, expected, actual):
    assert expected == actual, "mismatch of %s -- expected: %s, actual: %s" % (name, expected, actual)

def test_full_config():
    name = "full_config"
    log_level = "debug"
    log_console = True
    remote_syslog = ("localhost", 514)

    config = LoggerConfig(name=name, log_level=log_level, log_console=log_console, remote_syslog=remote_syslog)

    assert_eq("name", name, config.name)
    assert_eq("log_level", log_level, config.log_level)
    assert_eq("log_console", log_console, config.log_console)
    assert_eq("remote_syslog", remote_syslog, config.remote_syslog)

def test_no_config():
    try:
        LoggerConfig()
    except AssertionError:
        pass

    try:
        LoggerConfig('name')
    except AssertionError:
        pass

    try:
        LoggerConfig('name', 'log_level')
    except AssertionError:
        pass

    try:
        LoggerConfig('name', 'log_level', False)
    except AssertionError:
        pass

    try:
        LoggerConfig('name', 'log_level', False, ())
    except AssertionError:
        pass

    LoggerConfig('name', 'log_level', False, ('localhost', 123))

def test_no_syslog():
    name = "full_config"
    log_level = "debug"
    log_console = True
    remote_syslog = None
    config = LoggerConfig(name=name, log_level=log_level, log_console=log_console, remote_syslog=remote_syslog)

    assert_eq("name", name, config.name)
    assert_eq("log_level", log_level, config.log_level)
    assert_eq("log_console", log_console, config.log_console)
    assert_eq("remote_syslog", remote_syslog, config.remote_syslog)

def test_no_console():
    name = "full_config"
    log_level = "debug"
    log_console = False
    remote_syslog = ("localhost", 514)
    config = LoggerConfig(name=name, log_level=log_level, log_console=log_console, remote_syslog=remote_syslog)

    assert_eq("name", name, config.name)
    assert_eq("log_level", log_level, config.log_level)
    assert_eq("log_console", log_console, config.log_console)
    assert_eq("remote_syslog", remote_syslog, config.remote_syslog)

def test_no_outputs():
    name = "full_config"
    log_level = "debug"
    log_console = False
    remote_syslog = None
    failed = False

    try:
        config = LoggerConfig(name=name, log_level=log_level, log_console=log_console, remote_syslog=remote_syslog)
    except AssertionError:
        failed = True

    assert_eq("failed", True, failed)
