"""
Central configuration for data paths.

The MIMIC-III derived files are NOT included in this repository (they are
governed by the PhysioNet Credentialed Health Data Use Agreement). Point
DATA_DIR at the local folder where you have placed them, either by editing
the line below or by setting the ERP_DATA_DIR environment variable.
"""
import os

DATA_DIR = os.environ.get("ERP_DATA_DIR", "./data")
