import sys
import subprocess

Required = []


def configure(ls):
    global Required
    Required = ls


def install():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])

        for module in Required:
            try:
                __import__(module)
            except ImportError:
                print(f"{module} not found. Installing...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", module])

    except subprocess.CalledProcessError as e:
        print(f"Error installing package(s): {e}")
