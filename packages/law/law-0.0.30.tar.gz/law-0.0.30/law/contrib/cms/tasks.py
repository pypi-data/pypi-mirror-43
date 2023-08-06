# coding: utf-8

"""
CMS-related tasks.
https://home.cern/about/experiments/cms
"""


__all__ = ["BundleCMSSW"]


import os

import luigi


from law import Task, LocalFileTarget, NO_STR
from law.target.file import get_path
from law.decorator import log
from law.util import rel_path, interruptable_popen


class BundleCMSSW(Task):

    task_namespace = "law.cms"

    cmssw_path = luigi.Parameter(description="the path to the CMSSW checkout to bundle")
    exclude = luigi.Parameter(default=NO_STR, description="regular expression for excluding files "
        "or directories, relative to the CMSSW checkout path")

    def __init__(self, *args, **kwargs):
        super(BundleCMSSW, self).__init__(*args, **kwargs)

        self.cmssw_path = os.path.expandvars(os.path.expanduser(os.path.abspath(self.cmssw_path)))

    def output(self):
        return LocalFileTarget("{}.tgz".format(os.path.basename(self.cmssw_path)))

    @log
    def run(self):
        with self.output().localize("w") as tmp:
            self.bundle(tmp.path)

    def bundle(self, dst_path):
        bundle_script = rel_path(__file__, "scripts", "bundle_cmssw.sh")
        cmd = [bundle_script, self.cmssw_path, get_path(dst_path)]
        if self.exclude != NO_STR:
            cmd += [self.exclude]

        code = interruptable_popen(cmd)[0]
        if code != 0:
            raise Exception("cmssw bundling failed")
