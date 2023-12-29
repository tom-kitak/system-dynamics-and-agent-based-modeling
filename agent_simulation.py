from agent_based_model import Person
import numpy as np


if __name__ == "__main__":
    madrs_scores = [Person.sample_MADRS_score() for _ in range(100)]
    remission_count = 0

    for ms in madrs_scores:
        remission_count += 1 if ((ms - np.random.normal(16.4, 8.76)) <= 12) else 0

    print(remission_count)

