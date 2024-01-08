import matplotlib.pyplot as plt


def plot_num_of_people_on_waiting_list(data):

    # Extracting the data for plotting
    weeks = list(data.keys())
    antidepressant_counts = [data[w]['waiting_list_count']['antidepressant_waiting_list'] for w in weeks]
    antidepressant_antipsychotic_counts = [
        data[w]['waiting_list_count']['antidepressant_antipsychotic_waiting_list'] for w in weeks]
    antipsychotic_counts = [data[w]['waiting_list_count']['antipsychotic_waiting_list'] for w in weeks]
    esketamine_counts = [data[w]['waiting_list_count']['esketamine_waiting_list'] for w in weeks]
    ect_counts = [data[w]['waiting_list_count']['ect_waiting_list'] for w in weeks]

    # Creating the plot
    plt.figure()
    plt.plot(weeks, antidepressant_counts, label='Antidepressant', marker='o')
    plt.plot(weeks, antidepressant_antipsychotic_counts, label='Antidepressant + Antipsychotic', marker='o')
    plt.plot(weeks, antipsychotic_counts, label='Antipsychotic', marker='o')
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


def plot_percentage_in_remission(data):
    weeks = list(data.keys())
    percentage_in_remission = [data[w]['percentage_in_remission'] for w in weeks]

    # Creating the plot for percentage in remission
    plt.figure()
    plt.plot(weeks, percentage_in_remission, label='Percentage in Remission', color='green', marker='o')

    # Adding labels and title
    plt.xlabel('Weeks')
    plt.ylabel('Percentage in Remission')
    plt.title('Percentage of People in Remission Over Time')
    plt.grid(True)

    # Display the plot
    plt.show()


def plot_total_monetary_cost(data):
    # Extracting time points and corresponding total monetary cost
    weeks = list(data.keys())
    total_monetary_cost = [data[w]['total_monetary_cost'] for w in weeks]

    # Plotting the data
    plt.figure()
    plt.plot(weeks, total_monetary_cost, marker='o')

    # Setting y-axis tick labels to display full numbers
    plt.ticklabel_format(style='plain', axis='y')

    # Adding labels and title
    plt.title("Total Monetary Cost in EUR Over Time")
    plt.xlabel("Weeks")
    plt.ylabel("Total Monetary Cost in EUR")
    plt.grid(True)

    # Display the plot
    plt.show()

