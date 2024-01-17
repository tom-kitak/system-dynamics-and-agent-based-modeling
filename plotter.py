import matplotlib.pyplot as plt
import numpy as np


def plot_num_of_people_on_waiting_list_mean_run(runs, with_or_without_esketamine="with_esketamine"):

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
        plt.title('Number of People in Each Waiting List Over Time With Esketamine')
    else:
        plt.title('Number of People in Each Waiting List Over Time Without Esketamine')
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
    plt.ylabel('Number of People on Waiting List')
    plt.title('Number of People in Each Waiting List Over Time')
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
