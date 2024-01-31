import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import sem


def plot_percentage_in_recovery_multi_run(runs, plot_confidence_interval=True, after_weeks=0):
    aggregated_data = dict()

    for run_name in runs:
        aggregated_data[run_name] = dict()

        for sim_num in runs[run_name]:
            for time_step in runs[run_name][sim_num]["run_statistics"][0]:
                if time_step not in aggregated_data[run_name]:
                    aggregated_data[run_name][time_step] = dict()
                if "sim_dataset" not in aggregated_data[run_name][time_step]:
                    aggregated_data[run_name][time_step]["sim_dataset"] = []

                aggregated_data[run_name][time_step]["sim_dataset"]\
                    .append(runs[run_name][sim_num]["run_statistics"][0][time_step]["percentage_in_recovery"])

    for run_name in runs:
        for time_step in aggregated_data[run_name]:
            aggregated_data[run_name][time_step]["mean"] = np.mean(aggregated_data[run_name][time_step]["sim_dataset"])
            if plot_confidence_interval:
                # Calculate standard error of the mean (SEM)
                aggregated_data[run_name][time_step]["sem"] = sem(
                    aggregated_data[run_name][time_step]["sim_dataset"])

    weeks = list(aggregated_data["without_esketamine"].keys())

    plot_results = dict()
    for run_name in runs:
        plot_results[run_name + "_recovery_rates"] = np.array([aggregated_data[run_name][time_step]["mean"] for time_step in weeks])
        plot_results[run_name + "_sems"] = np.array([aggregated_data[run_name][time_step]["sem"] for time_step in weeks])

        plot_results[run_name + "_recovery_rates"] = plot_results[run_name + "_recovery_rates"][after_weeks:]
        plot_results[run_name + "_sems"] = plot_results[run_name + "_sems"][after_weeks:]

    # Z-score for 95% confidence
    z_score = 1.96

    # Creating the plot
    plt.figure(figsize=(8, 6))

    # Plotting the mean recovery rates
    if after_weeks > 0:
        weeks = weeks[:-after_weeks]

    for run_name in runs:
        run_key = run_name + "_recovery_rates"
        plt.plot(weeks, plot_results[run_key], label=run_key.replace("_", " "))

        # Adding confidence intervals
        plt.fill_between(weeks,
                         plot_results[run_key] - z_score * plot_results[run_name + "_sems"],
                         plot_results[run_key] + z_score * plot_results[run_name + "_sems"], alpha=0.1)

    # Adding labels and title
    plt.xlabel('Weeks')
    plt.ylabel('Recovery rate')
    plt.legend()
    plt.grid(True)

    # Display the plot
    plt.ylim(0, 1)
    plt.show()


def plot_percentage_in_remission_multi_run(runs, plot_confidence_interval=True, after_weeks=0):
    aggregated_data = dict()

    for run_name in runs:
        aggregated_data[run_name] = dict()

        for sim_num in runs[run_name]:
            for time_step in runs[run_name][sim_num]["run_statistics"][0]:
                if time_step not in aggregated_data[run_name]:
                    aggregated_data[run_name][time_step] = dict()
                if "sim_dataset" not in aggregated_data[run_name][time_step]:
                    aggregated_data[run_name][time_step]["sim_dataset"] = []

                aggregated_data[run_name][time_step]["sim_dataset"]\
                    .append(runs[run_name][sim_num]["run_statistics"][0][time_step]["percentage_in_remission"])

    for run_name in runs:
        for time_step in aggregated_data[run_name]:
            aggregated_data[run_name][time_step]["mean"] = np.mean(aggregated_data[run_name][time_step]["sim_dataset"])
            if plot_confidence_interval:
                # Calculate standard error of the mean (SEM)
                aggregated_data[run_name][time_step]["sem"] = sem(
                    aggregated_data[run_name][time_step]["sim_dataset"])

    weeks = list(aggregated_data["without_esketamine"].keys())

    plot_results = dict()
    for run_name in runs:
        plot_results[run_name + "_remission_rates"] = np.array([aggregated_data[run_name][time_step]["mean"] for time_step in weeks])
        plot_results[run_name + "_sems"] = np.array([aggregated_data[run_name][time_step]["sem"] for time_step in weeks])

        plot_results[run_name + "_remission_rates"] = plot_results[run_name + "_remission_rates"][after_weeks:]
        plot_results[run_name + "_sems"] = plot_results[run_name + "_sems"][after_weeks:]

    # Z-score for 95% confidence
    z_score = 1.96

    # Creating the plot
    plt.figure(figsize=(8, 6))

    # Plotting the mean remission rates
    if after_weeks > 0:
        weeks = weeks[:-after_weeks]

    for run_name in runs:
        run_key = run_name + "_remission_rates"
        plt.plot(weeks, plot_results[run_key], label=run_key.replace("_", " "))

        # Adding confidence intervals
        plt.fill_between(weeks,
                         plot_results[run_key] - z_score * plot_results[run_name + "_sems"],
                         plot_results[run_key] + z_score * plot_results[run_name + "_sems"], alpha=0.1)

    # Adding labels and title
    plt.xlabel('Weeks')
    plt.ylabel('Remission rate')
    plt.legend()
    # plt.grid(True)

    max_weeks = len(weeks)
    plt.xticks(np.arange(0, max_weeks + 1, 100))  # Setting x-axis ticks every 100 weeks
    plt.grid(True, which='both', axis='x', linestyle='-', linewidth=0.5)  # Adding grid lines for x-axis

    # Display the plot
    plt.show()


