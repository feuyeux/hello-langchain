import json
import matplotlib.pyplot as plt
import numpy as np
import os

# Model names and corresponding file paths
models = [
    "qwen3_8b", 
    "qwen3_14b", 
    "qwen3_30b", 
    "qwen3_32b"
]
log_dir = "ollama_log"

# Initialize data dictionaries to store metrics
execution_times = {model: [] for model in models}
cpu_usages = {model: [] for model in models}
memory_usages = {model: [] for model in models}
gpu_statuses = {model: [] for model in models}  # For GPU information

# Load data from JSON files
for model in models:
    filepath = os.path.join(log_dir, f"{model}_performance.json")
    with open(filepath, 'r') as f:
        data = json.load(f)
        
    for entry in data:
        execution_times[model].append(entry["execution_time"])
        cpu_usages[model].append(entry["metrics"]["cpu_percent"])
        memory_usages[model].append(entry["metrics"]["memory_used_mb"])
        # Store GPU information (for Apple Silicon, it's integrated with CPU)
        if "gpu_info" in entry["metrics"]:
            gpu_statuses[model].append(entry["metrics"]["gpu_info"][0]["utilization"])

# Ensure ollama_log directory exists
os.makedirs(log_dir, exist_ok=True)

# Calculate max and median values for each metric
max_execution = [max(execution_times[model]) for model in models]
median_execution = [np.median(execution_times[model]) for model in models]

max_cpu = [max(cpu_usages[model]) for model in models]
median_cpu = [np.median(cpu_usages[model]) for model in models]

max_memory = [max(memory_usages[model]) for model in models]
median_memory = [np.median(memory_usages[model]) for model in models]

# Convert memory to GB for better readability
max_memory_gb = [mem/1024 for mem in max_memory]
median_memory_gb = [mem/1024 for mem in median_memory]

# Set up plot parameters
x = np.arange(len(models))
width = 0.35
model_labels = [model.replace('_', ' ').upper() for model in models]
colors = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12']  # Blue, Green, Red, Orange

# Create execution time comparison chart (max and median)
fig, ax = plt.subplots(figsize=(12, 8))
rects1 = ax.bar(x - width/2, max_execution, width, label='Maximum Time', color='#3498db')
rects2 = ax.bar(x + width/2, median_execution, width, label='Median Time', color='#2ecc71')

ax.set_ylabel('Execution Time (seconds)', fontsize=12)
ax.set_title('Execution Time Comparison Across Models', fontsize=16, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(model_labels, fontsize=10, fontweight='bold')
ax.legend(fontsize=10)
ax.grid(axis='y', linestyle='--', alpha=0.7)

# Add value labels
def autolabel(rects, fmt='{:.1f}'):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(fmt.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom',
                    fontsize=10, fontweight='bold')

autolabel(rects1)
autolabel(rects2)
fig.tight_layout()
plt.savefig(os.path.join(log_dir, 'execution_time_comparison.png'), dpi=300)
plt.close()

# Create CPU usage comparison chart
fig, ax = plt.subplots(figsize=(12, 8))
rects1 = ax.bar(x - width/2, max_cpu, width, label='Maximum CPU', color='#e74c3c')
rects2 = ax.bar(x + width/2, median_cpu, width, label='Median CPU', color='#f39c12')

ax.set_ylabel('CPU Usage (%)', fontsize=12)
ax.set_title('CPU Usage Comparison Across Models', fontsize=16, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(model_labels, fontsize=10, fontweight='bold')
ax.legend(fontsize=10)
ax.grid(axis='y', linestyle='--', alpha=0.7)

autolabel(rects1)
autolabel(rects2)
fig.tight_layout()
plt.savefig(os.path.join(log_dir, 'cpu_usage_comparison.png'), dpi=300)
plt.close()

# Create memory usage comparison chart (in GB)
fig, ax = plt.subplots(figsize=(12, 8))
rects1 = ax.bar(x - width/2, max_memory_gb, width, label='Maximum Memory', color='#9b59b6')
rects2 = ax.bar(x + width/2, median_memory_gb, width, label='Median Memory', color='#1abc9c')

ax.set_ylabel('Memory Used (GB)', fontsize=12)
ax.set_title('Memory Usage Comparison Across Models', fontsize=16, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(model_labels, fontsize=10, fontweight='bold')
ax.legend(fontsize=10)
ax.grid(axis='y', linestyle='--', alpha=0.7)

# Format in GB with 1 decimal place
def autolabel_gb(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height:.1f} GB',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom',
                    fontsize=10, fontweight='bold')

autolabel_gb(rects1)
autolabel_gb(rects2)
fig.tight_layout()
plt.savefig(os.path.join(log_dir, 'memory_usage_comparison.png'), dpi=300)
plt.close()

# Create a consolidated comparison chart for all metrics
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 18))

