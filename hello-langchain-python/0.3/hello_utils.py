import platform

import subprocess
import psutil

import os
import json
import re

def get_gpu_info():
    """Get GPU information based on the current platform with improved error handling"""
    system = platform.system()
    gpu_info = []
    
    if system == "Darwin":  # macOS
        try:
            # Check if Apple Silicon
            is_arm = platform.processor() == 'arm' or 'arm64' in platform.machine().lower()
            
            if is_arm:
                # For Apple Silicon, we don't need to run pmset everytime as it's less informative
                # and more resource-intensive
                gpu_info.append({
                    'device': 'Apple Silicon GPU',
                    'utilization': 'Integrated with CPU',
                    'memory_info': 'Shared with system memory'
                })
            else:
                # For Intel Mac, use a more direct command with timeout
                try:
                    # Use timeout to avoid hanging
                    result = subprocess.run(
                        ['system_profiler', 'SPDisplaysDataType', '-json'],
                        capture_output=True, text=True, check=False, timeout=2.0
                    )
                    
                    if result.returncode == 0:
                        data = json.loads(result.stdout)
                        for gpu in data.get('SPDisplaysDataType', []):
                            gpu_info.append({
                                'device': gpu.get('spdisplays_device-name', 'Unknown GPU'),
                                'vendor': gpu.get('spdisplays_vendor', 'Unknown'),
                                'memory_info': gpu.get('spdisplays_vram', 'Unknown')
                            })
                except (subprocess.TimeoutExpired, json.JSONDecodeError) as e:
                    gpu_info.append({'error': f'GPU info retrieval error: {str(e)}'})
        except Exception as e:
            gpu_info.append({'error': f'Failed to get GPU info: {str(e)}'})
    
    elif system == "Linux" or system == "Windows":
        try:
            # Set environment and use a timeout for nvidia-smi
            env = os.environ.copy()
            env['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'
            
            result = subprocess.run(
                ['nvidia-smi', '--query-gpu=index,name,memory.used,memory.total,utilization.gpu', 
                 '--format=csv,noheader,nounits'],
                capture_output=True, text=True, check=False, env=env, timeout=3.0
            )
            
            if result.returncode == 0 and result.stdout.strip():
                for line in result.stdout.strip().split('\n'):
                    if not line.strip():
                        continue
                    parts = [p.strip() for p in line.split(',')]
                    if len(parts) >= 5:
                        gpu_info.append({
                            'index': int(parts[0]),
                            'name': parts[1],
                            'memory_used_mb': float(parts[2]),
                            'memory_total_mb': float(parts[3]),
                            'utilization_percent': float(parts[4])
                        })
            else:
                gpu_info.append({'message': 'No NVIDIA GPU detected or NVIDIA-SMI unavailable'})
        except (subprocess.TimeoutExpired, ValueError, IndexError) as e:
            gpu_info.append({'error': f'GPU info retrieval error: {str(e)}'})
        except Exception as e:
            gpu_info.append({'error': f'Failed to get GPU info: {str(e)}'})
    
    # If no information was collected, return a default message
    if not gpu_info:
        gpu_info.append({'message': 'No GPU information available'})
    
    return gpu_info

def get_system_metrics(timestamp):
    """Get system metrics with improved efficiency"""
    # Get CPU usage (without waiting for interval)
    cpu_percent = psutil.cpu_percent(interval=None)
    
    # Get memory usage
    memory = psutil.virtual_memory()
    memory_used_mb = memory.used / (1024 * 1024)
    memory_total_mb = memory.total / (1024 * 1024)
    
    # Only fetch GPU info when we're within reasonable CPU usage
    # to avoid overloading the system during high usage periods
    gpu_info = get_gpu_info() if cpu_percent < 90 else [{'message': 'GPU check skipped due to high CPU usage'}]
    
    return {
        'timestamp': timestamp,
        'cpu_percent': cpu_percent,
        'memory_used_mb': round(memory_used_mb, 2),  # Round to 2 decimal places for readability
        'memory_total_mb': round(memory_total_mb, 2),
        'gpu_info': gpu_info
    }

def clean_think_sections(text):
    """Remove <think> sections from model responses"""
    pattern = r'<think>.*?</think>\s*'
    return re.sub(pattern, '', text, flags=re.DOTALL)