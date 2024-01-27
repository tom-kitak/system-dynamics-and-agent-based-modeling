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


def add_metadata(runs):
    pass


if __name__ == "__main__":

    # Parameters
    CONFIG_FILE = "config_eskt.json"
    NUM_SIMULATIONS = 30
    SAVE_FILE = "aggregated_results.json"
    ESKETAMINE_FRACTION = 0.2

    # Load config file
    pwd = os.path.dirname(os.path.realpath(__file__))
    config_file_path = os.path.join(pwd, "../configs", CONFIG_FILE)
    with open(config_file_path, 'r') as file:
        config_eskt = json.load(file)

    with open(config_file_path, 'r') as file:
        config_no_eskt = json.load(file)

    # Esketamine percentages
    capacity_allocation(config_eskt, esketamine_fraction=ESKETAMINE_FRACTION)
    capacity_allocation(config_no_eskt, esketamine_fraction=0.0)

    runs = dict()
    runs["with_esketamine"] = {}
    runs["without_esketamine"] = {}

    print("Running with Esketamine")
    for sim_num in tqdm(range(NUM_SIMULATIONS)):
        model = DepressionTreatmentHybridABSD(name="Treatment pathway with Esketamie", scheduler=SimultaneousScheduler(), data_collector=PatientDataCollector())
        runs["with_esketamine"][f"sim_run_{sim_num}"] = run(model, config_eskt)

    print("Running without Esketamine")
    for sim_num in tqdm(range(NUM_SIMULATIONS)):
        model = DepressionTreatmentHybridABSDWithoutEsketamine(name="ETreatment pathway without Esketamie", scheduler=SimultaneousScheduler(), data_collector=PatientDataCollector())
        runs["without_esketamine"][f"sim_run_{sim_num}"] = run(model, config_no_eskt)

    save_file_path = os.path.join(pwd, "../results", "runs_data_dump.json")
    with open(save_file_path, 'w') as file:
        json.dump(runs, file, indent=4)

    aggregated_statistics_results = custom_stats.aggregated_statistics(runs)

    # Add metadata
    now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    aggregated_statistics_results["metadata"] = dict()
    aggregated_statistics_results["metadata"]["timedate"] = now
    aggregated_statistics_results["metadata"]["with_esketamine_config"] = config_eskt
    aggregated_statistics_results["metadata"]["without_esketamine_config"] = config_no_eskt

    save_file_path = os.path.join(pwd, "../results", SAVE_FILE)
    with open(save_file_path, 'w') as file:
        json.dump(aggregated_statistics_results, file, indent=4)

    # Plotting
    plotter.plot_num_of_people_on_waiting_list_mean_multi_run(runs, esketamine_fraction=ESKETAMINE_FRACTION)
    plotter.plot_num_of_people_on_waiting_list_mean_multi_run(runs, with_or_without_esketamine="without_esketamine")
    plotter.plot_percentage_in_remission_multi_run(runs, esketamine_fraction=ESKETAMINE_FRACTION)
    plotter.plot_percentage_in_recovery_multi_run(runs, esketamine_fraction=ESKETAMINE_FRACTION)
