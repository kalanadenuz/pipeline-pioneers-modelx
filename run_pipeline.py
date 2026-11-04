#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from hydropulse.cli import run_full_pipeline_demo

if __name__ == "__main__":
    run_full_pipeline_demo()
