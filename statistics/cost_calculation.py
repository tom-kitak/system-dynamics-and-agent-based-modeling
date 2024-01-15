def direct_costs_per_patient(agents, treatment_config):
    """
        agent.agent_treatment_history (list): A pair where each element is (state, time in weeks in the state).
        treatment_config (dict): dictionary containing information about treatments
    """

    total_cost = 0
    for agent in agents:
        agent_treatment_history = agent.treatment_history
        for i in range(len(agent_treatment_history)):
            state, time_in_state = agent_treatment_history[i]
            if state == "response":
                continue
            elif state == "remission":
                treatment_that_put_them_in_remission, _ = agent_treatment_history[i - 1]
                maintenance_cost = treatment_config["treatment_properties"][treatment_that_put_them_in_remission][
                    "maintenance_cost"]

                # You are in maintenance for maximum of 6 months or 24 weeks
                total_cost += min(time_in_state, 24) * maintenance_cost
            else:
                total_cost += treatment_config["treatment_properties"][state]["treatment_cost"]
    return total_cost // len(agents)


def indirect_costs_per_patient(agents):
    total_cost = 0
    for agent in agents:
        # 714 is in EUR and is average weekly salary, percentages of unemployed people, 0.54 and 0.23, can be found
        # in "Model Data" under "Functional impairment"
        total_cost += ((agent.total_time_in_the_model - agent.total_remission_time) * 0.54 + agent.total_remission_time * 0.23) * 714
    return total_cost // len(agents)
