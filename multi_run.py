from BPTK_Py import SimultaneousScheduler
from data_collection import PatientDataCollector
import statistics as custom_stats
from hybrid_ABSD_model_eskt import DepressionTreatmentHybridABSD
from hybrid_ABSD_model_no_eskt import DepressionTreatmentHybridABSDWithoutEsketamine
from tqdm import tqdm
import plotter
import json
import os


def run(model, config):
    model.instantiate_model()
    model.configure(config)
    model.run()
    run_stats = model.statistics(),

    model_results_stats = {
        "run_statistics": run_stats,
        "aggregated_run_statistics": custom_stats.aggregated_single_run_statistics(model, config, run_stats)
    }

    return model_results_stats


if __name__ == "__main__":

    # Parameters
    CONFIG_FILE = "config_eskt.json"
    NUM_SIMULATIONS = 3
    SAVE_FILE = "aggregated_results.json"

    # Load config file
    pwd = os.path.dirname(os.path.realpath(__file__))
    config_file_path = os.path.join(pwd, "configs", CONFIG_FILE)
    with open(config_file_path, 'r') as file:
        config = json.load(file)

    runs = dict()
    runs["with_esketamine"] = {}
    runs["without_esketamine"] = {}

    print("Running with Esketamine")
    for sim_num in tqdm(range(NUM_SIMULATIONS)):
        model = DepressionTreatmentHybridABSD(name="Treatment pathway with Esketamie", scheduler=SimultaneousScheduler(), data_collector=PatientDataCollector())
        runs["with_esketamine"][f"sim_run_{sim_num}"] = run(model, config)

    print("Running without Esketamine")
    for sim_num in tqdm(range(NUM_SIMULATIONS)):
        model = DepressionTreatmentHybridABSDWithoutEsketamine(name="ETreatment pathway without Esketamie", scheduler=SimultaneousScheduler(), data_collector=PatientDataCollector())
        runs["without_esketamine"][f"sim_run_{sim_num}"] = run(model, config)

    save_file_path = os.path.join(pwd, "results", "runs_data_dump.json")
    with open(save_file_path, 'w') as file:
        json.dump(runs, file, indent=4)

    aggregated_statistics_results = custom_stats.aggregated_statistics(runs)

    save_file_path = os.path.join(pwd, "results", SAVE_FILE)
    with open(save_file_path, 'w') as file:
        json.dump(aggregated_statistics_results, file, indent=4)

    # Plotting
    plotter.plot_num_of_people_on_waiting_list_mean_multi_run(runs)
    plotter.plot_num_of_people_on_waiting_list_mean_multi_run(runs, with_or_without_esketamine="without_esketamine")
    plotter.plot_percentage_in_remission_multi_run(runs)
    plotter.plot_percentage_in_recovery_multi_run(runs)
