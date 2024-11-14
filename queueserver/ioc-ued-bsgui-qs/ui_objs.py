from pathlib import Path

from hutch_python.load_conf import load


objs = load('/cds/group/pcds/pyps/apps/hutch-python/ued/conf.yml')
globals().update(**objs)
