import os
import socket
import sys
import time

import luigi
import yaml
from morpfw.request import request_factory

try:
    from pyspark.sql import SparkSession

    HAS_SPARK = True
except ImportError:
    HAS_SPARK = False


class MorpTask(luigi.Task):
    settings_file = luigi.Parameter()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not os.path.exists(self.settings_file):
            raise IOError("%s not found" % self.settings_file)
        self.request = request_factory(
            yaml.load(open(self.settings_file), Loader=yaml.Loader)
        )


if HAS_SPARK:

    class MorpSparkTask(MorpTask):
        def spark_session(self):
            os.environ["PYSPARK_PYTHON"] = sys.executable
            os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable
            return SparkSession.builder.appName(
                "%s_%s" % (socket.gethostname(), int(time.time()))
            ).getOrCreate()
