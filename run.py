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
            ]
    }

    depression_treatment_hybrid.configure(depression_treatment_hybrid_config)
    depression_treatment_hybrid.run()

    results = depression_treatment_hybrid.statistics()

    for t, r in results.items():
        r = dict(sorted(r["person"].items()))
        print(f"T:{t}={r}")