from threading import Lock

from ..schemas.events import VPetStateSnapshot


class VPetStateStore:
    def __init__(self) -> None:
        self._lock = Lock()
        self._latest_state: VPetStateSnapshot | None = None

    def update(self, snapshot: VPetStateSnapshot) -> VPetStateSnapshot:
        with self._lock:
            self._latest_state = snapshot.model_copy(deep=True)
            return self._latest_state.model_copy(deep=True)

    def get_latest(self) -> VPetStateSnapshot | None:
        with self._lock:
            if self._latest_state is None:
                return None
            return self._latest_state.model_copy(deep=True)
