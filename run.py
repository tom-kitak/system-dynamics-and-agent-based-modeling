from BPTK_Py import DataCollector
from BPTK_Py import SimultaneousScheduler
from hybrid_ABSD_model import DepressionTreatmentHybridABSD


if __name__ == "__main__":
    depression_treatment_hybrid = DepressionTreatmentHybridABSD(name="Depression treatment",
                                                                scheduler=SimultaneousScheduler(),
                                                                data_collector=DataCollector())

    depression_treatment_hybrid.instantiate_model()

    depression_treatment_hybrid_config = {
        "runspecs": {
            "starttime": 1,
            "stoptime": 10,
            "dt": 1.0
        },
        "properties":
            {
                "treatment_success_rate":
                    {
                        "type": "Double",
                        "value": 0.5
                    },
                "enter_treatment_rate":
                    {
                        "type": "Double",
                        "value": 0.8
                    },
            },
        "agents":
            [
                {
                    "name": "person",
                    "count": 100,
                    "properties": {
                        "monetary_cost": {
                            "type": "Integer",
                            "value": 0
                        }
                    }
                }
            ],
        "treatment_properties":
            {
                "esketamine": {
                    "duration": 26,
                    "cost": 10000,
                    "response_rate": 0.784,
                    "remission_rate": 0.472,
                    "relapse_rate": 0.054,
                    "suicide_rate": 0,
                    "treatment_adherence": 0.937,
                    "mean_delta_madrs": -16.4,
                    "sd_delta_madrs": 8.76
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
                    "sd_delta_madrs": 0.8245
                }
            }
    }

    depression_treatment_hybrid.configure(depression_treatment_hybrid_config)
    depression_treatment_hybrid.run()

    results = depression_treatment_hybrid.statistics()

    for t, r in results.items():
        r = dict(sorted(r["person"].items()))
        print(f"T:{t}={r}")