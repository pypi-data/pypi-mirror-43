import logging


def get_logger(name):
	# default
	logger = logging.getLogger(name)
	logger.setLevel(logging.INFO)

	# file handler
	# h = logging.FileHandler('job.log')

	# console handler
	h = logging.StreamHandler()

	# formatter
	formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
	h.setFormatter(formatter)
	
	logger.addHandler(h)
	return logger
