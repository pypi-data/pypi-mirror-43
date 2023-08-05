# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Context manager that wraps an AutoML run context."""
import sys
import time
from automl.client.core.common.automl_run_context import AutoMLAbstractRunContext

from azureml._async import TaskQueue
from azureml.core import Run


class AzureAutoMLRunContext(AutoMLAbstractRunContext):

    def _get_run_internal(self):
        """Retrieve a run context if needed and return it."""
        # In case we use get_run in nested with statements, only get the run context once
        if self._refresh_needed():
            self._last_refresh = time.time()
            self._run = Run.get_context()
        return self._run

    def _refresh_needed(self) -> bool:
        if self._run is None:
            return True

        if self._is_adb_run:
            return (time.time() - self._last_refresh) > self._timeout_interval

        return False

    def save_model_output_async(self, fitted_pipeline: object, remote_path: str) -> None:
        """
        Async save model function.

        :param fitted_pipeline:
        :param remote_path:
        :return:
        """
        self._task_queue.add(super(AzureAutoMLRunContext, self).save_model_output, fitted_pipeline, remote_path)

    def start_async_job(self, func, scores, logger):
        """
        Start async job function.

        :param func:
        :param scores:
        :param logger:
        :return:
        """
        self._task_queue.add(func, self, scores, logger)

    @property
    def _task_queue(self):
        if self._task_queue_internal is not None:
            return self._task_queue_internal

        self._task_queue_internal = TaskQueue(_ident=self._ident)
        return self._task_queue_internal

    def flush(self, timeout_seconds=sys.maxsize):
        timeout_seconds = timeout_seconds if timeout_seconds > 0 else sys.maxsize
        self._task_queue.flush(self._ident, timeout_seconds=timeout_seconds)

    def __init__(self, run, is_adb_run: bool = False) -> None:
        """
        Create an AzureAutoMLRunContext object that wraps a run context.

        :param run: the run context to use
        :param is_adb_run: whether we are running in Azure DataBricks or not
        """
        super().__init__()
        self._run = run
        self._is_adb_run = is_adb_run

        # Refresh the run context after 15 minutes if running under adb
        self._timeout_interval = 900
        self._last_refresh = 0
        self._task_queue_internal = None
        self._ident = 'AutoMLRunContextTasks'
