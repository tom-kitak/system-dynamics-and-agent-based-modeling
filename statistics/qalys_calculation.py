QOL_WEIGHT_REMISSION = 0.826
QOL_WEIGHT_RESPONSE = 0.673
QOL_WEIGHT_NO_RESPONSE = 0.417


def average_qalys(agents):

    total_qalys = 0
    for agent in agents:
        # There are 12 * 4 = 48 weeks in a year
        total_qalys += QOL_WEIGHT_REMISSION * (agent.total_remission_time / 48) \
                       + QOL_WEIGHT_RESPONSE * (agent.total_response_time / 48) \
                       + QOL_WEIGHT_NO_RESPONSE * ((agent.total_time_in_the_model - agent.total_remission_time - agent.total_response_time) / 48)

    return total_qalys / len(agents)
