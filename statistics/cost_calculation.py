

def aggregated_costs(agents, treatment_config):

    total_cost = 0
    for agent in agents:
        total_cost += direct_agent_cost(agent, treatment_config)
    return total_cost


def direct_agent_cost(agent, treatment_config):
    """
        agent.agent_treatment_history (list): A pair where each element is (state, time in weeks in the state).
        treatment_config (dict): dictionary containing information about treatments
    """
    total_cost = 0
    agent_treatment_history = agent.treatment_history
    for i in range(len(agent_treatment_history)):
        state, time_in_state = agent_treatment_history[i]
        if state == "response":
            continue
        elif state == "remission":
            treatment_that_put_them_in_remission, _ = agent_treatment_history[i-1]
            maintenance_cost = treatment_config["treatment_properties"][treatment_that_put_them_in_remission]["maintenance_cost"]

            # You are in maintenance for maximum of 6 months or 24 weeks
            total_cost += min(time_in_state, 24) * maintenance_cost
        else:
            total_cost += treatment_config["treatment_properties"][state]["treatment_cost"]

    return total_cost
