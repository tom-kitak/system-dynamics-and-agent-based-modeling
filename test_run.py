from BPTK_Py import SimultaneousScheduler
from data_collection import PatientDataCollector
from hybrid_ABSD_model_no_eskt import DepressionTreatmentHybridABSDWithoutEsketamine
from hybrid_ABSD_model_eskt import DepressionTreatmentHybridABSD
import plotter
import json
import os

if __name__ == "__main__":
    config_file = 'config_eskt.json'
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

    results_datacollector = depression_treatment_hybrid.statistics()

    plotter.plot_num_of_people_on_waiting_list(results_datacollector, plot_esketamine=False)
    plotter.plot_percentage_in_remission(results_datacollector)
    plotter.plot_percentage_in_recovery(results_datacollector)
