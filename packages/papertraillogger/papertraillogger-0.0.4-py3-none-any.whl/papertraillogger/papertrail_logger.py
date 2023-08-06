import logging
import socket
from logging.handlers import SysLogHandler


class ContextFilter(logging.Filter):
	hostname = socket.gethostname()

	def filter(self, record):
		record.hostname = ContextFilter.hostname
		return True


class PapertrailLogger:
	def __init__(self, destination, app_name, logging_level):
		self.logger = logging.getLogger()
		self.destination_url = destination.split(":")[0]
		self.destination_code = int(destination.split(":")[1])
		self.syslog = SysLogHandler(address=(self.destination_url, self.destination_code))
		self.syslog.addFilter(ContextFilter())
		self.format = "%(asctime)s %(levelname)s %(hostname)s " + app_name + " (%(process)d): %(message)s"
		self.formatter = logging.Formatter(self.format, datefmt='%b %d %H:%M:%S')
		self.syslog.setFormatter(self.formatter)
		self.logger = logging.getLogger()
		self.logger.addHandler(self.syslog)
		self.logger.setLevel(logging_level)

	def debug(self, msg):
		self.logger.debug(msg)

	def info(self, msg):
		self.logger.info(msg)

	def warning(self, msg):
		self.logger.warning(msg)

	def error(self, msg):
		self.logger.error(msg)

	def critical(self, msg):
		self.logger.critical(msg)
