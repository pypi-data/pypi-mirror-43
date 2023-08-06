
"""
Global settings
"""

DEBUG = False

SERVER_CLASS = 'socketserver.UDPServer'
REQUEST_HANDLER = 'socketserver.BaseRequestHandler'




###########
# LOGGING #
###########

# The callable to use to configure logging
LOGGING_CONFIG = 'logging.config.dictConfig'

# Custom logging configuration.
LOGGING = {}

if DEBUG:
    LOG_LEVEL = 'DEBUG'
else:
    LOG_LEVEL = 'INFO'