class PatientDataCollector:

    def __init__(self):
        self.agent_statistics = {}
        self.event_statistics = {}
        self.aggregated_statistics = {}

    def reset(self):
        self.agent_statistics = {}
        self.event_statistics = {}
        self.aggregated_statistics = {}

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
        self.aggregated_statistics[time] = {}

        self.aggregated_statistics[time]["waiting_list_count"] = {}
        self.aggregated_statistics[time]["waiting_list_count"]["antidepressant_waiting_list"] = 0
        self.aggregated_statistics[time]["waiting_list_count"]["antidepressant_antipsychotic_waiting_list"] = 0
        self.aggregated_statistics[time]["waiting_list_count"]["antipsychotic_waiting_list"] = 0
        self.aggregated_statistics[time]["waiting_list_count"]["esketamine_waiting_list"] = 0
        self.aggregated_statistics[time]["waiting_list_count"]["ect_waiting_list"] = 0

        self.aggregated_statistics[time]["percentage_in_remission"] = 0.0
        self.aggregated_statistics[time]["num_in_remission"] = 0
        self.aggregated_statistics[time]["percentage_in_recovery"] = 0.0
        self.aggregated_statistics[time]["num_in_recovery"] = 0

        for agent in agents:

            # Collect number of patients in waiting list
            if "waiting_list" in agent.state:
                self.aggregated_statistics[time]["waiting_list_count"][agent.state] += 1

            # Collect percentage of patients in remission
            if "remission" in agent.state:
                self.aggregated_statistics[time]["num_in_remission"] += 1

            if "recovery" in agent.state:
                self.aggregated_statistics[time]["num_in_recovery"] += 1

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

        self.aggregated_statistics[time]["percentage_in_remission"] = self.aggregated_statistics[time]["num_in_remission"] / len(agents)
        self.aggregated_statistics[time]["percentage_in_recovery"] = self.aggregated_statistics[time][
                                                                          "num_in_recovery"] / len(agents)


    def statistics(self):
        """
        Get the statistics collected.

        Returns:
            A dictionary with the data that was collected.
        """

        return self.aggregated_statistics
