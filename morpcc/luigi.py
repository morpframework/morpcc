import os
import socket
import sys
import threading
import time
import typing

import luigi
import transaction
import yaml
from morpfw.request import request_factory

try:
    from pyspark.sql import SparkSession

    HAS_SPARK = True
except ImportError:
    HAS_SPARK = False

threadlocal = threading.local()


class MorpTask(luigi.Task):
    settings_file = luigi.Parameter()

    environ: typing.Optional[dict] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not os.path.exists(self.settings_file):
            raise IOError("%s not found" % self.settings_file)

    def request(self):
        extra_environ = self.environ or {}
        return request_factory(
            yaml.load(open(self.settings_file), Loader=yaml.Loader),
            extra_environ=extra_environ,
        )


if HAS_SPARK:

    class MorpSparkTask(MorpTask):
        def spark_session(self):
            if not os.environ.get("PYSPARK_PYTHON", None):
                os.environ["PYSPARK_PYTHON"] = sys.executable
            if not os.environ.get("PYSPARK_DRIVER_PYTHON", None):
                os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable
            return SparkSession.builder.appName(
                "%s_%s" % (socket.gethostname(), int(time.time()))
            ).getOrCreate()
