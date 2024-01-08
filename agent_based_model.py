from BPTK_Py import Agent
import numpy as np
import random


class Person(Agent):

    def initialize(self):
        self.agent_type = "person"
        # Every stock from SD is a state
        self.state = "untreated"

        self.current_waiting_time = 0
        self.total_waiting_time = 0

        self.treatment_history = []  # Includes past treatments, response, remission, relapse

        self.current_in_treatment_time = 0
        self.current_in_remission_time = 0

        self.total_remission_time = 0
        self.total_response_time = 0

    def act(self, time, round_no, step_no):
        pass

    def __repr__(self):
        return f"state: {self.state}"
