import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit


class PHQ9Analysis:
    def __init__(self):
        self.relapse_threshold = 6
        self.time_points = {"baseline": 0, "6wk": 6, "12wk": 12, "26wk": 26, "39wk": 39, "52wk": 52}

        # PHQ-9 scores data for maintenance and discontinued groups
        self.phq_scores_maintenance = {
            "baseline": [3.9, 3.5],
            "6wk": [4.1, 3.8],
            "12wk": [4.1, 3.8],
            "26wk": [4.2, 3.7],
            "39wk": [3.8, 3.9],
            "52wk": [3.7, 3.7]
        }

        self.phq_scores_discontinued = {
            "baseline": [3.8, 3.6],
            "6wk": [4.4, 4.0],
            "12wk": [6.3, 5.1],
            "26wk": [5.0, 4.6],
            "39wk": [4.4, 4.2],
            "52wk": [4.0, 4.5]
        }

        self.sorted_times = sorted(self.time_points.keys(), key=lambda x: self.time_points[x])
        self.sorted_time_values = [self.time_points[time] for time in self.sorted_times]

        # Calculate proportions and interval probabilities for both groups
        self.proportions_maintenance = self.calculate_proportions(self.phq_scores_maintenance)
        self.proportions_discontinued = self.calculate_proportions(self.phq_scores_discontinued)
        self.interval_probs_maintenance = self.cumulative_to_interval(self.proportions_maintenance)
        self.interval_probs_discontinued = self.cumulative_to_interval(self.proportions_discontinued)

    # Existing functions are transformed to methods here
    def calculate_proportions(self, phq_scores):
        proportions = {}
        for time, (mean, sd) in phq_scores.items():
            proportion_relapse = norm.sf(self.relapse_threshold, loc=mean, scale=sd)
            proportions[time] = proportion_relapse
        return proportions

        # Transforming cumulative probabilities to interval probabilities
    def cumulative_to_interval(self, cumulative_probs):
        sorted_probs = [cumulative_probs[time] for time in self.sorted_times]
        interval_probs = [sorted_probs[0]]
        for i in range(1, len(sorted_probs)):
            interval_prob = sorted_probs[i] - sorted_probs[i - 1]
            interval_probs.append(max(interval_prob, 0))  # Ensure non-negative probabilities
        return interval_probs

    def calculate_cumulative_probability(self, time_point, interval_probs, time_values):
        cumulative_probability = 0
        for i, time in enumerate(time_values):
            if self.time_points[time] <= time_point:  # Use time_points[time] instead of just time
                cumulative_probability += interval_probs[i]
            else:
                break
        return cumulative_probability  # Also, you missed returning this value

    def plot_cumulative_probability(self):
        plt.figure(figsize=(12, 8))
        plt.step(self.sorted_time_values, self.interval_probs_maintenance, label='Maintenance Group', where='mid', linewidth=2)
        plt.step(self.sorted_time_values, self.interval_probs_discontinued, label='Discontinued Group', where='mid', linestyle='--',
                 linewidth=2)
        # Customizing x-axis ticks and labels
        plt.xticks(self.sorted_time_values, self.sorted_times)
        plt.xlabel('Time (months)')
        # Adding a y-axis label
        plt.ylabel('Probability of Relapse in Interval')
        # Customizing the title
        plt.title('Interval Relapse Probability Over Time for Maintenance and Discontinued Groups', fontsize=14)
        # Customizing legend
        plt.legend(loc='upper right')
        # Setting axis limits and grid
        plt.xlim(0, 13)
        plt.ylim(0, 0.4)
        plt.grid(True, linestyle='--', alpha=0.6)
        # Adding a horizontal line at y=0.5 for reference
        plt.axhline(y=0.5, color='gray', linestyle=':', linewidth=1)
        # Showing the plot
        plt.show()

    def plot_relapse_functions(self):

        x_interp = np.linspace(0, 13, 1000)  # Create a smooth x-axis
        f_maintenance = interp1d(self.sorted_time_values, self.interval_probs_maintenance, kind='cubic')
        f_discontinued = interp1d(self.sorted_time_values, self.interval_probs_discontinued, kind="quadratic")

        y_interp_maintenance = f_maintenance(x_interp)
        y_interp_discontinued = f_discontinued(x_interp)

        plt.figure(figsize=(12, 8))
        plt.plot(x_interp, y_interp_maintenance, label='Maintenance Group', linewidth=2)
        plt.plot(x_interp, y_interp_discontinued, label='Discontinued Group', linestyle='--', linewidth=2)
        # Customizing x-axis ticks and labels
        plt.xlabel('Time (months)')
        # Adding a y-axis label
        plt.ylabel('Probability of Relapse in Interval')
        # Customizing the title
        plt.title('Interval Relapse Probability Over Time for Maintenance and Discontinued Groups', fontsize=14)
        # Customizing legend
        plt.legend(loc='upper right')
        # Setting axis limits and grid
        plt.xlim(0, 13)
        plt.ylim(0, 0.4)
        plt.grid(True, linestyle='-', alpha=0.8)
        # Adding a horizontal line at y=0.5 for reference
        plt.axhline(y=0.5, color='gray', linestyle=':', linewidth=1)
        # Showing the plot
        plt.show()

    def plot_relapse(self):
        time_interval = np.arange(0, 52, 2)
        probs = [self.calculate_cumulative_probability(time, self.interval_probs_maintenance, self.sorted_times) for time in time_interval]

        # Create a plot for cumulative probabilities
        plt.figure(figsize=(10, 6))
        plt.plot(time_interval, probs, label='Group')
        plt.title('Cumulative Probability of Relapse Over Time')
        plt.xlabel('Time (months)')
        plt.ylabel('Cumulative Probability')
        plt.legend()
        plt.grid(True)
        plt.show()
    # plot_cumulative_probabilties(time_interval, interval_probs_maintenance, sorted_times, label="Maintenance")
    # plot_cumulative_probabilties(time_interval, interval_probs_discontinued, sorted_times, label="Discontinued")
    # Your data points

    def logistic_function(self, x, L, k, x0):
        return L / (1 + np.exp(-k * (x - x0)))

    def plot_cumulative_probabilities(self, group_type="maintenance"):
            time_interval = np.array([0, 1.5, 3, 6.5, 9.75, 13])  # Time points
            smooth_time = np.linspace(0, 13, 1000)  # More points for smoother curve

            probabilities_method = self.interval_probs_maintenance if group_type == "maintenance" else self.interval_probs_discontinued

            cumulative_probs, (params, _) = self.calculate_cumulative_params(probabilities_method)

            plt.figure(figsize=(10, 6))
            plt.plot(time_interval, cumulative_probs, 'o', label=f'{group_type.capitalize()} Group Data')
            plt.plot(smooth_time, self.logistic_function(smooth_time, *params), label=f'{group_type.capitalize()} Group Logistic Fit', linestyle='--')
            plt.title('Cumulative Probability of Relapse Over Time (Logistic Fit)')
            plt.xlabel('Time (months)')
            plt.ylabel('Cumulative Probability')
            plt.legend()
            plt.grid(True)
            plt.show()

            return cumulative_probs, params

    def calculate_cumulative_params(self, group_type="maintenance", specific_time=None):
        def logistic_function(x, L, k, x0):
            return L / (1 + np.exp(-k * (x - x0)))

        time_interval = specific_time if specific_time else np.array([0, 1.5, 3, 6.5, 9.75, 13])  # Time points image
        probabilities_method = self.interval_probs_maintenance if group_type == "maintenance" else self.interval_probs_discontinued

        cumulative_probs = [self.calculate_cumulative_probability(time, probabilities_method, self.sorted_times) for
                            time in time_interval]
        params, _ = curve_fit(logistic_function, time_interval, np.array(cumulative_probs), p0=(1, 1, 1))

        return cumulative_probs, params

    def return_probability_intervals(self, group_type="maintenance"):
        if group_type == "maintenance":
            return self.interval_probs_maintenance
        elif group_type == "discontinued":
            return self.interval_probs_discontinued
        else:
            raise ValueError(f"Don't have that group_type: {group_type}")

    def interpolate_probability_intervals(self, interval):
        # ensure timepoints and interval_probs are of same length
        assert len(interval) == len(self.sorted_time_values)

        # Create interpolation function using scipy interp1d
        interpolation_function = interp1d(list(self.sorted_time_values), interval, kind='cubic',
                                          fill_value="extrapolate")

        new_time_points = np.arange(0, 52+1, 1)  # Creating new set of time points from 1 to 52*4.34 (inclusive)

        # Get interpolated values for new set of timepoints
        interpolated_values = interpolation_function(new_time_points)

        # Normalize interpolated_values so they sum to 1
        interpolated_values /= interpolated_values.sum()

        return interpolated_values
    
    # @TOM HERE IS THE FUNCTION TO USE
    '''
    t: time to calculate, starts at week 0
    p: general probability to even relapse

    output: probability to relapse at time t
    '''
    def get_prob_at_time(self, t, type="maintenance", p=0.3):
        intervals = self.return_probability_intervals(group_type=type)
        interpolated_values = self.interpolate_probability_intervals(intervals)

        if t < len(interpolated_values):
            return interpolated_values[t] * p
        else:
            return 0.0

    def time_to_relapse(self, group_type="maintenance"):
        # Get the relapse probability intervals
        interval_probs = np.array(self.return_probability_intervals(group_type=group_type))

        # Transform these from interval probabilities to a cumulative distribution
        cumulative_probs = np.cumsum(interval_probs)

        # Draw a random number between 0 and 1
        random_prob = np.random.random()

        # Find the week this number lands at in the cumulative distribution
        relapse_week = np.searchsorted(cumulative_probs, random_prob)

        return relapse_week

    def plot_interpolated_probability_intervals(self, interval):
        # Get the interpolated probabilities
        interpolated_probabilities = self.interpolate_probability_intervals(interval)

        # Create a new set of time points in weeks
        new_time_points = np.arange(0, 52+1, 1)

        # Create the plot
        plt.figure(figsize=(10, 6))
        plt.plot(new_time_points, interpolated_probabilities, label='Interpolated Probabilities')
        plt.title('Interpolated Probability Intervals Over Time')
        plt.xlabel('Time (weeks)')
        plt.ylabel('Probability')
        plt.legend()
        plt.grid(True)
        plt.show()

