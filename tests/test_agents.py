import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

import agents.arbiter_phase as arbiter
import agents.father_phase as father
import agents.soap_phase as soap
import agents.watson_phase as watson


def test_run_arbiter():
    assert arbiter.run_arbiter('issue') == '[Arbiter resolves] issue'


def test_run_father():
    assert father.run_father('data') == '[Father logic for] data'


def test_run_soap():
    assert soap.run_soap('plan') == '[Soap builds SOP] plan'


def test_run_watson():
    assert watson.run_watson() == '[Watson ready]'
