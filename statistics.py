import numpy as np
import scipy.stats as stats

QOL_WEIGHT_REMISSION = 0.901
QOL_WEIGHT_RESPONSE = 0.673
QOL_WEIGHT_NO_RESPONSE = 0.417
TREATMENTS = {"antidepressant", "antidepressant_antipsychotic", "antipsychotic", "esketamine", "ect"}
WILLINGNESS_TO_PAY_THRESHOLD = 50000


def average_qalys(agents):

    total_qalys = 0
    for agent in agents:
        # There are 12 * 4 = 48 weeks in a year
        total_qalys += QOL_WEIGHT_REMISSION * (agent.total_remission_time / 48) \
                       + QOL_WEIGHT_RESPONSE * (agent.total_response_time / 48) \
                       + QOL_WEIGHT_NO_RESPONSE * ((agent.total_time_in_the_model - agent.total_remission_time - agent.total_response_time) / 48)

    return total_qalys / len(agents)


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


def mean_treatment_level(agents):
    total_treatments = 0
    for agent in agents:
        for state, _ in agent.treatment_history:
            if state in TREATMENTS:
                total_treatments += 1

    return total_treatments / len(agents)


def aggregated_single_run_statistics(model, config, run_stats):
    direct_cost_per_patient = direct_costs_per_patient(model.agents, config)
    indirect_cost_per_patient = indirect_costs_per_patient(model.agents)

    return {
        "average_qalys": average_qalys(model.agents),
        "direct_costs_per_patient": direct_cost_per_patient,
        "indirect_costs_per_patient": indirect_cost_per_patient,
        "total_costs_per_patient": direct_cost_per_patient + indirect_cost_per_patient,
        "remission_rate": 100 * run_stats[0][config['runspecs']['stoptime']]['percentage_in_remission'],
        "mean_treatment_level": mean_treatment_level(model.agents)
    }


def aggregated_statistics(aggr_run_stats, confidence_level=0.95):

    aggr_stats_results = dict()
    aggr_stats_results["pipelines_comparison"] = {}
    aggr_stats_results["with_esketamine"] = {}
    aggr_stats_results["without_esketamine"] = {}

    for data_point_type in aggr_run_stats["with_esketamine"][f"sim_run_0"]["aggregated_run_statistics"]:

        aggr_stats_results["with_esketamine"][data_point_type] = {}
        aggr_stats_results["without_esketamine"][data_point_type] = {}

        aggr_stats_results["with_esketamine"][data_point_type]["dataset"] = []
        aggr_stats_results["without_esketamine"][data_point_type]["dataset"] = []

    for eskt_or_not in aggr_run_stats:
        for run_num, run_data in aggr_run_stats[eskt_or_not].items():
            for data_point_type, v in run_data["aggregated_run_statistics"].items():
                aggr_stats_results[eskt_or_not][data_point_type]["dataset"].append(v)

    for eskt_or_not in aggr_stats_results:
        for data_point_type in aggr_stats_results[eskt_or_not]:
            dataset = aggr_stats_results[eskt_or_not][data_point_type]["dataset"]
            mean = np.mean(dataset)
            std_dev = np.std(dataset)
            standard_error_of_the_mean = stats.sem(dataset)
            degrees_freedom = len(dataset) - 1
            confidence_interval = stats.t.interval(confidence_level, degrees_freedom, mean, standard_error_of_the_mean)

            aggr_stats_results[eskt_or_not][data_point_type]["mean"] = mean
            aggr_stats_results[eskt_or_not][data_point_type]["standard_deviation"] = std_dev
            aggr_stats_results[eskt_or_not][data_point_type]["standard_error_of_the_mean"] = standard_error_of_the_mean
            aggr_stats_results[eskt_or_not][data_point_type][F"confidence_interval_{confidence_level}"] = confidence_interval

    aggr_stats_results["pipelines_comparison"]["incremental_cost_effectiveness_ratio"] = {}
    aggr_stats_results["pipelines_comparison"]["incremental_cost_effectiveness_ratio"]["dataset"] = []
    aggr_stats_results["pipelines_comparison"]["net_monetary_benefit"] = {}
    aggr_stats_results["pipelines_comparison"]["net_monetary_benefit"]["dataset"] = []

    for run_num in range(len(aggr_stats_results["with_esketamine"]["average_qalys"]["dataset"])):
        run_incremental_effectiveness = \
            aggr_stats_results["with_esketamine"]["average_qalys"]["dataset"][run_num] - aggr_stats_results["without_esketamine"]["average_qalys"]["dataset"][run_num]

        run_incremental_cost = \
            aggr_stats_results["with_esketamine"]["total_costs_per_patient"]["dataset"][run_num] - aggr_stats_results["without_esketamine"]["total_costs_per_patient"]["dataset"][run_num]

        run_icer = run_incremental_cost / run_incremental_effectiveness
        aggr_stats_results["pipelines_comparison"]["incremental_cost_effectiveness_ratio"]["dataset"].append(run_icer)

        nmb = WILLINGNESS_TO_PAY_THRESHOLD * run_incremental_effectiveness - run_incremental_cost
        aggr_stats_results["pipelines_comparison"]["net_monetary_benefit"]["dataset"].append(nmb)

    for comparison_stats in aggr_stats_results["pipelines_comparison"]:
        dataset = aggr_stats_results["pipelines_comparison"][comparison_stats]["dataset"]

        mean = np.mean(dataset)
        std_dev = np.std(dataset)
        standard_error_of_the_mean = stats.sem(dataset)
        degrees_freedom = len(dataset) - 1
        confidence_interval = stats.t.interval(confidence_level, degrees_freedom, mean, standard_error_of_the_mean)

        aggr_stats_results["pipelines_comparison"][comparison_stats]["mean"] = mean
        aggr_stats_results["pipelines_comparison"][comparison_stats]["standard_deviation"] = std_dev
        aggr_stats_results["pipelines_comparison"][comparison_stats]["standard_error_of_the_mean"] = standard_error_of_the_mean
        aggr_stats_results["pipelines_comparison"][comparison_stats][f"confidence_interval_{confidence_level}"] = confidence_interval

    return aggr_stats_results

