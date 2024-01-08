from BPTK_Py import DataCollector
from BPTK_Py import SimultaneousScheduler
from data_collection import PatientDataCollector
from hybrid_ABSD_model import DepressionTreatmentHybridABSD
import json
import os
import plotter


if __name__ == "__main__":
    config_file = 'config.json'
    depression_treatment_hybrid = DepressionTreatmentHybridABSD(name="Depression treatment",
                                                                scheduler=SimultaneousScheduler(),
                                                                data_collector=PatientDataCollector())

    depression_treatment_hybrid.instantiate_model()

    # Load config file
    pwd = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(pwd, "configs", config_file)
    with open(file_path, 'r') as file:
        depression_treatment_hybrid_config = json.load(file)

    depression_treatment_hybrid.configure(depression_treatment_hybrid_config)
    depression_treatment_hybrid.run()

    results = depression_treatment_hybrid.statistics()

    plotter.plot_num_of_people_on_waiting_list(results)
    plotter.plot_percentage_in_remission(results)

    # for t, r in results.items():
    #     r = dict(sorted(r["person"].items()))
    #     print(f"T:{t}={r}")
