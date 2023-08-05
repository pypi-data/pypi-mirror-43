import logging


def reset_logging(conf=None):
    """ Reset logging.
    
    Removes any configured handlers and filters.
    Sets new configuration (if provided).
    """
    if conf is None:
        conf = {}
    root = logging.getLogger()
    list(map(root.removeHandler, root.handlers[:]))
    list(map(root.removeFilter, root.filters[:]))
    logging.config.dictConfig(conf)

