from hippodamia.agentshadow.states.amonitoringstate import AMonitoringState
from hippodamia.enums import Health


class Onboarded(AMonitoringState):
    func_activate_recv_messages = None

    def __init__(self, id, update_available, set_health, reset_max_level, logger):
        AMonitoringState.__init__(self, id, update_available, set_health, Health.YELLOW, reset_max_level,
                                  logger, __class__.__name__)

    def _on_entry(self):
        return None

    def _on_exit(self):
        pass
