from BPTK_Py import Model
from system_dynamics_model import DepressionTreatmentSystemDynamics
from agent_based_model import Person
import numpy as np


class DepressionTreatmentHybridABSD(Model):
    def instantiate_model(self):
        super().instantiate_model()
        self.register_agent_factory("person", lambda agent_id, model, properties: Person(agent_id, model, properties))

        self.sd_model = None
        self.exchange = {}
        self.exchange["depression_treatment_demand"] = 0
        self.exchange["out_anti_depressant"] = 0


    def configure(self, config):
        super().configure(config)
        self.sd_model = DepressionTreatmentSystemDynamics(self)

        # self.sd_model.treatment_success_rate.equation = self.treatment_success_rate

    def end_round(self, time, sim_round, step):

        depression_treatment_demand = 0
        update_anti_depressant_waiting_list = int(self.evaluate_equation("anti_depressant_waiting_list", time))
        update_anti_depressant_anti_psychotic_waiting_list = \
            int(self.evaluate_equation("anti_depressant_anti_psychotic_waiting_list", time))
        update_anti_anti_psychotic_waiting_list = int(self.evaluate_equation("anti_psychotic_waiting_list", time))

        shuffled_agents = np.random.permutation(self.agents)

        for agent in shuffled_agents:
            if agent.state == "untreated":
                depression_treatment_demand += 1

                if update_anti_depressant_waiting_list > 0:
                    agent.state = "anti_depressant_waiting_list"
                    agent.waiting_time = 0
                    update_anti_depressant_waiting_list -= 1
                elif update_anti_depressant_anti_psychotic_waiting_list > 0:
                    agent.state = "anti_depressant_anti_psychotic_waiting_list"
                    agent.waiting_time = 0
                    update_anti_depressant_anti_psychotic_waiting_list -= 1
                elif update_anti_anti_psychotic_waiting_list > 0:
                    agent.state = "anti_psychotic_waiting_list"
                    agent.waiting_time = 0
                    update_anti_anti_psychotic_waiting_list -= 1
            elif "waiting_list" in agent.state:
                agent.waiting_time += 1

            if agent.state == "anti_depressant_waiting_list" and agent.waiting_time == :


        self.exchange["depression_treatment_demand"] = depression_treatment_demand

    # def end_round(self, time, sim_round, step):
    #
    #     depression_demand = 0
    #     update_enter_treatment = int(self.evaluate_equation("enter_treatment", time))
    #     update_untreated = int(self.evaluate_equation("untreated", time))
    #     update_outgoing_patients = int(self.evaluate_equation("outgoing_patients", time))
    #
    #     for agent in self.agents:
    #         if agent.state == "depression":
    #             depression_demand += 1
    #             if update_enter_treatment > 0:
    #                 agent.state = "depression_treated"
    #                 update_enter_treatment -= 1
    #             elif update_untreated > 0:
    #                 agent.state = "depression_untreated"
    #                 update_untreated -= 1
    #         elif agent.state == "depression_treated":
    #             if update_outgoing_patients > 0:
    #                 agent.state = "healthy_treated"
    #                 update_outgoing_patients -= 1
    #             else:
    #                 # Adding monetary costs for as long as they are treated
    #                 treatment_cost = 1
    #                 agent.set_property_value("monetary_cost", agent.get_property_value("monetary_cost")
    #                                          + treatment_cost)
    #
    #     self.exchange["depression_demand"] = depression_demand