import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import sem


def plot_percentage_in_remission_multi_run(runs, plot_confidence_interval=True):
    aggregated_data = dict()
    aggregated_data["with_esketamine"] = dict()
    aggregated_data["without_esketamine"] = dict()

    for with_or_without_esketamine in ["with_esketamine", "without_esketamine"]:
        for sim_num in runs[with_or_without_esketamine]:
            for time_step in runs[with_or_without_esketamine][sim_num]["run_statistics"][0]:
                if time_step not in aggregated_data[with_or_without_esketamine]:
                    aggregated_data[with_or_without_esketamine][time_step] = dict()
                if "sim_dataset" not in aggregated_data[with_or_without_esketamine][time_step]:
                    aggregated_data[with_or_without_esketamine][time_step]["sim_dataset"] = []

                aggregated_data[with_or_without_esketamine][time_step]["sim_dataset"]\
                    .append(runs[with_or_without_esketamine][sim_num]["run_statistics"][0][time_step]["percentage_in_remission"])

    for with_or_without_esketamine in ["with_esketamine", "without_esketamine"]:
        for time_step in aggregated_data[with_or_without_esketamine]:
            aggregated_data[with_or_without_esketamine][time_step]["mean"] = np.mean(aggregated_data[with_or_without_esketamine][time_step]["sim_dataset"])
            if plot_confidence_interval:
                # Calculate standard error of the mean (SEM)
                aggregated_data[with_or_without_esketamine][time_step]["sem"] = sem(
                    aggregated_data[with_or_without_esketamine][time_step]["sim_dataset"])

    weeks = list(aggregated_data["with_esketamine"].keys())
    with_esketamine_remission_rates = np.array(
        [aggregated_data["with_esketamine"][time_step]["mean"] for time_step in weeks])
    with_esketamine_sems = np.array([aggregated_data["with_esketamine"][time_step]["sem"] for time_step in weeks])

    without_esketamine_remission_rates = np.array(
        [aggregated_data["without_esketamine"][time_step]["mean"] for time_step in weeks])
    without_esketamine_sems = np.array([aggregated_data["without_esketamine"][time_step]["sem"] for time_step in weeks])

    # Z-score for 95% confidence
    z_score = 1.96

    # Creating the plot
    plt.figure()

    # Plotting the mean remission rates
    plt.plot(weeks, with_esketamine_remission_rates, label='Remission rates with Esketamine', color='blue')
    plt.plot(weeks, without_esketamine_remission_rates, label='Remission rates without Esketamine', color='red')

    # Adding confidence intervals
    plt.fill_between(weeks,
                     with_esketamine_remission_rates - z_score * with_esketamine_sems,
                     with_esketamine_remission_rates + z_score * with_esketamine_sems,
                     color='blue', alpha=0.1)

    plt.fill_between(weeks,
                     without_esketamine_remission_rates - z_score * without_esketamine_sems,
                     without_esketamine_remission_rates + z_score * without_esketamine_sems,
                     color='red', alpha=0.1)

    # Adding labels and title
    plt.xlabel('Weeks')
    plt.ylabel('Remission rate')
    plt.title('Remission rates with and without Esketamine')
    plt.legend()
    plt.grid(True)

    # Display the plot
    plt.show()


