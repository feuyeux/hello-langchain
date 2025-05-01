from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
import time
import psutil
import subprocess
import json
import os
import platform
import sys

def get_gpu_info():
    system = platform.system()
    gpu_info = []
    
    if system == "Darwin":  # macOS
        try:
            # 检查是否为M系列芯片
            is_arm = platform.processor() == 'arm'
            if is_arm:
                # 尝试获取M系列芯片上的性能计数器信息
                result = subprocess.run(['pmset', '-g', 'therm'], 
                                      capture_output=True, text=True, check=False)
                gpu_info.append({
                    'device': 'Apple Silicon GPU',
                    'utilization': 'Integrated with CPU',
                    'memory_info': 'Shared with system memory'
                })
            else:
                # Intel Mac
                result = subprocess.run(['system_profiler', 'SPDisplaysDataType', '-json'], 
                                      capture_output=True, text=True, check=False)
                if result.returncode == 0:
                    try:
                        data = json.loads(result.stdout)
                        if 'SPDisplaysDataType' in data:
                            for gpu in data['SPDisplaysDataType']:
                                if 'spdisplays_vendor' in gpu:
                                    gpu_info.append({
                                        'device': gpu.get('spdisplays_device-name', 'Unknown GPU'),
                                        'vendor': gpu.get('spdisplays_vendor', 'Unknown'),
                                        'memory_info': gpu.get('spdisplays_vram', 'Unknown')
                                    })
                    except json.JSONDecodeError:
                        pass
        except Exception as e:
            gpu_info.append({'error': f'Failed to get GPU info: {str(e)}'})
    
    elif system == "Linux" or system == "Windows":
        try:
            # 尝试使用nvidia-smi获取GPU信息
            env = os.environ.copy()
            env['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'
            result = subprocess.run(['nvidia-smi', '--query-gpu=index,name,memory.used,memory.total,utilization.gpu', 
                                   '--format=csv,noheader,nounits'], 
                                  capture_output=True, text=True, check=False, env=env)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if line.strip():
                        parts = line.split(', ')
                        if len(parts) >= 5:
                            index, name, mem_used, mem_total, util = parts[:5]
                            gpu_info.append({
                                'index': int(index),
                                'name': name,
                                'memory_used_mb': float(mem_used),
                                'memory_total_mb': float(mem_total),
                                'utilization_percent': float(util)
                            })
            else:
                # NVIDIA工具不可用，尝试其他方法
                gpu_info.append({'error': 'NVIDIA-SMI failed, GPU metrics unavailable'})
        except Exception as e:
            gpu_info.append({'error': f'Failed to get GPU info: {str(e)}'})
    
    # 如果没有获取到任何信息，返回一个默认消息
    if not gpu_info:
        gpu_info.append({'message': 'No GPU information available'})
    
    return gpu_info

def get_system_metrics():
    # 获取CPU使用率
    cpu_percent = psutil.cpu_percent(interval=0.1)
    
    # 获取内存使用情况
    memory = psutil.virtual_memory()
    memory_used_mb = memory.used / (1024 * 1024)
    memory_total_mb = memory.total / (1024 * 1024)
    
    # 获取GPU信息
    gpu_info = get_gpu_info()
    
    return {
        'timestamp': time.time(),
        'cpu_percent': cpu_percent,
        'memory_used_mb': memory_used_mb,
        'memory_total_mb': memory_total_mb,
        'gpu_info': gpu_info
    }

def format_metrics_diff(start_metrics, end_metrics):
    # 计算差异
    execution_time = end_metrics['timestamp'] - start_metrics['timestamp']
    cpu_diff = end_metrics['cpu_percent'] - start_metrics['cpu_percent']
    memory_diff_mb = end_metrics['memory_used_mb'] - start_metrics['memory_used_mb']
    
    result = {
        'execution_time_sec': execution_time,
        'cpu_percent_diff': cpu_diff,
        'cpu_percent_end': end_metrics['cpu_percent'],
        'memory_used_diff_mb': memory_diff_mb,
        'memory_used_end_mb': end_metrics['memory_used_mb'],
        'memory_total_mb': end_metrics['memory_total_mb'],
        'gpu_info': end_metrics['gpu_info']
    }
    
    return result

# 确保结果目录存在
results_dir = "model_performance_results"
os.makedirs(results_dir, exist_ok=True)

template = """你是顶级的短片作家，
使用{lang},请根据{title}的内容，写一篇50字的精品短文"""
prompt = ChatPromptTemplate.from_template(template)

# 定义要测试的所有模型
model_names = ["qwen3:8b", "qwen3:14b", "qwen3:30b", "qwen3:32b"]
languages = ["英语", "法语", "俄语", "汉语"]

all_results = {}

try:
    for model_name in model_names:
        print(f"\n\n=========== 测试模型: {model_name} ===========")
        
        model_results = []
        llama_model = OllamaLLM(
            model=model_name,
            base_url="http://localhost:11434",
            temperature=0,
        )
        chain = prompt | llama_model
        
        for lang in languages:
            print(f"\n----- {lang} -----")
            
            # 记录开始状态
            start_metrics = get_system_metrics()
            
            # 执行模型调用
            try:
                result = chain.invoke({"title": "窗外", "lang": lang})
                success = True
            except Exception as e:
                result = f"错误: {str(e)}"
                success = False
            
            # 记录结束状态
            end_metrics = get_system_metrics()
            
            # 计算性能差异
            perf_metrics = format_metrics_diff(start_metrics, end_metrics)
            
            # 打印结果
            print(result)
            print(f"执行时间: {perf_metrics['execution_time_sec']:.2f} 秒")
            print(f"CPU使用变化: {perf_metrics['cpu_percent_diff']:.2f}% (当前: {perf_metrics['cpu_percent_end']:.2f}%)")
            print(f"内存使用变化: {perf_metrics['memory_used_diff_mb']:.2f} MB")
            print(f"当前内存使用: {perf_metrics['memory_used_end_mb']:.2f}/{perf_metrics['memory_total_mb']:.2f} MB")
            
            # GPU信息
            print("GPU信息:")
            for gpu in perf_metrics['gpu_info']:
                if 'error' in gpu:
                    print(f"  错误: {gpu['error']}")
                elif 'message' in gpu:
                    print(f"  {gpu['message']}")
                elif 'device' in gpu:  # Mac
                    print(f"  设备: {gpu['device']}")
                    if 'utilization' in gpu:
                        print(f"  利用率: {gpu['utilization']}")
                    if 'memory_info' in gpu:
                        print(f"  内存: {gpu['memory_info']}")
                else:  # NVIDIA
                    print(f"  GPU {gpu.get('index', 'N/A')}: {gpu.get('name', 'Unknown')}")
                    print(f"    使用率: {gpu.get('utilization_percent', 'N/A')}%")
                    print(f"    显存: {gpu.get('memory_used_mb', 'N/A')}/{gpu.get('memory_total_mb', 'N/A')} MB")
            
            # 保存结果
            model_results.append({
                'language': lang,
                'output': result,
                'success': success,
                'metrics': perf_metrics
            })
        
        # 保存此模型的所有结果
        all_results[model_name] = model_results
        
        # 将性能数据写入单独的文件
        model_filename = model_name.replace(':', '_')
        with open(f"{results_dir}/{model_filename}_performance.json", 'w', encoding='utf-8') as f:
            json.dump(model_results, f, ensure_ascii=False, indent=2)
    
    # 保存所有模型的汇总结果
    with open(f"{results_dir}/all_models_performance.json", 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    
    print(f"\n性能数据已保存到 {os.path.abspath(results_dir)} 目录")

except KeyboardInterrupt:
    print("\n测试被用户中断")
except Exception as e:
    print(f"\n发生错误: {str(e)}")
    # 尝试保存已有的结果
    if all_results:
        with open(f"{results_dir}/partial_results.json", 'w', encoding='utf-8') as f:
            json.dump(all_results, f, ensure_ascii=False, indent=2)
        print(f"部分结果已保存到 {os.path.abspath(results_dir)}/partial_results.json")
