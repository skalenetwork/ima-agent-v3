#   -*- coding: utf-8 -*-
#
#   This file is part of ima-agent
#
#   Copyright (C) 2025 SKALE Labs
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

from __future__ import annotations

import inspect
from concurrent.futures import Future, ThreadPoolExecutor, TimeoutError
from threading import Event, Lock, Timer
from typing import Any, Callable, Optional, Set

JobFunc = Callable[..., Any]


def _accepts(fn: JobFunc, name: str) -> bool:
    try:
        return name in inspect.signature(fn).parameters
    except (ValueError, TypeError):
        return False


class JobExecutor:
    """In-memory executor with fixed concurrency, per-job soft timeout, and de-dupe."""

    def __init__(self, workers: int) -> None:
        self._exec = ThreadPoolExecutor(max_workers=workers, thread_name_prefix='job')
        self._inflight: Set[str] = set()
        self._lock = Lock()

    def post_once(
        self,
        job_id: str,
        fn: JobFunc,
        /,
        *args: Any,
        timeout: Optional[float] = None,
        **kwargs: Any,
    ) -> Optional[Future[Any]]:
        """
        Enqueue job if not already queued/running. Returns Future or None if duplicate.
        Soft timeout: Future gets TimeoutError and, if supported, 'cancel_event' is set.
        """
        with self._lock:
            if job_id in self._inflight:
                return None
            self._inflight.add(job_id)

        cancel_event = Event()
        if _accepts(fn, 'cancel_event'):
            kwargs = {**kwargs, 'cancel_event': cancel_event}

        outer: Future[Any] = Future()

        def wrapped() -> Any:
            try:
                return fn(*args, **kwargs)
            finally:
                with self._lock:
                    self._inflight.discard(job_id)

        inner = self._exec.submit(wrapped)

        def bridge(_f: Future[Any]) -> None:
            if outer.done():
                return
            try:
                outer.set_result(inner.result())
            except BaseException as e:
                outer.set_exception(e)

        inner.add_done_callback(bridge)

        if timeout is not None:

            def on_timeout() -> None:
                if not outer.done():
                    cancel_event.set()
                    outer.set_exception(TimeoutError(f'job {job_id} timed out after {timeout}s'))

            t = Timer(timeout, on_timeout)
            t.daemon = True
            t.start()

        return outer

    def shutdown(self) -> None:
        self._exec.shutdown(wait=True, cancel_futures=True)
