

class DepressionTreatmentSystemDynamics:
    def __init__(self, model):
        self.model = model

        # # Stocks
        # Treatments
        self.anti_depressant = model.stock("anti_depressant")
        self.anti_depressant_anti_psychotic = model.stock("anti_depressant_anti_psychotic")
        self.anti_psychotic = model.stock("anti_psychotic")
        self.esketamine = model.stock("esketamine")
        self.ect = model.stock("ect")

        # Waiting times
        self.anti_depressant_waiting_list = model.stock("anti_depressant_waiting_list")
        self.anti_depressant_anti_psychotic_waiting_list = model.stock("anti_depressant_anti_psychotic_waiting_list")
        self.anti_psychotic_waiting_list = model.stock("anti_psychotic_waiting_list")
        self.esketamine_waiting_list = model.stock("esketamine_waiting_list")
        self.ect_waiting_list = model.stock("ect_waiting_list")

        # Health states
        self.remission = model.stock("remission")
        self.recovery = model.stock("recovery")
        self.relapse = model.stock("relapse")

        # # Flows
        # Treatments
        self.in_anti_depressant = model.flow("in_anti_depressant")
        self.out_anti_depressant = model.flow("out_anti_depressant")
        self.in_anti_depressant_anti_psychotic = model.flow("in_anti_depressant_anti_psychotic")
        self.out_anti_depressant_anti_psychotic = model.flow("out_anti_depressant_anti_psychotic")
        self.in_anti_psychotic = model.flow("in_anti_psychotic")
        self.out_anti_psychotic = model.flow("out_anti_psychotic")
        self.in_esketamine = model.flow("in_esketamine")
        self.out_esketamine = model.flow("out_esketamine")
        self.in_ect = model.flow("in_ect")
        self.out_ect = model.flow("out_ect")

        # Waiting times
        self.in_anti_depressant_waiting_list = model.flow("in_anti_depressant_waiting_list")
        self.out_anti_depressant_waiting_list = model.flow("out_anti_depressant_waiting_list")
        self.in_anti_depressant_anti_psychotic_waiting_list = model.flow(
            "in_anti_depressant_anti_psychotic_waiting_list")
        self.out_anti_depressant_anti_psychotic_waiting_list = model.flow(
            "out_anti_depressant_anti_psychotic_waiting_list")
        self.in_anti_psychotic_waiting_list = model.flow("in_anti_psychotic_waiting_list")
        self.out_anti_psychotic_waiting_list = model.flow("out_anti_psychotic_waiting_list")
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
        self.anti_depressant_allocation_percentage = model.constant("anti_depressant_allocation_percentage")
        self.anti_depressant_anti_psychotic_allocation_percentage = model.constant(
            "anti_depressant_anti_psychotic_allocation_percentage")
        self.anti_psychotic_allocation_percentage = model.constant("anti_psychotic_allocation_percentage")


        # # Equations
        
        # Treatments flow
        self.anti_depressant.equation = self.in_anti_depressant - self.out_anti_depressant
        self.anti_depressant_anti_psychotic.equation = self.in_anti_depressant_anti_psychotic - self.out_anti_depressant_anti_psychotic
        self.anti_psychotic.equation = self.in_anti_psychotic - self.out_anti_psychotic
        self.esketamine.equation = self.in_esketamine - self.out_esketamine
        self.ect.equation = self.in_ect - self.out_ect

        # Waiting times flow
        self.anti_depressant_waiting_list.equation = self.in_anti_depressant_waiting_list - self.out_anti_depressant_waiting_list
        self.anti_depressant_anti_psychotic_waiting_list.equation = self.in_anti_depressant_anti_psychotic_waiting_list - self.out_anti_depressant_anti_psychotic_waiting_list
        self.anti_psychotic_waiting_list.equation = self.in_anti_psychotic_waiting_list - self.out_anti_psychotic_waiting_list
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
        self.in_anti_depressant_waiting_list.equation = self.anti_depressant_allocation_percentage * self.depression_treatment_demand
        self.in_anti_depressant_anti_psychotic_waiting_list.equation = self.anti_depressant_anti_psychotic_allocation_percentage * self.depression_treatment_demand
        self.in_anti_psychotic_waiting_list.equation = self.anti_psychotic_allocation_percentage * self.depression_treatment_demand

        

        # # Initial values
        # NOTE: These values are from Julia's decision tree thingy, probably going to change
        self.anti_depressant_allocation_percentage.equation = 59.915
        self.anti_depressant_anti_psychotic_allocation_percentage.equation = 35.254999999999995
        self.anti_psychotic_allocation_percentage.equation = 4.83

        # self.mild_depression_treatment_demand.equation = self.model.function("mild_depression_treatment_update",
            # lambda m, t: m.exchange["mild_depression_treatment_demand"])()
