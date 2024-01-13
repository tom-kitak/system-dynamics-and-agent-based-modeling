from BPTK_Py import SimultaneousScheduler
from data_collection import PatientDataCollector
from statistics.cost_calculation import direct_costs, indirect_costs
from statistics.qalys_calculation import average_qalys
from hybrid_ABSD_model import DepressionTreatmentHybridABSD
import plotter
import json
import os

if __name__ == "__main__":
    config_file = 'config_2.json'
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

    # plotter.plot_num_of_people_on_waiting_list(results)
    # plotter.plot_percentage_in_remission(results)

    total_direct_cost_of_the_system = direct_costs(depression_treatment_hybrid.agents, depression_treatment_hybrid_config)
    total_indirect_cost_of_the_system = indirect_costs(depression_treatment_hybrid.agents)
    print(f"Total direct cost of the system: {total_direct_cost_of_the_system} EUR")
    print(f"Direct cost per patient: {total_direct_cost_of_the_system // len(depression_treatment_hybrid.agents)} EUR")
    print(f"Total direct cost of the system: {total_indirect_cost_of_the_system} EUR")
    print(f"Direct cost per patient: {total_indirect_cost_of_the_system // len(depression_treatment_hybrid.agents)} EUR")
    print()
    print(f"Average QALYs: {average_qalys(depression_treatment_hybrid.agents)}")

    # for t, r in results.items():
    #     r = dict(sorted(r["person"].items()))
    #     print(f"T:{t}={r}")
