#* Imports
import re
import os
import pycook.elisp as el
sc = el.sc
lf = el.lf
os.environ["TERM"] = "linux"

#* Functions
def install_package(package):
    if type(package) is list:
        [install_package(p) for p in package]
    else:
        res = sc("dpkg --get-selections '{package}'")
        if not len(res) or re.search("deinstall$", res):
            el.bash(lf("sudo apt-get install -y {package}"))
        else:
            print(lf("{package}: OK"))


def git_clone(addr, target, commit=None):
    target = el.expand_file_name(target)
    if el.file_exists_p(target):
        print(lf("{target}: OK"))
    else:
        gdir = el.expand_file_name(target)
        pdir = el.file_name_directory(gdir)
        if not el.file_exists_p(pdir):
            el.make_directory(pdir)
        sc("git clone {addr} {gdir}")
        if commit:
            sc("cd {pdir} && git reset --hard {commit}")


def ln(fr, to):
    fr = el.expand_file_name(fr)
    if not el.file_exists_p(fr):
        raise RuntimeError("File doesn't exist", fr)
    to = el.expand_file_name(to)
    if el.file_directory_p(to):
        to_full = el.expand_file_name(el.file_name_nondirectory(fr), to)
    else:
        to_full = to
    if el.file_exists_p(to_full):
        print(lf("{to_full}: OK"))
    else:
        fr_abbr = os.path.relpath(fr, os.path.dirname(to))
        el.sc("ln -s {fr_abbr} {to_full}")


def make(target, cmd, deps=[]):
    if not el.file_exists_p(target):
        el.bash(
            # "TERM=linux " +
            cmd)
