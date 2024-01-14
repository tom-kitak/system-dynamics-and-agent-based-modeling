from BPTK_Py import Model
from system_dynamics_model_no_eskt import DepressionTreatmentSystemDynamicsWithoutEsketamine
from agent_based_model import Person
import numpy as np
import random
import sympy as sp


class DepressionTreatmentHybridABSDWithoutEsketamine(Model):
    def instantiate_model(self):
        super().instantiate_model()
        self.register_agent_factory("person", lambda agent_id, model, properties: Person(agent_id, model, properties))

        self.sd_model = None
        self.exchange = {}
        self.exchange["depression_treatment_demand"] = 0

        self.exchange["out_antidepressant"] = 0
        self.exchange["out_antidepressant_antipsychotic"] = 0
        self.exchange["out_antipsychotic"] = 0
        self.exchange["out_ect"] = 0

        self.exchange["in_remission"] = 0
        self.exchange["out_remission"] = 0
        self.exchange["in_ect_waiting_list"] = 0
        self.exchange["in_antidepressant_waiting_list"] = 0

        self.treatments = {"antidepressant", "antidepressant_antipsychotic", "antipsychotic", "ect"}

    def configure(self, config):
        super().configure(config)
        self.sd_model = DepressionTreatmentSystemDynamicsWithoutEsketamine(self)
        self.treatment_properties = config["treatment_properties"]
        self.new_patients_per_week = config["new_patients_per_week"]

        self.sd_model.antidepressant_capacity.equation = self.treatment_properties["antidepressant"]["capacity"]
        self.sd_model.antidepressant_antipsychotic_capacity.equation = self.treatment_properties["antidepressant_antipsychotic"]["capacity"]
        self.sd_model.antipsychotic_capacity.equation = self.treatment_properties["antipsychotic"]["capacity"]
        self.sd_model.ect_capacity.equation = self.treatment_properties["ect"]["capacity"]

    def end_round(self, time, sim_round, step):

        depression_treatment_demand = 0
        out_antidepressant = 0
        out_antidepressant_antipsychotic = 0
        out_antipsychotic = 0
        out_ect = 0

        in_remission = 0
        out_remission = 0
        in_ect_waiting_list = 0
        in_antidepressant_waiting_list = 0

        update_in_antidepressant = round(self.evaluate_equation("in_antidepressant", time))
        update_in_antidepressant_antipsychotic = round(self.evaluate_equation("in_antidepressant_antipsychotic", time))
        update_in_antipsychotic = round(self.evaluate_equation("in_antipsychotic", time))
        update_in_ect = round(self.evaluate_equation("in_ect", time))

        update_values = {
            'in_antidepressant_waiting_list': round(self.evaluate_equation("in_antidepressant_waiting_list", time)),
            'in_antidepressant_antipsychotic_waiting_list': round(self.evaluate_equation("in_antidepressant_antipsychotic_waiting_list", time)),
            'in_antipsychotic_waiting_list': round(self.evaluate_equation("in_antipsychotic_waiting_list", time))
        }

        # Debugging START
        # if time != 1.0:
        #     print(DepressionTreatmentHybridABSD.format_stats(self.statistics(), float(time) - 1.0))

        print("TIME:", time)
        # print("in_antipsychotic_waiting_list", self.evaluate_equation("in_antipsychotic_waiting_list", time))
        # print("antipsychotic_waiting_list", self.evaluate_equation("antipsychotic_waiting_list", time))
        # print("in_antipsychotic", self.evaluate_equation("in_antipsychotic", time))
        # print("antipsychotic", self.evaluate_equation("antipsychotic", time))
        # print("out_antipsychotic", self.evaluate_equation("out_antipsychotic", time))

        # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        # Debugging END

        for agent in self.agents:
            agent.total_time_in_the_model += 1
            if agent.state == "untreated":

                conditions_actions = [
                    (lambda: update_values['in_antidepressant_waiting_list'] > 0,
                     lambda: self.set_agent_state(agent, "antidepressant_waiting_list", update_values)),
                    (lambda: update_values['in_antidepressant_antipsychotic_waiting_list'] > 0,
                     lambda: self.set_agent_state(agent, "antidepressant_antipsychotic_waiting_list", update_values)),
                    (lambda: update_values['in_antipsychotic_waiting_list'] > 0,
                     lambda: self.set_agent_state(agent, "antipsychotic_waiting_list", update_values))
                ]
                random.shuffle(conditions_actions)

                # Iterate and execute the first true condition
                for condition, action in conditions_actions:
                    if condition():
                        action()
                        break
                else:
                    depression_treatment_demand += 1

            if "waiting_list" in agent.state:
                if agent.state == "antidepressant_waiting_list" and update_in_antidepressant > 0:
                    agent.state = "antidepressant"
                    agent.total_waiting_time += agent.current_waiting_time
                    agent.current_waiting_time = 0
                    agent.current_in_treatment_time = 0
                    update_in_antidepressant -= 1
                elif agent.state == "antidepressant_antipsychotic_waiting_list" and update_in_antidepressant_antipsychotic > 0:
                    agent.state = "antidepressant_antipsychotic"
                    agent.total_waiting_time += agent.current_waiting_time
                    agent.current_waiting_time = 0
                    agent.current_in_treatment_time = 0
                    update_in_antidepressant_antipsychotic -= 1
                elif agent.state == "antipsychotic_waiting_list" and update_in_antipsychotic > 0:
                    agent.state = "antipsychotic"
                    agent.total_waiting_time += agent.current_waiting_time
                    agent.current_waiting_time = 0
                    agent.current_in_treatment_time = 0
                    update_in_antipsychotic -= 1
                elif agent.state == "ect_waiting_list" and update_in_ect > 0:
                    agent.state = "ect"
                    agent.total_waiting_time += agent.current_waiting_time
                    agent.current_waiting_time = 0
                    agent.current_in_treatment_time = 0
                    update_in_ect -= 1
                else:
                    agent.current_waiting_time += 1
            elif agent.state in self.treatments:
                agent.current_in_treatment_time += 1

                if agent.current_in_treatment_time >= self.treatment_properties[agent.state]["duration"]:

                    # todo: Is it correct
                    if len(agent.treatment_history) > 0 and agent.treatment_history[-1][0] == "response":
                        agent.total_response_time += agent.current_in_treatment_time

                    agent.treatment_history.append([agent.state, agent.current_in_treatment_time])
                    agent.current_in_treatment_time = 0

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
                        elif agent.state == "ect":
                            out_ect += 1
                        else:
                            raise Exception(f"{agent.state} is not first line treatment")

                        agent.state = "remission"
                        agent.current_in_remission_time = 0
                        agent.treatment_history.append(["remission", 0])
                        in_remission += 1
                    elif random_number < remission_prob + response_prob:
                        # Response -> Start the same treatment again
                        agent.treatment_history.append(["response", 0])
                    else:
                        # Fail -> Enter next treatment waiting list
                        if agent.state == "antidepressant":
                            out_antidepressant += 1
                            agent.state = "ect_waiting_list"
                            in_ect_waiting_list += 1
                        elif agent.state == "antidepressant_antipsychotic":
                            out_antidepressant_antipsychotic += 1
                            agent.state = "ect_waiting_list"
                            in_ect_waiting_list += 1
                        elif agent.state == "antipsychotic":
                            out_antipsychotic += 1
                            agent.state = "ect_waiting_list"
                            in_ect_waiting_list += 1
                        elif agent.state == "ect":
                            out_ect += 1
                            agent.state = "antidepressant_waiting_list"
                            in_antidepressant_waiting_list += 1
                        else:
                            raise Exception(f"{agent.state} is not first line treatment")
            elif agent.state == "remission":
                agent.current_in_remission_time += 1
                agent.total_remission_time += 1
                agent.treatment_history[-1][1] = agent.current_in_remission_time

                relapse_probability = DepressionTreatmentHybridABSDWithoutEsketamine.relapse_function(agent.current_in_remission_time)

                if random.random() < relapse_probability:
                    # Relapse occurs -> Back to the start of the pipeline
                    agent.state = "untreated"
                    agent.current_in_remission_time = 0
                    out_remission += 1

        self.exchange["depression_treatment_demand"] = depression_treatment_demand

        self.exchange["out_antidepressant"] = out_antidepressant
        self.exchange["out_antidepressant_antipsychotic"] = out_antidepressant_antipsychotic
        self.exchange["out_antipsychotic"] = out_antipsychotic
        self.exchange["out_ect"] = out_ect

        self.exchange["in_remission"] = in_remission
        self.exchange["out_remission"] = out_remission

        self.exchange["in_ect_waiting_list"] = in_ect_waiting_list
        self.exchange["in_antidepressant_waiting_list"] = in_antidepressant_waiting_list

        self.create_agents({"name": "person", "count": self.new_patients_per_week})

    def set_agent_state(self, agent, state, update_values):
        agent.state = state
        agent.current_waiting_time = 0
        update_values["in_" + state] -= 1

    @staticmethod
    def format_stats(input_dict, time):
        # Find the longest key to determine the padding
        print("STATS TIME:", time)
        input_dict = input_dict[time]["person"]
        longest_key_length = len("antidepressant_antipsychotic_waiting_list")

        formatted_string = ""
        list_of_states = [
            "antidepressant_waiting_list",
            "antidepressant",
            "antidepressant_antipsychotic_waiting_list",
            "antidepressant_antipsychotic",
            "antipsychotic_waiting_list",
            "antipsychotic",
            "ect_waiting_list",
            "ect",
            "remission"
        ]

        for state in list_of_states:
            padding = longest_key_length - len(state)
            if state in input_dict:
                count = input_dict[state]['count']
            else:
                count = "0"
            formatted_string += f"'{state}': {'_' * padding}{count}\n"
        return formatted_string

    @staticmethod
    def relapse_function(time):
        """returns probability of relapse at a certain time point"""
        return 0.398 * sp.exp(-1.556 * time * 0.453)
