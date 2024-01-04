from collections import defaultdict


class PatientDataCollector:

    def __init__(self):
        self.agent_statistics = {}
        self.event_statistics = {}
        self.aggregated_statistics = {}

    def reset(self):
        self.agent_statistics = {}
        self.event_statistics = {}
        self.aggregated_statistics = {}

    # def record_event(self, time, event):
    #     """
    #     Record an event

    #     Parameters:
    #         time: Timestep.
    #             The time at which to record the event.
    #         event: event instance
    #             The event to record.
    #     """
    #     if time not in self.event_statistics:
    #         self.event_statistics[time] = {}

    #     if event.name not in self.event_statistics[time]:
    #         self.event_statistics[time][event.name] = 0

    #     self.event_statistics[time][event.name] += 1

    def collect_agent_statistics(self, time, agents):
        """
        Collect agent statistics from agent(s).

        Parameters:
            time: Timestep.
                The timestep at which to collect agents.
            agents: List of agent.
                The list of agents to collect.
        """
        self.agent_statistics[time] = {}
        self.aggregated_statistics[time] = defaultdict(int)

        for agent in agents:

            self.aggregated_statistics[time]["monetary_cost"] += agent.monetary_cost

            if agent.agent_type not in self.agent_statistics[time]:
                self.agent_statistics[time][agent.agent_type] = {}

            if agent.state not in self.agent_statistics[time][agent.agent_type]:
                self.agent_statistics[time][agent.agent_type][agent.state] = {"count": 0}

            self.agent_statistics[time][agent.agent_type][agent.state]["count"] += 1

            if agent.properties:

                for agent_property_name, agent_property_value in agent.properties.items():
                    if agent_property_value["type"] == "Integer" or agent_property_value["type"] == "Double":
                        if agent_property_name not in self.agent_statistics[time][agent.agent_type][agent.state]:
                            self.agent_statistics[time][agent.agent_type][agent.state][agent_property_name] = {
                                "total": 0, "max": None, "min": None}

                        self.agent_statistics[time][agent.agent_type][agent.state][agent_property_name]["total"] += \
                        agent_property_value["value"]

                        self.agent_statistics[time][agent.agent_type][agent.state][agent_property_name]["mean"] = (
                                    self.agent_statistics[time][agent.agent_type][agent.state][agent_property_name]["total"]/
                                    self.agent_statistics[time][agent.agent_type][agent.state]["count"]
                        )

                        if self.agent_statistics[time][agent.agent_type][agent.state][agent_property_name][
                            "max"] is None:
                            (self.agent_statistics[time][agent.agent_type][agent.state]
                            [agent_property_name]["max"]) = agent_property_value["value"]

                            (self.agent_statistics[time][agent.agent_type][agent.state]
                            [agent_property_name]["min"]) = agent_property_value["value"]


                        else:
                            (self.agent_statistics[time][agent.agent_type][agent.state]
                            [agent_property_name]["max"]) = (max(self.agent_statistics[time][agent.agent_type]
                                                                 [agent.state][agent_property_name]["max"],
                                                                 agent_property_value["value"]))

                            (self.agent_statistics[time][agent.agent_type][agent.state]
                            [agent_property_name]["min"]) = (min(self.agent_statistics[time][agent.agent_type]
                                                                 [agent.state][agent_property_name]["min"],
                                                                 agent_property_value["value"]))


    def statistics(self):
        """
        Get the statistics collected.

        Returns:
            A dictionary with the data that was collected.
        """

        return self.aggregated_statistics

    def agg_statistics(self):
        """
        Get the aggregated statistics collected.

        Returns:
            A dictionary with the data that was collected.
        """

        return self.aggregated_statistics
