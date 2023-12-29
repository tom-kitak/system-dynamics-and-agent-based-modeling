from BPTK_Py import Model
from system_dynamics_model import DepressionTreatmentSystemDynamics
from agent_based_model import Person


class DepressionTreatmentHybridABSD(Model):
    def instantiate_model(self):
        super().instantiate_model()
        self.register_agent_factory("person", lambda agent_id, model, properties: Person(agent_id, model, properties))

        self.sd_model = None
        self.exchange = {}
        self.exchange["mild_depression_treatment_demand"] = 0
        self.exchange["moderate_depression_treatment_demand"] = 0
        self.exchange["severe_depression_treatment_demand"] = 0

        self.exchange["AD_finished_treatment"] = 0
        self.exchange["AD_AP_finished_treatment"] = 0
        self.exchange["AP_finished_treatment"] = 0

        self.exchange["remission"] = 0


    def configure(self, config):
        super().configure(config)
        self.sd_model = DepressionTreatmentSystemDynamics(self)

        self.sd_model.treatment_success_rate.equation = self.treatment_success_rate
        self.sd_model.enter_treatment_rate.equation = self.enter_treatment_rate

    def end_round(self, time, sim_round, step):

        depression_demand = 0
        update_enter_treatment = int(self.evaluate_equation("enter_treatment", time))
        update_untreated = int(self.evaluate_equation("untreated", time))
        update_outgoing_patients = int(self.evaluate_equation("outgoing_patients", time))

        for agent in self.agents:
            if agent.state == "depression":
                depression_demand += 1
                if update_enter_treatment > 0:
                    agent.state = "depression_treated"
                    update_enter_treatment -= 1
                elif update_untreated > 0:
                    agent.state = "depression_untreated"
                    update_untreated -= 1
            elif agent.state == "depression_treated":
                if update_outgoing_patients > 0:
                    agent.state = "healthy_treated"
                    update_outgoing_patients -= 1
                else:
                    # Adding monetary costs for as long as they are treated
                    treatment_cost = 1
                    agent.set_property_value("monetary_cost", agent.get_property_value("monetary_cost")
                                             + treatment_cost)
        # print("+++++++++++++++++++++++++++++++++")
        # print(f"Hybrid time:          {time}")
        # print(f"Hybrid dep demand:    {depression_demand}")
        self.exchange["depression_demand"] = depression_demand