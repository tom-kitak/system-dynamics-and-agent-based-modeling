from BPTK_Py import DataCollector
from BPTK_Py import SimultaneousScheduler
from data_collection import PatientDataCollector
from hybrid_ABSD_model import DepressionTreatmentHybridABSD
import json
import os


if __name__ == "__main__":
    config_file = 'config.json'
    depression_treatment_hybrid = DepressionTreatmentHybridABSD(name="Depression treatment",
                                                                scheduler=SimultaneousScheduler(),
                                                                data_collector=DataCollector())

    depression_treatment_hybrid.instantiate_model()

    # Load config file
    pwd = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(pwd, "configs", config_file)
    with open(file_path, 'r') as file:
        depression_treatment_hybrid_config = json.load(file)

    depression_treatment_hybrid.configure(depression_treatment_hybrid_config)
    depression_treatment_hybrid.run()

    results = depression_treatment_hybrid.statistics()

    # print(results)

    # for t, r in results.items():
    #     # print(f"T:{t}={r['total_monetary_cost']}")
    #     print(f"T:{t}={r['waiting_list_count']}")

    print("------------")

    for t, r in results.items():
        r = dict(sorted(r["person"].items()))
        print(f"T:{t}={r}")
        count = 0
        for treatment, count_dict in r.items():
            count += count_dict["count"]
        print(count)
