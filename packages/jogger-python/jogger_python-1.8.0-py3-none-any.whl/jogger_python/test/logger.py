from jogger_python import create_logger, get_logger, LoggerConfig

def test_create_console_logger():
    name = 'test_create_console_logger'
    config = LoggerConfig(name, 'debug', True)
    console_logger = create_logger(config)
    console_logger.debug("debug")
    console_logger.info("info")
    console_logger.warn("warn")
    console_logger.warning("warning")
    console_logger.error("error")
    console_logger.critical("critical")
    console_logger.fatal("fatal")

def test_get_console_logger():
    name = 'test_get_console_logger'
    config = LoggerConfig(name, 'debug', True)
    logger = create_logger(config)
    assert logger is get_logger(name)

def test_cannot_get_logger_twice():
    name = 'test_cannot_get_logger_twice'
    config = LoggerConfig(name, 'debug', True)
    failed = False
    try:
        create_logger(config)
        create_logger(config)
    except AssertionError:
        failed = True

    assert failed is True, "Cannot get same logger name twice"