# Execution Time chart (top subplot)
bars1 = ax1.bar(x - width/2, max_execution, width, label='Maximum', color='#3498db')
bars2 = ax1.bar(x + width/2, median_execution, width, label='Median', color='#2ecc71')
ax1.set_ylabel('Execution Time (s)', fontsize=14)
ax1.set_title('Model Performance Comparison: Execution Time', fontsize=16, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(model_labels, fontsize=12, fontweight='bold')
ax1.legend(fontsize=12)
ax1.grid(axis='y', linestyle='--', alpha=0.7)
for i, v in enumerate(max_execution):
    ax1.text(i - width/2, v + 0.2, f'{v:.1f}s', ha='center', fontweight='bold')
for i, v in enumerate(median_execution):
    ax1.text(i + width/2, v + 0.2, f'{v:.1f}s', ha='center', fontweight='bold')

# CPU usage (middle subplot)
bars3 = ax2.bar(x - width/2, max_cpu, width, label='Maximum', color='#e74c3c')
bars4 = ax2.bar(x + width/2, median_cpu, width, label='Median', color='#f39c12')
ax2.set_ylabel('CPU Usage (%)', fontsize=14)
ax2.set_title('Model Performance Comparison: CPU Usage', fontsize=16, fontweight='bold')
ax2.set_xticks(x)
ax2.set_xticklabels(model_labels, fontsize=12, fontweight='bold')
ax2.legend(fontsize=12)
ax2.grid(axis='y', linestyle='--', alpha=0.7)
for i, v in enumerate(max_cpu):
    ax2.text(i - width/2, v + 0.2, f'{v:.1f}%', ha='center', fontweight='bold')
for i, v in enumerate(median_cpu):
    ax2.text(i + width/2, v + 0.2, f'{v:.1f}%', ha='center', fontweight='bold')

# Memory usage (bottom subplot)
bars5 = ax3.bar(x - width/2, max_memory_gb, width, label='Maximum', color='#9b59b6')
bars6 = ax3.bar(x + width/2, median_memory_gb, width, label='Median', color='#1abc9c')
ax3.set_ylabel('Memory Used (GB)', fontsize=14)
ax3.set_title('Model Performance Comparison: Memory Usage', fontsize=16, fontweight='bold')
ax3.set_xlabel('Models', fontsize=14)
ax3.set_xticks(x)
ax3.set_xticklabels(model_labels, fontsize=12, fontweight='bold')
ax3.legend(fontsize=12)
ax3.grid(axis='y', linestyle='--', alpha=0.7)
for i, v in enumerate(max_memory_gb):
    ax3.text(i - width/2, v + 0.2, f'{v:.1f} GB', ha='center', fontweight='bold')
for i, v in enumerate(median_memory_gb):
    ax3.text(i + width/2, v + 0.2, f'{v:.1f} GB', ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig(os.path.join(log_dir, 'model_performance_comparison.png'), dpi=300)
plt.close()

# Add a note about GPU usage
print(f"Note: For Apple Silicon GPU, the utilization is '{gpu_statuses[models[0]][0]}'")
print(f"Charts have been saved as PNG files in the {log_dir} directory.")