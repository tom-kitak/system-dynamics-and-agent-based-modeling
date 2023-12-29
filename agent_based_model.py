from BPTK_Py import Agent
import numpy as np
import random


class Person(Agent):

    def initialize(self):
        self.agent_type = "person"
        # Every stock from SD is a state
        self.state = "depressed"

        self.treatment_history = []
        self.total_waiting_time = 0
        self.in_treatment_time = 0
        self.monetary_cost = 0

    def act(self, time, round_no, step_no):
        pass

    def __repr__(self):
        return f"state: {self.state}"
