

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
        self.in_anti_depressant = model.stock("in_anti_depressant")
        self.out_anti_depressant = model.stock("out_anti_depressant")
        self.in_anti_depressant_anti_psychotic = model.stock("in_anti_depressant_anti_psychotic")
        self.out_anti_depressant_anti_psychotic = model.stock("out_anti_depressant_anti_psychotic")
        self.in_anti_psychotic = model.stock("in_anti_psychotic")
        self.out_anti_psychotic = model.stock("out_anti_psychotic")
        self.in_esketamine = model.stock("in_esketamine")
        self.out_esketamine = model.stock("out_esketamine")
        self.in_ect = model.stock("in_ect")
        self.out_ect = model.stock("out_ect")

        # Waiting times
        self.in_anti_depressant_waiting_list = model.stock("in_anti_depressant_waiting_list")
        self.out_anti_depressant_waiting_list = model.stock("out_anti_depressant_waiting_list")
        self.in_anti_depressant_anti_psychotic_waiting_list = model.stock(
            "in_anti_depressant_anti_psychotic_waiting_list")
        self.out_anti_depressant_anti_psychotic_waiting_list = model.stock(
            "out_anti_depressant_anti_psychotic_waiting_list")
        self.in_anti_psychotic_waiting_list = model.stock("in_anti_psychotic_waiting_list")
        self.out_anti_psychotic_waiting_list = model.stock("out_anti_psychotic_waiting_list")
        self.in_esketamine_waiting_list = model.stock("in_esketamine_waiting_list")
        self.out_esketamine_waiting_list = model.stock("out_esketamine_waiting_list")
        self.in_ect_waiting_list = model.stock("in_ect_waiting_list")
        self.out_ect_waiting_list = model.stock("out_ect_waiting_list")

        # Health states
        self.in_remission = model.stock("in_remission")
        self.out_remission = model.stock("out_remission")
        self.in_recovery = model.stock("in_recovery")
        self.out_recovery = model.stock("out_recovery")
        self.in_relapse = model.stock("in_relapse")
        self.out_recovery = model.stock("out_recovery")

        # # Converters
        self.depression_treatment_demand = model.converter("depression_treatment_demand")

        # # Constants
        self.mild_depression_AD_rate = model.constant("mild_depression_AD_rate")

        # # Equations
        self.mild_depression_treatment_demand.equation = self.model.function("mild_depression_treatment_update",
            lambda m, t: m.exchange["mild_depression_treatment_demand"])()
        self.moderate_depression_treatment_demand.equation = self.model.function("moderate_depression_treatment_update",
            lambda m, t: m.exchange["moderate_depression_treatment_demand"])()
        self.severe_depression_treatment_demand.equation = self.model.function("severe_depression_treatment_update",
            lambda m, t: m.exchange["severe_depression_treatment_demand"])()

        self.AD.equation = self.AD_in - self.AD_out
        self.AD_AP.equation = self.AD_AP_in - self.AD_AP_out
        self.AP.equation = self.AP_in - self.AP_out
        self.esketamine.equation = self.esketamine_in - self.esketamine_out
        self.ECT.equation = self.ECT_in - self.ECT_out

        self.AD_in.equation = self.mild_depression_treatment_demand * self.mild_depression_AD_rate \
                              + self.moderate_depression_treatment_demand * self.moderate_depression_AD_rate \
                              + self.severe_depression_treatment_demand * self.severe_depression_AD_rate
        self.AD_AP_in.equation = self.mild_depression_treatment_demand * self.mild_depression_AD_AP_rate \
                              + self.moderate_depression_treatment_demand * self.moderate_depression_AD_AP_rate \
                              + self.severe_depression_treatment_demand * self.severe_depression_AD_AP_rate
        self.AP_in.equation = self.mild_depression_treatment_demand * self.mild_depression_AP_rate \
                              + self.moderate_depression_treatment_demand * self.moderate_depression_AP_rate \
                              + self.severe_depression_treatment_demand * self.severe_depression_AP_rate

        self.AD_out.equation = self.model.function("AD_finished_treatment",
                                                   lambda m, t: m.exchange["AD_finished_treatment"])()
        self.AD_AP_out.equation = self.model.function("AD_AP_finished_treatment",
                                                   lambda m, t: m.exchange["AD_AP_finished_treatment"])()
        self.AP_out.equation = self.model.function("AP_finished_treatment",
                                                   lambda m, t: m.exchange["AP_finished_treatment"])()

        self.remission.equation = self.model.function("remission_update", lambda m, t: m.exchange["remission"])()
        self.second_line_treatment_demand.equation = self.AD_out + self.AD_AP_out + self.AP_out - self.remission

        self.esketamine_in.equation = self.model.function("esketamine_flow",
            lambda m, t: min(self.esketamine_capacity, self.second_line_treatment_demand))()
        self.ECT_in = self.second_line_treatment_demand - self.esketamine_in

        self.esketamine_out = self.model.function("esketamine_finished_treatment",
                                    lambda m, t: m.exchange["esketamine_finished_treatment"])()
        self.ECT_out = self.model.function("ECT_finished_treatment",
                                    lambda m, t: m.exchange["ECT_finished_treatment"])()

        # # Initial values
        # self.treated.initial_value = 0.0
