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

from threading import Event, Thread
from typing import Any, Callable, Optional

Target = Callable[..., Any]


class ThreadGroup:
    def __init__(self) -> None:
        self.cancel = Event()
        self._threads: list[Thread] = []
        self._error: Optional[BaseException] = None

    def go(self, target: Target, *args: Any, **kwargs: Any) -> None:
        import inspect

        if 'cancel' in inspect.signature(target).parameters:
            kwargs = {**kwargs, 'cancel': self.cancel}

        def run() -> None:
            try:
                target(*args, **kwargs)
            except BaseException as e:
                if self._error is None:
                    self._error = e
                    self.cancel.set()

        t = Thread(target=run, daemon=True)
        t.start()
        self._threads.append(t)

    def join(self) -> None:
        for t in self._threads:
            t.join()
        if self._error:
            raise self._error
