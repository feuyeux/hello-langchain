import json
import os
import platform
import sys
import time

import psutil
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from hello_utils import clean_think_sections

os.environ["OPENAI_API_BASE"] = "http://localhost:1234/v1"
os.environ["OPENAI_API_KEY"] = "sk-hellolmstudio"

results_dir = "profile_log"
os.makedirs(results_dir, exist_ok=True)
print(f"os version: {platform.version()}")
print(f"os name: {platform.system()}")
print(f"os release: {platform.release()}")
print(f"machine: {platform.machine()}")
print(f"processor: {platform.processor()}")
print(f"node: {platform.node()}")
print(f"python version:  {sys.version}")

# model_names = ["qwen3:8b", "qwen3:14b", "qwen3:30b", "qwen3:32b"]
model_names = ["qwen3-0.6b", "qwen3-1.7b", "qwen3-4b",
               "qwen3-8b", "qwen3-8b-mlx", "qwen3-14b", "qwen3-30b"]
# model_names = ["qwen3-0.6b", "qwen3-1.7b"]

template = """你是顶级的短片作家，
使用{lang},请根据{title}的内容，写一篇50字的精品短文"""
prompt = ChatPromptTemplate.from_template(template)
languages = ["英语", "法语", "俄语", "汉语"]


def get_system_metrics(timestamp):
    """Get system metrics with improved efficiency"""
    # Get CPU usage (without waiting for interval)
    cpu_percent = psutil.cpu_percent(interval=None)

    # Get memory usage
    memory = psutil.virtual_memory()
    memory_used_mb = memory.used / (1024 * 1024)
    memory_total_mb = memory.total / (1024 * 1024)

    # Add GPU info for Apple Silicon
    gpu_info = None
    if platform.system() == "Darwin" and platform.processor() == "arm":
        try:
            import subprocess
            # For Apple Silicon, use system profiler to get GPU info
            result = subprocess.run(["system_profiler", "SPDisplaysDataType", "-json"],
                                    capture_output=True, text=True)
            if result.returncode == 0:
                import json
                data = json.loads(result.stdout)
                gpu_data = {
                    "gpu_type": "Apple Silicon (Integrated)",
                    "apple_silicon": True,
                }
                gpu_info = [gpu_data]
        except Exception as e:
            print(f"Warning: Could not get Apple Silicon GPU info: {e}")

    return {
        'timestamp': timestamp,
        'cpu_percent': cpu_percent,
        # Round to 2 decimal places for readability
        'memory_used_mb': round(memory_used_mb, 2),
        'memory_total_mb': round(memory_total_mb, 2),
        'gpu_info': gpu_info
    }


try:
    for model_name in model_names:
        print(f"\n\n==== {model_name} ====")

        lm_studio_model = ChatOpenAI(
            model=model_name,
            timeout=180
        )
        chain = prompt | lm_studio_model
        model_results = []
        for lang in languages:
            print(f"\n----- {lang} -----")
            result = {}
            metrics = {}
            execution_time = 0
            try:
                startTime = time.time()
                result = chain.invoke({"title": "窗外", "lang": lang})
                endTime = time.time()
                execution_time = endTime - startTime
                metrics = get_system_metrics(execution_time)
                # print(f"结果类型: {type(result)}")
                # if hasattr(result, 'content'):
                #     print(f"结果内容: {result.content}")
                # Extract content from AIMessage before cleaning
                result_text = result.content
                result = clean_think_sections(result_text)
                success = True
            except Exception as e:
                import traceback
                print(f"详细错误: {traceback.format_exc()}")
                result = f"错误: {str(e)}"
                success = False

            print(
                f"执行时间: {execution_time:.2f}s\n执行结果: {result}")

            model_results.append({
                'language': lang,
                'output': result,
                'success': success,
                'metrics': metrics,
                'execution_time': execution_time
            })

        model_filename = model_name.replace(':', '_')
        model_filename = model_filename.replace('-', '_')
        with open(f"{results_dir}/{model_filename}_performance.json", 'w', encoding='utf-8') as f:
            json.dump(model_results, f, ensure_ascii=False, indent=2)
except KeyboardInterrupt:
    print("\n测试被用户中断")
except Exception as e:
    print(f"\n发生错误: {str(e)}")
