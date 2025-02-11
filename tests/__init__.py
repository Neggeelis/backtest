import os
import sys

# Nodrošina, ka projekta saknes mape tiek pievienota sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
