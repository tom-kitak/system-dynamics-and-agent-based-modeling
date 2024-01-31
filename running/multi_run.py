from BPTK_Py import SimultaneousScheduler
from utils.data_collection import PatientDataCollector
from models.hybrid_ABSD_model_eskt import DepressionTreatmentHybridABSD
from models.hybrid_ABSD_model_no_eskt import DepressionTreatmentHybridABSDWithoutEsketamine
from utils.capacity_allocation import capacity_allocation
from tqdm import tqdm
from utils import plotter, statistics as custom_stats
import json
import os
from datetime import datetime
import time


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
    NUM_SIMULATIONS = 10
    ESKETAMINE_CAPACITY_FRACTIONS = [0.1, 0.2, 0.4]

    AFTER_WEEKS_PLOT = 0
    CONFIG_FILE = "config_eskt.json"
    SAVE_FILE = "aggregated_results.json"

    # Load config file
    start_time = time.perf_counter()
    pwd = os.path.dirname(os.path.realpath(__file__))
    config_file_path = os.path.join(pwd, "../configs", CONFIG_FILE)

    runs = dict()
    metadata = dict()
    metadata["timedate"] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    for eskt_fraction in ESKETAMINE_CAPACITY_FRACTIONS:
        key = f"{int(eskt_fraction * 100)}%_with_esketamine"
        print(key)

        runs[key] = {}

        with open(config_file_path, 'r') as file:
            config_eskt = json.load(file)

        capacity_allocation(config_eskt, esketamine_fraction=eskt_fraction)

        for sim_num in tqdm(range(NUM_SIMULATIONS)):
            model = DepressionTreatmentHybridABSD(name="Treatment pathway with Esketamie", scheduler=SimultaneousScheduler(), data_collector=PatientDataCollector())
            runs[key][f"sim_run_{sim_num}"] = run(model, config_eskt)
        metadata[key] = config_eskt

    print("Running without Esketamine")
    runs["without_esketamine"] = {}

    with open(config_file_path, 'r') as file:
        config = json.load(file)

    capacity_allocation(config, esketamine_fraction=0.0)

    for sim_num in tqdm(range(NUM_SIMULATIONS)):
        model = DepressionTreatmentHybridABSDWithoutEsketamine(name="ETreatment pathway without Esketamie", scheduler=SimultaneousScheduler(), data_collector=PatientDataCollector())
        runs["without_esketamine"][f"sim_run_{sim_num}"] = run(model, config)
    metadata["without_esketamine"] = config

    save_file_path = os.path.join(pwd, "../results", "runs_data_dump.json")
    with open(save_file_path, 'w') as file:
        json.dump(runs, file, indent=4)

    aggregated_statistics_results = custom_stats.aggregated_statistics(runs)

    end_time = time.perf_counter()
    execution_time = end_time - start_time
    metadata["time_it_took_to_run_in_seconds"] = execution_time
    aggregated_statistics_results["metadata"] = metadata

    save_file_path = os.path.join(pwd, "../results", SAVE_FILE)
    with open(save_file_path, 'w') as file:
        json.dump(aggregated_statistics_results, file, indent=4)

    # Plotting
    for run_name, run_data in runs.items():
        plotter.plot_num_of_people_on_waiting_list_mean_multi_run(run_name, run_data, after_weeks=AFTER_WEEKS_PLOT)

    plotter.plot_percentage_in_remission_multi_run(runs, after_weeks=AFTER_WEEKS_PLOT)
    plotter.plot_percentage_in_recovery_multi_run(runs, after_weeks=AFTER_WEEKS_PLOT)
