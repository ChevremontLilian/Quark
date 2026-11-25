import unittest

import torch

from Scripts.pyAI import _build_warmup_cosine_scheduler


class TrainingScheduleTests(unittest.TestCase):
    def test_warmup_ramps_up_before_cosine_decay(self):
        parameter = torch.nn.Parameter(torch.tensor(1.0))
        optimizer = torch.optim.SGD([parameter], lr=1.0)

        scheduler, warmup_steps = _build_warmup_cosine_scheduler(optimizer, 100)

        self.assertEqual(warmup_steps, 5)
        self.assertAlmostEqual(optimizer.param_groups[0]["lr"], 0.1)

        for step in range(100):
            optimizer.step()
            scheduler.step()
            if step + 1 == warmup_steps:
                self.assertAlmostEqual(optimizer.param_groups[0]["lr"], 1.0)

        self.assertAlmostEqual(optimizer.param_groups[0]["lr"], 0.1)

    def test_single_step_training_skips_warmup(self):
        parameter = torch.nn.Parameter(torch.tensor(1.0))
        optimizer = torch.optim.SGD([parameter], lr=1.0)

        scheduler, warmup_steps = _build_warmup_cosine_scheduler(optimizer, 1)

        self.assertEqual(warmup_steps, 0)
        optimizer.step()
        scheduler.step()
        self.assertAlmostEqual(optimizer.param_groups[0]["lr"], 0.1)


if __name__ == "__main__":
    unittest.main()
