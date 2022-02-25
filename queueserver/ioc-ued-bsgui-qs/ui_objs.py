from pathlib import Path

from hutch_python.load_conf import load


objs = load('/cds/home/z/zlentz/github/ued/conf.yml')
globals().update(**objs)
