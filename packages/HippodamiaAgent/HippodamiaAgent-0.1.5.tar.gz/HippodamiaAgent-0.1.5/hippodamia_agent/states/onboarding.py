from hippodamia_agent.states.aagentstate import AAgentState
from hippodamia_agent.states.event_ids import event_ids


class Onboarding(AAgentState):
    def __init__(self, logger, history, sigint):
        AAgentState.__init__(self, logger, history, sigint)

    def _on_entry(self):
        if self.sigint.is_set():
            return event_ids.SIGINT

        return None

    def _on_exit(self):
        pass
