from BPTK_Py import sd_functions as sd


class DepressionTreatmentSystemDynamics:
    def __init__(self, model):
        self.model = model

        # # Stocks
        # Treatments
        self.antidepressant = model.stock("antidepressant")
        self.antidepressant_antipsychotic = model.stock("antidepressant_antipsychotic")
        self.antipsychotic = model.stock("antipsychotic")
        self.esketamine = model.stock("esketamine")
        self.ect = model.stock("ect")

        # Waiting times
        self.antidepressant_waiting_list = model.stock("antidepressant_waiting_list")
        self.antidepressant_antipsychotic_waiting_list = model.stock("antidepressant_antipsychotic_waiting_list")
        self.antipsychotic_waiting_list = model.stock("antipsychotic_waiting_list")
        self.esketamine_waiting_list = model.stock("esketamine_waiting_list")
        self.ect_waiting_list = model.stock("ect_waiting_list")

        # Health states
        self.remission = model.stock("remission")
        self.recovery = model.stock("recovery")

        # # Flows
        # Treatments
        self.in_antidepressant = model.flow("in_antidepressant")
        self.out_antidepressant = model.flow("out_antidepressant")
        self.in_antidepressant_antipsychotic = model.flow("in_antidepressant_antipsychotic")
        self.out_antidepressant_antipsychotic = model.flow("out_antidepressant_antipsychotic")
        self.in_antipsychotic = model.flow("in_antipsychotic")
        self.out_antipsychotic = model.flow("out_antipsychotic")
        self.in_esketamine = model.flow("in_esketamine")
        self.out_esketamine = model.flow("out_esketamine")
        self.in_ect = model.flow("in_ect")
        self.out_ect = model.flow("out_ect")

        # Waiting times
        self.in_antidepressant_waiting_list = model.flow("in_antidepressant_waiting_list")
        self.out_antidepressant_waiting_list = model.flow("out_antidepressant_waiting_list")
        self.in_antidepressant_antipsychotic_waiting_list = model.flow(
            "in_antidepressant_antipsychotic_waiting_list")
        self.out_antidepressant_antipsychotic_waiting_list = model.flow(
            "out_antidepressant_antipsychotic_waiting_list")
        self.in_antipsychotic_waiting_list = model.flow("in_antipsychotic_waiting_list")
        self.out_antipsychotic_waiting_list = model.flow("out_antipsychotic_waiting_list")
        self.in_esketamine_waiting_list = model.flow("in_esketamine_waiting_list")
        self.out_esketamine_waiting_list = model.flow("out_esketamine_waiting_list")
        self.in_ect_waiting_list = model.flow("in_ect_waiting_list")
        self.out_ect_waiting_list = model.flow("out_ect_waiting_list")

        # Health states
        self.in_remission = model.flow("in_remission")
        self.out_remission = model.flow("out_remission")
        self.in_recovery = model.flow("in_recovery")
        self.out_recovery = model.flow("out_recovery")

        # # Converters
        self.depression_treatment_demand = model.converter("depression_treatment_demand")

        # # Constants
        self.antidepressant_allocation_percentage = model.constant("antidepressant_allocation_percentage")
        self.antidepressant_antipsychotic_allocation_percentage = model.constant(
            "antidepressant_antipsychotic_allocation_percentage")
        self.antipsychotic_allocation_percentage = model.constant("antipsychotic_allocation_percentage")

        # Capacities
        self.antidepressant_capacity = model.constant("antidepressant_capacity")
        self.antidepressant_antipsychotic_capacity = model.constant("antidepressant_antipsychotic_capacity")
        self.antipsychotic_capacity = model.constant("antipsychotic_capacity")
        self.esketamine_capacity = model.constant("esketamine_capacity")
        self.ect_capacity = model.constant("ect_capacity")

        # # Equations
        
        # Treatments flow
        self.antidepressant.equation = self.in_antidepressant - self.out_antidepressant
        self.antidepressant_antipsychotic.equation = self.in_antidepressant_antipsychotic - self.out_antidepressant_antipsychotic
        self.antipsychotic.equation = self.in_antipsychotic - self.out_antipsychotic
        self.esketamine.equation = self.in_esketamine - self.out_esketamine
        self.ect.equation = self.in_ect - self.out_ect

        # Waiting times flow
        self.antidepressant_waiting_list.equation = self.in_antidepressant_waiting_list - self.out_antidepressant_waiting_list
        self.antidepressant_antipsychotic_waiting_list.equation = self.in_antidepressant_antipsychotic_waiting_list - self.out_antidepressant_antipsychotic_waiting_list
        self.antipsychotic_waiting_list.equation = self.in_antipsychotic_waiting_list - self.out_antipsychotic_waiting_list
        self.esketamine_waiting_list.equation = self.in_esketamine_waiting_list - self.out_esketamine_waiting_list
        self.ect_waiting_list.equation = self.in_ect_waiting_list - self.out_ect_waiting_list

        # Health states flow
        self.remission.equation = self.in_remission - self.out_remission
        self.recovery.equation = self.in_recovery - self.out_recovery

        # Interesting part:
        # Gets the demand from the AB model
        self.depression_treatment_demand.equation = self.model.function("depression_treatment_demand_update",
            lambda m, t: m.exchange["depression_treatment_demand"])()

        # These are based on Julia's percentages from the decision tree
        # Enter first-line waiting lists
        self.in_antidepressant_waiting_list.equation = self.model.function("in_antidepressant_waiting_list_update",
            lambda m, t, antidepressant_allocation_percentage, depression_treatment_demand:
            m.exchange["in_antidepressant_waiting_list"] +
            antidepressant_allocation_percentage * depression_treatment_demand)(self.antidepressant_allocation_percentage, self.depression_treatment_demand)
        self.in_antidepressant_antipsychotic_waiting_list.equation = self.antidepressant_antipsychotic_allocation_percentage * self.depression_treatment_demand
        self.in_antipsychotic_waiting_list.equation = self.antipsychotic_allocation_percentage * self.depression_treatment_demand

        # Starting first-line treatment
        self.out_antidepressant_waiting_list.equation = sd.min(self.antidepressant_waiting_list, self.antidepressant_capacity - self.antidepressant)
        self.in_antidepressant.equation = self.out_antidepressant_waiting_list

        self.out_antidepressant_antipsychotic_waiting_list.equation = sd.min(self.antidepressant_antipsychotic_waiting_list, self.antidepressant_antipsychotic_capacity - self.antidepressant_antipsychotic)
        self.in_antidepressant_antipsychotic.equation = self.out_antidepressant_antipsychotic_waiting_list

        self.out_antipsychotic_waiting_list.equation = sd.min(self.antipsychotic_waiting_list, self.antipsychotic_capacity - self.antipsychotic)
        self.in_antipsychotic.equation = self.out_antipsychotic_waiting_list

        # Exit first-line treatment
        self.out_antidepressant.equation = self.model.function("out_antidepressant_update",
            lambda m, t: m.exchange["out_antidepressant"])()
        self.out_antidepressant_antipsychotic.equation = self.model.function("out_antidepressant_antipsychotic_update",
            lambda m, t: m.exchange["out_antidepressant_antipsychotic"])()
        self.out_antipsychotic.equation = self.model.function("out_antipsychotic_update",
            lambda m, t: m.exchange["out_antipsychotic"])()

        # Enter second-line waiting list
        self.in_esketamine_waiting_list.equation = self.model.function("in_esketamine_waiting_list_update",
            lambda m, t: m.exchange["in_esketamine_waiting_list"])()

        # Start second-line treatment
        self.out_esketamine_waiting_list.equation = sd.min(self.esketamine_waiting_list, self.esketamine_capacity - self.esketamine)
        self.in_esketamine.equation = self.out_esketamine_waiting_list

        # Exit second-line treatment
        self.out_esketamine.equation = self.model.function("out_esketamine_update",
            lambda m, t: m.exchange["out_esketamine"])()

        # Enter third-line waiting list
        self.in_ect_waiting_list.equation = self.model.function("in_ect_waiting_list_update",
            lambda m, t: m.exchange["in_ect_waiting_list"])()

        # Start third-line treatment
        self.out_ect_waiting_list.equation = sd.min(self.ect_waiting_list, self.ect_capacity - self.ect)
        self.in_ect.equation = self.out_ect_waiting_list

        # Exit third-line treatment
        self.out_ect.equation = self.model.function("out_ect_update",
            lambda m, t: m.exchange["out_ect"])()

        # Enter remission
        self.in_remission.equation = self.model.function("in_remission_update",
            lambda m, t: m.exchange["in_remission"])()

        # Exit remission
        self.out_remission.equation = self.model.function("out_remission_update",
            lambda m, t: m.exchange["out_remission"])()

        # Enter recovery
        self.in_recovery.equation = self.model.function("in_recovery_update",
            lambda m, t: m.exchange["in_recovery"])()

        # Exit recovery
        self.out_recovery.equation = self.model.function("out_recovery_update",
            lambda m, t: m.exchange["out_recovery"])()

        # # Initial values
        # NOTE: These values are from Julia's decision tree thingy, probably going to change
        # TODO: don't use hard cutoffs because then AP can only be seen when there are more than 20 patients per week
        self.antidepressant_allocation_percentage.equation = 0.60
        self.antidepressant_antipsychotic_allocation_percentage.equation = 0.35
        self.antipsychotic_allocation_percentage.equation = 0.05
