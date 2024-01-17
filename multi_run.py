from BPTK_Py import SimultaneousScheduler
from data_collection import PatientDataCollector
import statistics as custom_stats
from hybrid_ABSD_model_eskt import DepressionTreatmentHybridABSD
from hybrid_ABSD_model_no_eskt import DepressionTreatmentHybridABSDWithoutEsketamine
from tqdm import tqdm
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
    NUM_SIMULATIONS = 5
    SAVE_FILE = "run_one.json"

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

    aggregated_statistics_results = custom_stats.aggregated_statistics(runs)

    save_file_path = os.path.join(pwd, "results", SAVE_FILE)
    with open(save_file_path, 'w') as file:
        json.dump(aggregated_statistics_results, file, indent=4)
