import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from swarm.repl import run_demo_loop
from triage_agent.agents import triage_agent

if __name__ == "__main__":
    run_demo_loop(triage_agent)
