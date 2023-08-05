import socket

class LoggerConfig():
    def __init__(self, name=None, log_level=None, log_console=False, remote_syslog=None):
        assert isinstance(name, str), "name is required to be a string, got %s" % type(name)
        assert isinstance(log_level, str), "log_level is required to be a string"

        assert isinstance(log_console, bool) or log_console is None, "If passed, log_console must be a bool"
        assert remote_syslog is None or (isinstance(remote_syslog, tuple) and len(remote_syslog) == 2 and isinstance(remote_syslog[0], str) and isinstance(remote_syslog[1], int)), "If passed, remote_ip is required to be a tuple of (host(str), port(int))"

        assert not ((log_console is None or log_console is False) and remote_syslog is None), "Either log_console or remote_syslog must be passed"

        if remote_syslog is not None:
            socket.gethostbyaddr(remote_syslog[0])

        self.name = name
        self.log_level = log_level
        self.log_console = log_console
        self.remote_syslog = remote_syslog
