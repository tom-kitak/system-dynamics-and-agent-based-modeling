import numpy as np
from utils.phq_analysis import PHQ9Analysis
import matplotlib.pyplot as plt


if __name__ == "__main__":
    phq_analysis_obj_maintenance = PHQ9Analysis()
    phq_analysis_obj_discontinued = PHQ9Analysis()

    # intervals = phq_analysis_obj_maintenance.return_probability_intervals(group_type="maintenance")
    # # updated_intervals = phq_analysis_obj_maintenance.interpolate_probability_intervals(intervals)
    # phq_analysis_obj_maintenance.plot_interpolated_probability_intervals(intervals)

    # intervals = phq_analysis_obj_maintenance.return_probability_intervals(group_type="discontinued")
    # # updated_intervals = phq_analysis_obj_maintenance.interpolate_probability_intervals(intervals)
    # phq_analysis_obj_maintenance.plot_interpolated_probability_intervals(intervals)
    #
    #
    # phq_analysis_obj_maintenance.plot_cumulative_probabilities("maintenace")
    # phq_analysis_obj_maintenance.plot_cumulative_probabilities("maintenace")

    maintenance = []
    discontinued = []
    for w in range(53):
        maintenance.append(phq_analysis_obj_maintenance.get_prob_at_time(t=w, p=0.27, type="maintenance"))
        discontinued.append(phq_analysis_obj_maintenance.get_prob_at_time(t=w, p=0.27, type="discontinued"))

    maintenance = np.array(maintenance)
    discontinued = np.array(discontinued)

    print(np.sum(maintenance))
    print(np.sum(discontinued))

    # Plotting the numbers
    plt.figure(figsize=(8, 4))
    plt.plot(maintenance[:24], marker='o')
    plt.title('maintenance')
    plt.xlabel('Weeks')
    plt.ylabel('Relapse rate')
    plt.grid(True)
    plt.show()

    # Plotting the numbers
    plt.figure(figsize=(8, 4))
    plt.plot(discontinued, marker='o')
    plt.title('discontinued')
    plt.xlabel('Weeks')
    plt.ylabel('Relapse rate')
    plt.grid(True)
    plt.show()


