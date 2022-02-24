from pathlib import Path

from hutch_python.load_conf import load


objs = load(str(Path(__file__).parent.parent.parent / 'conf.yml'))
globals().update(**objs)
