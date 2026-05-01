import json
import subprocess
import sys
from pathlib import Path
import unittest

from src.substrate_model import simulate_single_cell


class TestSimulationModel(unittest.TestCase):
    def test_single_cell_is_deterministic_for_seed(self):
        params = {
            'rho_c': 5.0,
            'lambda_max': 1.0,
            'k': 2.0,
            'rho_eq': 4.5,
            'Gamma': 0.25,
            'R_0': 0.2,
            'C': -1.0,
        }
        first = simulate_single_cell(params, dt=0.01, T_max=2.0, initial_rho_s=4.0, seed=123)
        second = simulate_single_cell(params, dt=0.01, T_max=2.0, initial_rho_s=4.0, seed=123)

        self.assertTrue((first['rho_s'] == second['rho_s']).all())
        self.assertTrue((first['lambda'] == second['lambda']).all())
        self.assertTrue((first['events'] == second['events']).all())

    def test_main_single_cell_creates_output_file(self):
        out = Path('tmp/test_single_cell.json')
        out.parent.mkdir(parents=True, exist_ok=True)
        if out.exists():
            out.unlink()

        cmd = [sys.executable, 'main.py', '--mode', 'single-cell', '--seed', '7', '--output', str(out)]
        completed = subprocess.run(cmd, check=False, capture_output=True, text=True)

        self.assertEqual(completed.returncode, 0, msg=completed.stderr)
        self.assertTrue(out.exists(), msg=completed.stdout + completed.stderr)

        payload = json.loads(out.read_text())
        self.assertEqual(payload['seed'], 7)
        self.assertIn('rho_s_time_series', payload)
        self.assertIn('event_times', payload)


if __name__ == '__main__':
    unittest.main()