def plot_num_of_people_on_waiting_list_mean_multi_run(runs, with_or_without_esketamine="with_esketamine"):

    aggregated_data = dict()

    for sim_num in runs[with_or_without_esketamine]:
        for time_step in runs[with_or_without_esketamine][sim_num]["run_statistics"][0]:
            if time_step not in aggregated_data:
                aggregated_data[time_step] = dict()
            for waiting_list in runs[with_or_without_esketamine][sim_num]["run_statistics"][0][time_step]["waiting_list_count"]:
                if waiting_list not in aggregated_data[time_step]:
                    aggregated_data[time_step][waiting_list] = dict()
                if "sim_dataset" not in aggregated_data[time_step][waiting_list]:
                    aggregated_data[time_step][waiting_list]["sim_dataset"] = []

                aggregated_data[time_step][waiting_list]["sim_dataset"]\
                    .append(runs[with_or_without_esketamine][sim_num]["run_statistics"][0][time_step]["waiting_list_count"][waiting_list])

    for time_step in aggregated_data:
        for waiting_list in aggregated_data[time_step]:
            aggregated_data[time_step][waiting_list]["mean"] = np.mean(aggregated_data[time_step][waiting_list]["sim_dataset"])

    weeks = list(aggregated_data.keys())
    antidepressant_counts = [aggregated_data[time_step]["antidepressant_waiting_list"]["mean"] for time_step in weeks]
    antidepressant_antipsychotic_counts = [aggregated_data[time_step]["antidepressant_antipsychotic_waiting_list"]["mean"] for time_step in weeks]
    antipsychotic_counts = [aggregated_data[time_step]["antipsychotic_waiting_list"]["mean"] for time_step in weeks]
    if with_or_without_esketamine == "with_esketamine":
        esketamine_counts = [aggregated_data[time_step]["esketamine_waiting_list"]["mean"] for time_step in weeks]
    ect_counts = [aggregated_data[time_step]["ect_waiting_list"]["mean"] for time_step in weeks]

    # Creating the plot
    plt.figure()
    plt.plot(weeks, antidepressant_counts, label='Antidepressant')
    plt.plot(weeks, antidepressant_antipsychotic_counts, label='Antidepressant + Antipsychotic')
    plt.plot(weeks, antipsychotic_counts, label='Antipsychotic')
    if with_or_without_esketamine == "with_esketamine":
        plt.plot(weeks, esketamine_counts, label='Esketamine')
    plt.plot(weeks, ect_counts, label='ECT')

    # Adding labels and title
    plt.xlabel('Weeks')
    plt.ylabel('Number of People on a Waiting List')
    if with_or_without_esketamine == "with_esketamine":
        plt.title('Number of people in each waiting list over time with Esketamine')
    else:
        plt.title('Number of people in each waiting list over time without Esketamine')
    plt.legend()
    plt.grid(True)

    # Display the plot
    plt.show()


def plot_num_of_people_on_waiting_list(data, plot_esketamine=True):

    # Extracting the data for plotting
    weeks = list(data.keys())
    antidepressant_counts = [data[w]['waiting_list_count']['antidepressant_waiting_list'] for w in weeks]
    antidepressant_antipsychotic_counts = [
        data[w]['waiting_list_count']['antidepressant_antipsychotic_waiting_list'] for w in weeks]
    antipsychotic_counts = [data[w]['waiting_list_count']['antipsychotic_waiting_list'] for w in weeks]
    if plot_esketamine:
        esketamine_counts = [data[w]['waiting_list_count']['esketamine_waiting_list'] for w in weeks]
    ect_counts = [data[w]['waiting_list_count']['ect_waiting_list'] for w in weeks]

    # Creating the plot
    plt.figure()
    plt.plot(weeks, antidepressant_counts, label='Antidepressant', marker='o')
    plt.plot(weeks, antidepressant_antipsychotic_counts, label='Antidepressant + Antipsychotic', marker='o')
    plt.plot(weeks, antipsychotic_counts, label='Antipsychotic', marker='o')
    if plot_esketamine:
        plt.plot(weeks, esketamine_counts, label='Esketamine', marker='o')
    plt.plot(weeks, ect_counts, label='ECT', marker='o')

    # Adding labels and title
    plt.xlabel('Weeks')
    plt.ylabel('Number of people on waiting list')
    plt.title('Number of people in each waiting list over time')
    plt.legend()
    plt.grid(True)

    # Display the plot
    plt.show()


def plot_percentage_in_remission(data, title="Esketamine"):
    weeks = list(data.keys())
    percentage_in_remission = [data[w]['percentage_in_remission'] for w in weeks]

    # Creating the plot for percentage in remission
    plt.figure()
    plt.plot(weeks, percentage_in_remission, label='Percentage in Remission', color='green', marker='o')

    # Adding labels and title
    plt.xlabel('Weeks')
    plt.ylabel('Percentage in Remission')
    plt.title(f'Percentage of People in Remission Over Time For {title}')
    plt.grid(True)

    # Display the plot
    plt.show()


def plot_percentage_in_recovery(data, title="Esketamine"):
    weeks = list(data.keys())
    percentage_in_recovery = [data[w]['percentage_in_recovery'] for w in weeks]

    # Creating the plot for percentage in recovery
    plt.figure()
    plt.plot(weeks, percentage_in_recovery, label='Percentage in Recovery', color='green', marker='o')

    # Adding labels and title
    plt.xlabel('Weeks')
    plt.ylabel('Percentage in Recovery')
    plt.title(f'Percentage of People in Recovery Over Time For {title}')
    plt.grid(True)

    # Display the plot
    plt.show()
