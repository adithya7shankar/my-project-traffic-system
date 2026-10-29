import random
from contextlib import ExitStack
from unittest.mock import patch

import utils


def sampled_pairs(rows):
    return [(row['speed'], row['size']) for row in rows]


def test_seeded_sampling_is_repeatable_and_advances_between_batches():
    rng = random.Random(7)
    first = utils.generate_vehicle_data(6, rng=rng)
    second = utils.generate_vehicle_data(6, rng=rng)
    whole = utils.generate_vehicle_data(12, rng=random.Random(7))
    # Device numbering restarts per batch; compare the sampled attributes.
    assert sampled_pairs(first + second) == sampled_pairs(whole)
    assert first == utils.generate_vehicle_data(6, rng=random.Random(7))


def test_seeded_simulation_is_repeatable_without_mutating_global_random():
    state = random.getstate()
    with ExitStack() as stack:
        for name in ['visualize_speed_distribution', 'visualize_vehicle_sizes', 'time.sleep']:
            stack.enter_context(patch('utils.' + name))
        first = utils.run_simulation(2, 3, seed=7)
        second = utils.run_simulation(2, 3, seed=7)
    assert len(first) == 6
    assert sampled_pairs(first) == sampled_pairs(second)
    assert sampled_pairs(first) == sampled_pairs(utils.generate_vehicle_data(6, rng=random.Random(7)))
    assert random.getstate() == state


def test_default_sampling_keeps_using_global_random():
    with patch('utils.random.randint', return_value=45) as speed, patch('utils.random.choice', return_value='SUV') as size:
        rows = utils.generate_vehicle_data(2)
    assert [row['speed'] for row in rows] == [45, 45]
    assert [row['size'] for row in rows] == ['SUV', 'SUV']
    assert speed.call_count == size.call_count == 2
