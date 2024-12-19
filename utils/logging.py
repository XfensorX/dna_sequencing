import os
from typing import Any, Callable

import neptune
from pytorch_lightning.loggers import NeptuneLogger

from .metrics import Metrics

LogMethod = Callable[[str, Any], None]


class Logger:
    """
    A Logger class that provides functionality to log a combination of names and values.

    The Logger class can be instantiated with various log methods and provides
    an easy way to log metrics. It includes factory methods to create Logger
    instances for different logging backends, such as Neptune logger and standard output.
    """

    def __init__(self, log_method: LogMethod):
        """
        Initializes the Logger with a specified logging method.

        Args:
            log_method (LogMethod): A callable that takes a name and a value,
                                    used for logging the data.
        """
        self.log = log_method

    def log_metrics(self, metrics: Metrics):
        """
        Iterates over the provided metrics and logs each metric with
        a prefixed string "metrics".
        """
        for name, value in metrics:
            self.log(f"metrics/{name}", value)

    @classmethod
    def from_lightning_neptune_logger(
        cls, neptune_logger: NeptuneLogger, logging_path: str
    ) -> "Logger":
        """
        Factory method to create a Logger using a Pytorch Lightning Neptune logger backend.

        Args:
            neptune_logger (NeptuneLogger): The Lightning Neptune logger instance.
            logging_path (str): The path where logs should be stored in the Neptune experiment.
        """

        def log(name: str, value: Any):
            neptune_logger.experiment[str(os.path.join(logging_path, name))].log(value)

        return Logger(log)

    @classmethod
    def for_neptune(cls, run: neptune.Run, logging_path: str) -> "Logger":
        """
        Factory method to create a Logger for a Neptune Run.

        Args:
            run (neptune.Run): A Neptune Run instance to use for logging.
            logging_path (str): The path where logs should be stored in the Neptune experiment.
        """

        def log(name: str, value: Any):
            run[str(os.path.join(logging_path, name))].log(value)

        return Logger(log)

    @classmethod
    def for_stdout(cls) -> "Logger":
        """
        Factory method to create a Logger that logs to the standard output.
        """
        return Logger(lambda name, value: print(f"{name}: {value}"))
