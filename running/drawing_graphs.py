from utils import plotter
import os
import json
from utils import statistics as custom_stats

if __name__ == "__main__":

    AFTER_WEEKS_PLOT = 0

    pwd = os.path.dirname(os.path.realpath(__file__))
    runs_file = os.path.join(pwd, "../results", "runs_data_dump.json")

    with open(runs_file, 'r') as file:
        runs = json.load(file)

    # Plotting
    for run_name, run_data in runs.items():
        plotter.plot_num_of_people_on_waiting_list_mean_multi_run(run_name, run_data, after_weeks=AFTER_WEEKS_PLOT)

    plotter.plot_percentage_in_remission_multi_run(runs, after_weeks=AFTER_WEEKS_PLOT)
    plotter.plot_percentage_in_recovery_multi_run(runs, after_weeks=AFTER_WEEKS_PLOT)