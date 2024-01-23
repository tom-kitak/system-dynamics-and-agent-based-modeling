def capacity_allocation(config, esketamine_fraction=0.2):
    """
    It uses percentiles defined in config["capacities"] for every treatment.
    Esketamine percenrage can be overwritten by the argument esketamine_fraction, and esketamine is always
    guarantted to get the specified fraction, while other treatmetns redistribute what is left based on the new percentages.
    """
    total = config["capacities"]["total"]
    config["treatment_properties"]["esketamine"]["capacity"] = round(total * esketamine_fraction)

    dynamic_fraction_left = 1.0 - esketamine_fraction
    config_fraction_left = 1.0 - config["capacities"]["esketamine"]

    fraction = dynamic_fraction_left / config_fraction_left

    config["capacities"]["antidepressant"] = fraction * config["capacities"]["antidepressant"]
    config["capacities"]["antidepressant_antipsychotic"] = fraction * config["capacities"]["antidepressant_antipsychotic"]
    config["capacities"]["antipsychotic"] = fraction * config["capacities"]["antipsychotic"]
    config["capacities"]["ect"] = fraction * config["capacities"]["ect"]

    config["treatment_properties"]["antidepressant"]["capacity"] = round(total * config["capacities"]["antidepressant"])
    config["treatment_properties"]["antidepressant_antipsychotic"]["capacity"] = round(total * config["capacities"]["antidepressant_antipsychotic"])
    config["treatment_properties"]["antipsychotic"]["capacity"] = round(total * config["capacities"]["antipsychotic"])
    config["treatment_properties"]["ect"]["capacity"] = round(total * config["capacities"]["ect"])

    config["capacities"]["esketamine"] = esketamine_fraction

    return config
