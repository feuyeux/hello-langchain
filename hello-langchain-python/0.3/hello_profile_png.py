import json
import matplotlib.pyplot as plt
import numpy as np
import os

# Model names and corresponding file paths
models = [
    "qwen3_0.6b",
    "qwen3_1.7b",
    "qwen3_8b",
    "qwen3_14b",
    "qwen3_30b_a3b",
    "qwen3_30b"
]
log_dir = "profile_log"

# Initialize data dictionaries to store metrics
execution_times = {model: [] for model in models}
cpu_usages = {model: [] for model in models}
memory_usages = {model: [] for model in models}
gpu_statuses = {model: [] for model in models}  # For GPU information

# Load data from JSON files
for model in models:
    filepath = os.path.join(log_dir, f"{model}_performance.json")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for entry in data:
            execution_times[model].append(entry["execution_time"])
            metrics = entry.get("metrics", {})
            cpu_usages[model].append(metrics.get("cpu_percent", 0))
            memory_usages[model].append(metrics.get("memory_used_mb", 0))
            # Store GPU information (for Apple Silicon, it's integrated with CPU)
            if "gpu_info" in metrics and metrics["gpu_info"]:
                gpu_info = metrics["gpu_info"][0]
                # For Apple Silicon, set a conventional value since utilization isn't directly measurable
                if gpu_info.get("apple_silicon", False):
                    # Using CPU usage as a proxy for integrated GPU on Apple Silicon
                    gpu_statuses[model].append(metrics.get(
                        "cpu_percent", 0) * 0.8)  # Estimated GPU usage
                else:
                    utilization = gpu_info.get("utilization_percent", None)
                    gpu_statuses[model].append(utilization)
            else:
                gpu_statuses[model].append(None)
    except FileNotFoundError:
        print(f"Warning: File not found: {filepath} - Skipping this model")
        # Remove the model from our lists since it has no data
        models.remove(model)
        del execution_times[model]
        del cpu_usages[model]
        del memory_usages[model]
        del gpu_statuses[model]

# Ensure ollama_log directory exists
os.makedirs(log_dir, exist_ok=True)

# Skip processing if there are no valid models with data
if not models:
    print("No valid model data found in the specified directory. Exiting.")
    exit()

# Calculate max and median values for each metric
max_execution = np.array([max(execution_times[model])
                         if execution_times[model] else 0 for model in models])
median_execution = np.array([np.median(
    execution_times[model]) if execution_times[model] else 0 for model in models])

max_cpu = np.array(
    [max(cpu_usages[model]) if cpu_usages[model] else 0 for model in models])
median_cpu = np.array([np.median(cpu_usages[model])
                      if cpu_usages[model] else 0 for model in models])

max_memory = np.array(
    [max(memory_usages[model]) if memory_usages[model] else 0 for model in models])
median_memory = np.array([np.median(memory_usages[model])
                         if memory_usages[model] else 0 for model in models])

# Convert memory to GB for better readability
max_memory_gb = max_memory/1024
median_memory_gb = median_memory/1024

# Set up plot parameters
x = np.arange(len(models))
width = 0.35
model_labels = [model.replace('_', ' ').upper() for model in models]
colors = ['#3498db', '#2ecc71', '#e74c3c',
          '#f39c12']  # Blue, Green, Red, Orange

# Create execution time comparison chart (max and median)
fig, ax = plt.subplots(figsize=(12, 8))
rects1 = ax.bar(x - width/2, max_execution, width,
                label='Maximum Time', color='#3498db')
rects2 = ax.bar(x + width/2, median_execution, width,
                label='Median Time', color='#2ecc71')

ax.set_ylabel('Execution Time (seconds)', fontsize=12)
ax.set_title('Execution Time Comparison Across Models',
             fontsize=16, fontweight='bold')
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
rects1 = ax.bar(x - width/2, max_cpu, width,
                label='Maximum CPU', color='#e74c3c')
rects2 = ax.bar(x + width/2, median_cpu, width,
                label='Median CPU', color='#f39c12')

ax.set_ylabel('CPU Usage (%)', fontsize=12)
ax.set_title('CPU Usage Comparison Across Models',
             fontsize=16, fontweight='bold')
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
rects1 = ax.bar(x - width/2, max_memory_gb, width,
                label='Maximum Memory', color='#9b59b6')
rects2 = ax.bar(x + width/2, median_memory_gb, width,
                label='Median Memory', color='#1abc9c')

ax.set_ylabel('Memory Used (GB)', fontsize=12)
ax.set_title('Memory Usage Comparison Across Models',
             fontsize=16, fontweight='bold')
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
bars1 = ax1.bar(x - width/2, max_execution, width,
                label='Maximum', color='#3498db')
bars2 = ax1.bar(x + width/2, median_execution, width,
                label='Median', color='#2ecc71')
ax1.set_ylabel('Execution Time (s)', fontsize=14)
ax1.set_title('Model Performance Comparison: Execution Time',
              fontsize=16, fontweight='bold')
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
bars4 = ax2.bar(x + width/2, median_cpu, width,
                label='Median', color='#f39c12')
ax2.set_ylabel('CPU Usage (%)', fontsize=14)
ax2.set_title('Model Performance Comparison: CPU Usage',
              fontsize=16, fontweight='bold')
ax2.set_xticks(x)
ax2.set_xticklabels(model_labels, fontsize=12, fontweight='bold')
ax2.legend(fontsize=12)
ax2.grid(axis='y', linestyle='--', alpha=0.7)
for i, v in enumerate(max_cpu):
    ax2.text(i - width/2, v + 0.2, f'{v:.1f}%', ha='center', fontweight='bold')
for i, v in enumerate(median_cpu):
    ax2.text(i + width/2, v + 0.2, f'{v:.1f}%', ha='center', fontweight='bold')

# Memory usage (bottom subplot)
bars5 = ax3.bar(x - width/2, max_memory_gb, width,
                label='Maximum', color='#9b59b6')
bars6 = ax3.bar(x + width/2, median_memory_gb, width,
                label='Median', color='#1abc9c')
ax3.set_ylabel('Memory Used (GB)', fontsize=14)
ax3.set_title('Model Performance Comparison: Memory Usage',
              fontsize=16, fontweight='bold')
ax3.set_xlabel('Models', fontsize=14)
ax3.set_xticks(x)
ax3.set_xticklabels(model_labels, fontsize=12, fontweight='bold')
ax3.legend(fontsize=12)
ax3.grid(axis='y', linestyle='--', alpha=0.7)
for i, v in enumerate(max_memory_gb):
    ax3.text(i - width/2, v + 0.2, f'{v:.1f} GB',
             ha='center', fontweight='bold')
for i, v in enumerate(median_memory_gb):
    ax3.text(i + width/2, v + 0.2, f'{v:.1f} GB',
             ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig(os.path.join(log_dir, 'model_performance_comparison.png'), dpi=300)
plt.close()

# Add a note about GPU usage
print(
    f"Note: For Apple Silicon GPU, the utilization is approximated using CPU usage as a proxy")
print(f"Charts have been saved as PNG files in the {log_dir} directory.")
