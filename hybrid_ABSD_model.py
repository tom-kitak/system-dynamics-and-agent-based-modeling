from BPTK_Py import Model
from system_dynamics_model import DepressionTreatmentSystemDynamics
from agent_based_model import Person
import numpy as np
import random


class DepressionTreatmentHybridABSD(Model):
    def instantiate_model(self):
        super().instantiate_model()
        self.register_agent_factory("person", lambda agent_id, model, properties: Person(agent_id, model, properties))

        self.sd_model = None
        self.exchange = {}
        self.exchange["depression_treatment_demand"] = 0

        self.exchange["out_antidepressant"] = 0
        self.exchange["out_antidepressant_antipsychotic"] = 0
        self.exchange["out_antipsychotic"] = 0
        self.exchange["out_esketamine"] = 0
        self.exchange["out_ect"] = 0

        self.exchange["in_remission"] = 0
        self.exchange["out_remission"] = 0
        self.exchange["in_esketamine_waiting_list"] = 0
        self.exchange["in_ect_waiting_list"] = 0
        self.exchange["in_antidepressant_waiting_list"] = 0

        self.treatments = {"antidepressant", "antidepressant_antipsychotic", "antipsychotic", "esketamine", "ect"}


    def configure(self, config):
        super().configure(config)
        self.sd_model = DepressionTreatmentSystemDynamics(self)
        self.treatment_properties = config["treatment_properties"]

        # self.sd_model.treatment_success_rate.equation = self.treatment_success_rate

    def end_round(self, time, sim_round, step):

        depression_treatment_demand = 0
        out_antidepressant = 0
        out_antidepressant_antipsychotic = 0
        out_antipsychotic = 0
        out_esketamine = 0
        out_ect = 0

        in_remission = 0
        out_remission = 0
        in_esketamine_waiting_list = 0
        in_ect_waiting_list = 0
        in_antidepressant_waiting_list = 0

        # TODO: why can't I use int()
        update_antidepressant_waiting_list = self.evaluate_equation("antidepressant_waiting_list", time)
        update_antidepressant_antipsychotic_waiting_list = int(self.evaluate_equation("antidepressant_antipsychotic_waiting_list", time))
        update_anti_antipsychotic_waiting_list = int(self.evaluate_equation("antipsychotic_waiting_list", time))
        update_in_antidepressant = int(self.evaluate_equation("in_antidepressant", time))
        update_in_antidepressant_antipsychotic = int(self.evaluate_equation("in_antidepressant_antipsychotic", time))
        update_in_antipsychotic = int(self.evaluate_equation("in_antipsychotic", time))

        shuffled_agents = np.random.permutation(self.agents)

        for agent in shuffled_agents:
            if agent.state == "untreated":
                depression_treatment_demand += 1

                if update_antidepressant_waiting_list > 0:
                    agent.state = "antidepressant_waiting_list"
                    agent.waiting_time = 0
                    update_antidepressant_waiting_list -= 1
                elif update_antidepressant_antipsychotic_waiting_list > 0:
                    agent.state = "antidepressant_antipsychotic_waiting_list"
                    agent.waiting_time = 0
                    update_antidepressant_antipsychotic_waiting_list -= 1
                elif update_anti_antipsychotic_waiting_list > 0:
                    agent.state = "antipsychotic_waiting_list"
                    agent.waiting_time = 0
                    update_anti_antipsychotic_waiting_list -= 1
            elif "waiting_list" in agent.state:
                agent.waiting_time += 1
                if agent.state == "antidepressant_waiting_list" and update_in_antidepressant > 0:
                    agent.state = "antidepressant"
                    agent.total_waiting_time += agent.waiting_time
                    agent.waiting_time = 0
                    agent.in_treatment_time = 0
                elif agent.state == "antidepressant_antipsychotic_waiting_list" and update_in_antidepressant_antipsychotic > 0:
                    agent.state = "antidepressant_antipsychotic"
                    agent.total_waiting_time += agent.waiting_time
                    agent.waiting_time = 0
                    agent.in_treatment_time = 0
                elif agent.state == "antipsychotic_waiting_list" and update_in_antipsychotic > 0:
                    agent.state = "antipsychotic"
                    agent.total_waiting_time += agent.waiting_time
                    agent.waiting_time = 0
                    agent.in_treatment_time = 0
            elif agent.state in self.treatments:
                agent.in_treatment_time += 1
                if agent.in_treatment_time == self.treatment_properties[agent.state]["duration"]:
                    agent.in_treatment_time = 0
                    agent.treatment_history.append(agent.state)
                    agent.monetary_cost += self.treatment_properties[agent.state]["cost"]

                    remission_prob = self.treatment_properties[agent.state]["remission_rate"]
                    response_prob = self.treatment_properties[agent.state]["response_rate"] - \
                                    self.treatment_properties[agent.state]["remission_rate"]

                    random_number = random.random()
                    if random_number < remission_prob:
                        # Remission
                        if agent.state == "antidepressant":
                            out_antidepressant += 1
                        elif agent.state == "antidepressant_antipsychotic":
                            out_antidepressant_antipsychotic += 1
                        elif agent.state == "antipsychotic":
                            out_antipsychotic += 1
                        elif agent.state == "esketamine":
                            out_esketamine += 1
                        elif agent.state == "ect":
                            out_ect += 1
                        else:
                            raise Exception(f"{agent.state} is not first line treatment")

                        agent.state = "remission"
                        agent.in_remission_time = 0
                        in_remission += 1
                    elif random_number < remission_prob + response_prob:
                        # Response -> Start the same treatment again
                        agent.treatment_history.append("response")
                    else:
                        # Fail -> Enter next treatment waiting list
                        if agent.state == "antidepressant":
                            out_antidepressant += 1
                            agent.state = "esketamine_waiting_list"
                            in_esketamine_waiting_list += 1
                        elif agent.state == "antidepressant_antipsychotic":
                            out_antidepressant_antipsychotic += 1
                            agent.state = "esketamine_waiting_list"
                            in_esketamine_waiting_list += 1
                        elif agent.state == "antipsychotic":
                            out_antipsychotic += 1
                            agent.state = "esketamine_waiting_list"
                            in_esketamine_waiting_list += 1
                        elif agent.state == "esketamine":
                            out_esketamine += 1
                            agent.state = "ect_waiting_list"
                            in_ect_waiting_list += 1
                        elif agent.state == "ect":
                            out_ect += 1
                            agent.state = "antidepressant_waiting_list"
                            in_antidepressant_waiting_list += 1
                        else:
                            raise Exception(f"{agent.state} is not first line treatment")
            elif agent.state == "remission":
                agent.in_remission_time += 1

                # Note: relapse probability formula is obtained from https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5684279/
                relapse_probability = 1 / np.exp(7 * agent.in_remission_time)

                if random.random() < relapse_probability:
                    # Relapse occurs -> Back to the start of the pipeline
                    agent.treatment_history.append("relapse")
                    agent.state = "untreated"
                    out_remission += 1

        self.exchange["depression_treatment_demand"] = depression_treatment_demand

        self.exchange["out_antidepressant"] = out_antidepressant
        self.exchange["out_antidepressant_antipsychotic"] = out_antidepressant_antipsychotic
        self.exchange["out_antipsychotic"] = out_antipsychotic
        self.exchange["out_esketamine"] = out_esketamine
        self.exchange["out_ect"] = out_ect

        self.exchange["in_remission"] = in_remission
        self.exchange["out_remission"] = out_remission

        self.exchange["in_esketamine_waiting_list"] = in_esketamine_waiting_list
        self.exchange["in_ect_waiting_list"] = in_ect_waiting_list
        self.exchange["in_antidepressant_waiting_list"] = in_antidepressant_waiting_list
