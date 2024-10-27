import random
import time
from functools import lru_cache
from typing import NoReturn
from queue import Queue

from schemas import Event, EventState


class EventStorage:
    __DELAY: int = 5

    def __init__(self):
        super().__init__()
        self.completed_win1 = []
        self.completed_win2 = []
        self.pending = []
        self.fifo_changes = Queue()

    async def add(self, event: Event) -> None | NoReturn:
        match event.state:
            case "win1":
                self.completed_win1.append(event)
            case "win2":
                self.completed_win2.append(event)
            case "open":
                self.pending.append(event)
            case _:
                raise ValueError
        self.fifo_changes.put(event)

    def __getitem__(self, state: EventState) -> list[Event] | NoReturn:
        match state:
            case "win1":
                return self.completed_win1
            case "win2":
                return self.completed_win2
            case "open":
                return self.pending
            case _:
                raise ValueError

    def __contains__(self, event: Event) -> bool:
        for inner_event in self.all:
            if event.id == inner_event.id:
                return True
        return False

    @property
    def all(self):
        return self.completed_win1 + self.completed_win2 + self.pending

    def __len__(self):
        return len(self.all)

    def _update_event(self, event: Event) -> None:
        event.state = random.choice(["win1", "win2"])
        if event.state == "win1":
            self.completed_win1.append(event)
        else:
            self.completed_win2.append(event)
        self.fifo_changes.put(event)

    def _update(self) -> None:
        _temp_pending = self.pending[:]
        for e_ind, event in enumerate(self.pending):
            if event.deadline < time.time() - self.__DELAY:
                _temp_pending.remove(event)
                self._update_event(event)
        self.pending = _temp_pending

    async def get_updates(self):
        self._update()
        while not self.fifo_changes.empty():
            yield self.fifo_changes.get()
        else:
            self.fifo_changes.task_done()

@lru_cache
def storage() -> EventStorage:
    return EventStorage()
