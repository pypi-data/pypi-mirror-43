"""
Script which can be called before generating the doc
to generate description of files modified by each option.
"""

from os import listdir
from os.path import isdir
from os.path import splitext, join as pj

from pkglts.config_management import Config


def _nn(cfg, pth):
    """Helper function"""
    print("pth:", pth)
    tgt_name = cfg.render(pth)
    if tgt_name.endswith(".tpl"):
        tgt_name = tgt_name[:-4]

    return tgt_name


def _tree(dname, padding, txt):
    """Generate tree ascii representation of a dir"""
    pkg_cfg = dict(base={"namespace": None,
                         "owner": "owner",
                         "pkgname": "pkgname",
                         "url": None},
                   data={"use_ext_dir": False},
                   doc={"fmt": "rst"},
                   plugin_project={"plugin_name": "plugin"},
                   test={'suite_name': "pytest"})

    cfg = Config(pkg_cfg)

    files = [(isdir(pj(dname, fname)), fname) for fname in listdir(dname)]
    files.sort()

    count = 0
    for is_dir, fname in files:
        fmt_name = _nn(cfg, fname)
        if splitext(fmt_name)[0] != '_':
            count += 1
            txt += padding + '|\n'
            txt += padding + '+-' + fmt_name
            path = pj(dname, fname)
            if is_dir:
                txt += "/\n"
                if count == len(files):
                    txt = _tree(path, padding + ' ' + ' ' * int(len(fmt_name) / 2), txt)
                else:
                    txt = _tree(path, padding + '|' + ' ' * int(len(fmt_name) / 2), txt)
            else:
                txt += '\n'

    return txt


def fmt_tree(dname):
    """Generate tree ascii representation of a dir"""
    return _tree(dname, '', ".\n")
