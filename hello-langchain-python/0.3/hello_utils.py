import platform

import subprocess
import psutil

import os
import json
import re


def clean_think_sections(text):
    """Remove <think> sections from model responses"""
    pattern = r'<think>.*?</think>\s*'
    return re.sub(pattern, '', text, flags=re.DOTALL)