def plot_num_of_people_on_waiting_list_mean_multi_run(run_name, run_data, after_weeks=0):

    aggregated_data = dict()

    for sim_num in run_data:
        for time_step in run_data[sim_num]["run_statistics"][0]:
            if time_step not in aggregated_data:
                aggregated_data[time_step] = dict()
            for waiting_list in run_data[sim_num]["run_statistics"][0][time_step]["waiting_list_count"]:
                if waiting_list not in aggregated_data[time_step]:
                    aggregated_data[time_step][waiting_list] = dict()
                if "sim_dataset" not in aggregated_data[time_step][waiting_list]:
                    aggregated_data[time_step][waiting_list]["sim_dataset"] = []

                aggregated_data[time_step][waiting_list]["sim_dataset"]\
                    .append(run_data[sim_num]["run_statistics"][0][time_step]["waiting_list_count"][waiting_list])

    for time_step in aggregated_data:
        for waiting_list in aggregated_data[time_step]:
            aggregated_data[time_step][waiting_list]["mean"] = np.mean(aggregated_data[time_step][waiting_list]["sim_dataset"])

    weeks = list(aggregated_data.keys())

    antidepressant_counts = [aggregated_data[time_step]["antidepressant_waiting_list"]["mean"] for time_step in weeks]
    antidepressant_antipsychotic_counts = [aggregated_data[time_step]["antidepressant_antipsychotic_waiting_list"]["mean"] for time_step in weeks]
    antipsychotic_counts = [aggregated_data[time_step]["antipsychotic_waiting_list"]["mean"] for time_step in weeks]
    if "%" in run_name:
        # it is with eskt
        esketamine_counts = [aggregated_data[time_step]["esketamine_waiting_list"]["mean"] for time_step in weeks]
    ect_counts = [aggregated_data[time_step]["ect_waiting_list"]["mean"] for time_step in weeks]

    # Creating the plot
    if after_weeks > 0:
        weeks = weeks[:-after_weeks]
        antidepressant_counts = antidepressant_counts[after_weeks:]
        antidepressant_antipsychotic_counts = antidepressant_antipsychotic_counts[after_weeks:]
        antipsychotic_counts = antipsychotic_counts[after_weeks:]
        ect_counts = ect_counts[after_weeks:]
        if "%" in run_name:
            esketamine_counts = esketamine_counts[after_weeks:]

    plt.figure(figsize=(6, 4.5))

    markers = ['o', 's', 'D', '^', 'v']  # Circle, Square, Diamond, Triangle Up, Triangle Down
    markevery = 50

    weeks = [int(float(k)) for k in weeks]
    # Plot the lines with markers every 50 weeks
    plt.plot(weeks, antidepressant_counts, label='Antidepressant', color="blue", marker=markers[0], markevery=markevery)
    plt.plot(weeks, antidepressant_antipsychotic_counts, label='Antidepressant + Antipsychotic', color="orange", marker=markers[1], markevery=markevery)
    plt.plot(weeks, antipsychotic_counts, label='Antipsychotic', color="purple", marker=markers[2], markevery=markevery)
    plt.plot(weeks, ect_counts, label='ECT', color="green", marker=markers[4], markevery=markevery)
    if "%" in run_name:
        plt.plot(weeks, esketamine_counts, label='Esketamine', color="red", marker=markers[3], markevery=markevery)

    # # Adding labels and title
    plt.xlabel('Weeks')
    plt.ylabel('Number of people on a waiting list')

    plt.xticks(np.arange(0, 751, 100))
    plt.yticks(np.arange(0, 1301, 200))
    plt.xlim(0, 750)
    plt.ylim(0, 1300)

    # Add grid lines
    plt.grid(True)

    if "%" in run_name:
        eskt_percentage = run_name.split("%")[0]
        plt.title(f"{eskt_percentage}% of capacity going to Esketamine")
    else:
        plt.title("Without Esketamine")
    plt.legend()

    # Save the figure in high resolution for scientific paper
    plt.savefig(f'{run_name}.png', dpi=300, bbox_inches='tight')

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
