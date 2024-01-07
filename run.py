from BPTK_Py import DataCollector
from BPTK_Py import SimultaneousScheduler
from data_collection import PatientDataCollector
from hybrid_ABSD_model import DepressionTreatmentHybridABSD


if __name__ == "__main__":
    depression_treatment_hybrid = DepressionTreatmentHybridABSD(name="Depression treatment",
                                                                scheduler=SimultaneousScheduler(),
                                                                data_collector=DataCollector())

    depression_treatment_hybrid.instantiate_model()

    # TODO:LOW load it from a .json file
    depression_treatment_hybrid_config = {
        "runspecs": {
            "starttime": 1,
            "stoptime": 30,
            "dt": 1.0
        },
        "properties":
            {
                "treatment_success_rate":
                    {
                        "type": "Double",
                        "value": 0.5
                    }
            },
        "agents":
            [
                {
                    "name": "person",
                    "count": 100,
                }
            ],
        "new_patients_per_week": 5,
        "treatment_properties":
            {
                "esketamine": {
                    "duration": 6,
                    "cost": 10000,
                    "response_rate": 0.784,
                    "remission_rate": 0.472,
                    "relapse_rate": 0.054,
                    "suicide_rate": 0,
                    "treatment_adherence": 0.937,
                    "mean_delta_madrs": -16.4,
                    "sd_delta_madrs": 8.76,
                    "capacity": 10
                },
                "antipsychotic": {
                    "duration": 4,
                    "cost": 6000,
                    "response_rate": 0.507,
                    "remission_rate": 0.2978,
                    "relapse_rate": 0.043,
                    "suicide_rate": 0,
                    "treatment_adherence": 0.873,
                    "mean_delta_madrs": -15.05,
                    "sd_delta_madrs": 0.8245,
                    "capacity": 10
                },
                "antidepressant_antipsychotic": {
                    "duration": 4, 
                    "cost": 7200, 
                    "response_rate": 0.524, 
                    "remission_rate": 0.3886, 
                    "relapse_rate": 0.035, 
                    "suicide_rate": 0, 
                    "treatment_adherence": 0.9355, 
                    "mean_delta_madrs": -16.15, 
                    "sd_delta_madrs": 0.8115,
                    "capacity": 10
                },
                "antidepressant": {
                    "duration": 4, 
                    "cost": 5000, 
                    "response_rate": 0.402, 
                    "remission_rate": 0.34, 
                    "relapse_rate": 0.055, 
                    "suicide_rate": 0, 
                    "treatment_adherence": 0.944, 
                    "mean_delta_madrs": -13, 
                    "sd_delta_madrs": 3.5,
                    "capacity": 10
                },
                "ect": {
                    "duration": 4, 
                    "cost": 8000, 
                    "response_rate": 0.414, 
                    "remission_rate": 0.591, 
                    "relapse_rate": 0.015, 
                    "suicide_rate": 0, 
                    "treatment_adherence": 0.874, 
                    "mean_delta_madrs": -15.5, 
                    "sd_delta_madrs": 4,
                    "capacity": 10
                }
            }
    }

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
