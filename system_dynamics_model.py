

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
        self.relapse = model.stock("relapse")

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
        self.in_relapse = model.flow("in_relapse")
        self.out_relapse = model.flow("out_relapse")

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
        self.relapse.equation = self.in_relapse - self.out_relapse

        # Gets the demand from the AB model
        self.depression_treatment_demand.equation = self.model.function("depression_treatment_demand_update",
            lambda m, t: m.exchange["depression_treatment_demand"])()

        # These are based on Julia's percentages from the decision tree
        self.in_antidepressant_waiting_list.equation = self.antidepressant_allocation_percentage * self.depression_treatment_demand
        self.in_antidepressant_antipsychotic_waiting_list.equation = self.antidepressant_antipsychotic_allocation_percentage * self.depression_treatment_demand
        self.in_antipsychotic_waiting_list.equation = self.antipsychotic_allocation_percentage * self.depression_treatment_demand

        # Starting treatment
        self.out_antidepressant = self.model.function("out_antidepressant_update",
            lambda m, t: m.exchange["out_antidepressant"])()
        self.in_antidepressant = self.antidepressant_capacity - self.antidepressant

        # # Initial values
        # NOTE: These values are from Julia's decision tree thingy, probably going to change
        self.antidepressant_allocation_percentage.equation = 59.915
        self.antidepressant_antipsychotic_allocation_percentage.equation = 35.254999999999995
        self.antipsychotic_allocation_percentage.equation = 4.83

        # self.mild_depression_treatment_demand.equation = self.model.function("mild_depression_treatment_update",
            # lambda m, t: m.exchange["mild_depression_treatment_demand"])()
