from BPTK_Py import Agent
import numpy as np
import random


class Person(Agent):

    def initialize(self):
        self.agent_type = "person"
        # Every stock from SD is a state (you can look in diagram to see which stocks/states are there
        self.state = "untreated"

        self.current_waiting_time = 0 # If they are in waiting list this tracks how long they have been in this waiting list
        self.total_waiting_time = 0

        # This is a list where elements are lists of two items, the first element in this pair can be a one of the
        # treatment states (not waiting lists), response and remission. The second item in the pair is the
        # duration patient spent in the treatment in weeks
        self.treatment_history = []  # Includes past treatments, response, remission + duration in a list of 2 elements

        # If they are in treatment this tracks how long they have been in this treatment
        self.current_in_treatment_time = 0
        self.current_in_remission_time = 0

        self.total_remission_time = 0
        self.total_response_time = 0
        self.total_time_in_the_model = 0

    def act(self, time, round_no, step_no):
        pass

    def __repr__(self):
        return f"state: {self.state}"
