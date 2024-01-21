from BPTK_Py import Model
from models.system_dynamics_model_eskt import DepressionTreatmentSystemDynamics
from models.agent_based_model import Person
from utils.phq_analysis import PHQ9Analysis
import random


class DepressionTreatmentHybridABSD(Model):
    def instantiate_model(self):
        super().instantiate_model()
        self.register_agent_factory("person", lambda agent_id, model, properties: Person(agent_id, model, properties))

        self.sd_model = None
        self.exchange = {}

        self.exchange["in_antidepressant_waiting_list"] = 0
        self.exchange["in_antidepressant_antipsychotic_waiting_list"] = 0
        self.exchange["in_antipsychotic_waiting_list"] = 0
        self.exchange["in_esketamine_waiting_list"] = 0
        self.exchange["in_ect_waiting_list"] = 0

        self.exchange["out_antidepressant"] = 0
        self.exchange["out_antidepressant_antipsychotic"] = 0
        self.exchange["out_antipsychotic"] = 0
        self.exchange["out_esketamine"] = 0
        self.exchange["out_ect"] = 0

        self.exchange["in_remission"] = 0
        self.exchange["in_recovery"] = 0

        self.exchange["out_remission"] = 0
        self.exchange["out_recovery"] = 0

        self.treatments = {"antidepressant", "antidepressant_antipsychotic", "antipsychotic", "esketamine", "ect"}
        self.relapse_function = PHQ9Analysis()

        # These are based on Julia's percentages from the decision tree
        self.first_line_treatment_waiting_list = ["antidepressant_waiting_list",
                                                  "antidepressant_antipsychotic_waiting_list",
                                                  "antipsychotic_waiting_list"]
        self.first_line_treatment_allocation_percentage = [0.60, 0.35, 0.05]

    def configure(self, config):
        super().configure(config)
        self.sd_model = DepressionTreatmentSystemDynamics(self)
        self.treatment_properties = config["treatment_properties"]
        self.new_patients_per_week = config["new_patients_per_week"]

        self.sd_model.antidepressant_capacity.equation = self.treatment_properties["antidepressant"]["capacity"]
        self.sd_model.antidepressant_antipsychotic_capacity.equation = self.treatment_properties["antidepressant_antipsychotic"]["capacity"]
        self.sd_model.antipsychotic_capacity.equation = self.treatment_properties["antipsychotic"]["capacity"]
        self.sd_model.esketamine_capacity.equation = self.treatment_properties["esketamine"]["capacity"]
        self.sd_model.ect_capacity.equation = self.treatment_properties["ect"]["capacity"]

    def end_round(self, time, sim_round, step):

        in_antidepressant_waiting_list = 0
        in_antidepressant_antipsychotic_waiting_list = 0
        in_antipsychotic_waiting_list = 0
        in_esketamine_waiting_list = 0
        in_ect_waiting_list = 0

        out_antidepressant = 0
        out_antidepressant_antipsychotic = 0
        out_antipsychotic = 0
        out_esketamine = 0
        out_ect = 0

        in_remission = 0
        in_recovery = 0

        out_remission = 0
        out_recovery = 0

        update_in_antidepressant = round(self.evaluate_equation("in_antidepressant", time))
        update_in_antidepressant_antipsychotic = round(self.evaluate_equation("in_antidepressant_antipsychotic", time))
        update_in_antipsychotic = round(self.evaluate_equation("in_antipsychotic", time))

        update_in_esketamine = round(self.evaluate_equation("in_esketamine", time))
        update_in_ect = round(self.evaluate_equation("in_ect", time))

        # if time != 1.0:
        #     print(DepressionTreatmentHybridABSD.format_stats(self.statistics(), float(time) - 1.0))

        for agent in self.agents:
            agent.total_time_in_the_model += 1
            if agent.state == "untreated":

                waiting_list_allocation = random.choices(
                    population=self.first_line_treatment_waiting_list,
                    weights=self.first_line_treatment_allocation_percentage,
                    k=1
                )[0]

                agent.state = waiting_list_allocation
                agent.current_waiting_time = 0
                if waiting_list_allocation == "antidepressant_waiting_list":
                    in_antidepressant_waiting_list += 1
                elif waiting_list_allocation == "antidepressant_antipsychotic_waiting_list":
                    in_antidepressant_antipsychotic_waiting_list += 1
                else:
                    in_antipsychotic_waiting_list += 1

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
                elif agent.state == "esketamine_waiting_list" and update_in_esketamine > 0:
                    agent.state = "esketamine"
                    agent.total_waiting_time += agent.current_waiting_time
                    agent.current_waiting_time = 0
                    agent.current_in_treatment_time = 0
                    update_in_esketamine -= 1
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
                        elif agent.state == "esketamine":
                            out_esketamine += 1
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
                agent.current_in_remission_time += 1
                agent.total_remission_time += 1
                agent.treatment_history[-1][1] = agent.current_in_remission_time
                treatment_that_got_you_in_remission = agent.treatment_history[-2][0]

                relapse_probability = self.relapse_function.get_prob_at_time(t=agent.current_in_remission_time-1,
                                                                             p=self.treatment_properties[treatment_that_got_you_in_remission]["relapse_rate"],
                                                                             type="maintenance")
                if random.random() < relapse_probability:
                    # Relapse occurs -> Back to the start of the pipeline
                    agent.state = "untreated"
                    agent.current_in_remission_time = 0
                    out_remission += 1

                # Recovery after 6 months (6 * 4 = 24 weeks)
                elif agent.current_in_remission_time >= 24:
                    agent.state = "recovery"
                    agent.current_in_remission_time = 0
                    out_remission += 1
                    in_recovery += 1
                    agent.treatment_history.append(["recovery", 0])

            elif agent.state == "recovery":
                agent.current_in_recovery_time += 1
                agent.total_recovery_time += 1
                agent.treatment_history[-1][1] = agent.current_in_recovery_time
                treatment_that_got_you_in_recovery = agent.treatment_history[-3][0]

                relapse_probability = self.relapse_function.get_prob_at_time(t=agent.current_in_recovery_time - 1,
                                                                             p=self.treatment_properties[
                                                                                 treatment_that_got_you_in_recovery][
                                                                                 "relapse_rate"],
                                                                             type="discontinued")
                if random.random() < relapse_probability:
                    # Relapse occurs -> Back to the start of the pipeline
                    agent.state = "untreated"
                    agent.current_in_recovery_time = 0
                    out_recovery += 1

        self.exchange["in_antidepressant_waiting_list"] = in_antidepressant_waiting_list
        self.exchange["in_antidepressant_antipsychotic_waiting_list"] = in_antidepressant_antipsychotic_waiting_list
        self.exchange["in_antipsychotic_waiting_list"] = in_antipsychotic_waiting_list
        self.exchange["in_esketamine_waiting_list"] = in_esketamine_waiting_list
        self.exchange["in_ect_waiting_list"] = in_ect_waiting_list

        self.exchange["out_antidepressant"] = out_antidepressant
        self.exchange["out_antidepressant_antipsychotic"] = out_antidepressant_antipsychotic
        self.exchange["out_antipsychotic"] = out_antipsychotic
        self.exchange["out_esketamine"] = out_esketamine
        self.exchange["out_ect"] = out_ect

        self.exchange["in_remission"] = in_remission
        self.exchange["in_recovery"] = in_recovery

        self.exchange["out_remission"] = out_remission
        self.exchange["out_recovery"] = out_recovery

        self.create_agents({"name": "person", "count": self.new_patients_per_week})

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
            "esketamine_waiting_list",
            "esketamine",
            "ect_waiting_list",
            "ect",
            "remission",
            "recovery"
        ]

        for state in list_of_states:
            padding = longest_key_length - len(state)
            if state in input_dict:
                count = input_dict[state]['count']
            else:
                count = "0"
            formatted_string += f"'{state}': {'_' * padding}{count}\n"
        return formatted_string
