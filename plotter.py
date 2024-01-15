import matplotlib.pyplot as plt


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
