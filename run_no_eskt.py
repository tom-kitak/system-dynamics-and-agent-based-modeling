from BPTK_Py import SimultaneousScheduler
from data_collection import PatientDataCollector
from statistics.cost_calculation import direct_costs_per_patient, indirect_costs_per_patient
from statistics.qalys_calculation import average_qalys
from hybrid_ABSD_model_no_eskt import DepressionTreatmentHybridABSDWithoutEsketamine
import plotter
import json
import os

if __name__ == "__main__":
    config_file = 'config_eskt.json'
    depression_treatment_hybrid_no_eskt = DepressionTreatmentHybridABSDWithoutEsketamine(name="Depression treatment",
                                                                                         scheduler=SimultaneousScheduler(),
                                                                                         data_collector=PatientDataCollector())

    depression_treatment_hybrid_no_eskt.instantiate_model()

    # Load config file
    pwd = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(pwd, "configs", config_file)
    with open(file_path, 'r') as file:
        depression_treatment_hybrid_config = json.load(file)

    depression_treatment_hybrid_no_eskt.configure(depression_treatment_hybrid_config)
    depression_treatment_hybrid_no_eskt.run()

    no_eskt_results = depression_treatment_hybrid_no_eskt.statistics()

    plotter.plot_num_of_people_on_waiting_list(no_eskt_results, plot_esketamine=False)
    plotter.plot_percentage_in_remission(no_eskt_results)

    print("NO ESKT")
    direct_costs = direct_costs_per_patient(depression_treatment_hybrid_no_eskt.agents, depression_treatment_hybrid_config)
    indirect_costs = indirect_costs_per_patient(depression_treatment_hybrid_no_eskt.agents)
    print(f"Direct   cost per patient: {direct_costs} EUR")
    print(f"Indirect cost per patient: {indirect_costs} EUR")
    print(f"Total    cost per patient: {direct_costs + indirect_costs} EUR")
    print(f"Fraction in remission:   {no_eskt_results[depression_treatment_hybrid_config['runspecs']['stoptime']]['percentage_in_remission']:.3f}")
    print(f"Average QALYs:             {average_qalys(depression_treatment_hybrid_no_eskt.agents):.3f}")

