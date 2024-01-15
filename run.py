from BPTK_Py import SimultaneousScheduler
from data_collection import PatientDataCollector
from statistics.cost_calculation import direct_costs_per_patient, indirect_costs_per_patient
from statistics.qalys_calculation import average_qalys
from hybrid_ABSD_model_eskt import DepressionTreatmentHybridABSD
from hybrid_ABSD_model_no_eskt import DepressionTreatmentHybridABSDWithoutEsketamine
import plotter
import json
import os

if __name__ == "__main__":

    # Load config file
    config_file = 'config_eskt.json'
    pwd = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(pwd, "configs", config_file)
    with open(file_path, 'r') as file:
        depression_treatment_hybrid_config = json.load(file)

    # ESKT
    depression_treatment_hybrid_eskt = DepressionTreatmentHybridABSD(name="Depression treatment",
                                                                     scheduler=SimultaneousScheduler(),
                                                                     data_collector=PatientDataCollector())
    depression_treatment_hybrid_eskt.instantiate_model()
    depression_treatment_hybrid_eskt.configure(depression_treatment_hybrid_config)
    depression_treatment_hybrid_eskt.run()
    eskt_results = depression_treatment_hybrid_eskt.statistics()

    # NO ESKT
    depression_treatment_hybrid_no_eskt = DepressionTreatmentHybridABSDWithoutEsketamine(name="Depression treatment",
                                                                                         scheduler=SimultaneousScheduler(),
                                                                                         data_collector=PatientDataCollector())
    depression_treatment_hybrid_no_eskt.instantiate_model()
    depression_treatment_hybrid_no_eskt.configure(depression_treatment_hybrid_config)
    depression_treatment_hybrid_no_eskt.run()
    no_eskt_results = depression_treatment_hybrid_no_eskt.statistics()

    print("ESKT")

    plotter.plot_num_of_people_on_waiting_list(eskt_results)
    plotter.plot_percentage_in_remission(eskt_results)

    direct_costs_eskt = direct_costs_per_patient(depression_treatment_hybrid_eskt.agents, depression_treatment_hybrid_config)
    indirect_costs_eskt = indirect_costs_per_patient(depression_treatment_hybrid_eskt.agents)
    total_costs_eskt = direct_costs_eskt + indirect_costs_eskt
    average_qalys_eskt = average_qalys(depression_treatment_hybrid_eskt.agents)
    print(f"Direct   cost per patient: {direct_costs_eskt} EUR")
    print(f"Indirect cost per patient: {indirect_costs_eskt} EUR")
    print(f"Total    cost per patient: {total_costs_eskt} EUR")
    print(f"Fraction in remission:     {eskt_results[depression_treatment_hybrid_config['runspecs']['stoptime']]['percentage_in_remission']:.3f}")
    print(f"Average QALYs:             {average_qalys_eskt:.3f}")

    print("============================")
    print("NO ESKT")

    plotter.plot_num_of_people_on_waiting_list(no_eskt_results, plot_esketamine=False)
    plotter.plot_percentage_in_remission(no_eskt_results, title="No Esketamine")

    direct_costs_no_eskt = direct_costs_per_patient(depression_treatment_hybrid_no_eskt.agents, depression_treatment_hybrid_config)
    indirect_costs_no_eskt = indirect_costs_per_patient(depression_treatment_hybrid_no_eskt.agents)
    total_costs_no_eskt = direct_costs_no_eskt + indirect_costs_no_eskt
    average_qalys_no_eskt = average_qalys(depression_treatment_hybrid_no_eskt.agents)
    print(f"Direct   cost per patient: {direct_costs_no_eskt} EUR")
    print(f"Indirect cost per patient: {indirect_costs_no_eskt} EUR")
    print(f"Total    cost per patient: {total_costs_no_eskt} EUR")
    print(f"Fraction in remission:     {no_eskt_results[depression_treatment_hybrid_config['runspecs']['stoptime']]['percentage_in_remission']:.3f}")
    print(f"Average QALYs:             {average_qalys_no_eskt:.3f}")


    print("============================")

    incremental_cost = total_costs_eskt - total_costs_no_eskt
    incremental_effectiveness = average_qalys_eskt - average_qalys_no_eskt
    icer = incremental_cost / incremental_effectiveness
    print(f"Incremental Cost-effectiveness ratio (ICER):{icer:.3f}")

    willingness_to_pay_threshold = 50000
    nmb = willingness_to_pay_threshold * incremental_effectiveness - incremental_cost
    print(f"Net-monetary-benefit (NMB):                 {nmb:.3f}")


