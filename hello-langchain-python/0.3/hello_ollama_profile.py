from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
import json
import os
from hello_utils import get_system_metrics, clean_think_sections
import platform
import sys
import time

results_dir = "ollama_log"
os.makedirs(results_dir, exist_ok=True)
print(f"系统信息: {platform.system()} {platform.node()} {platform.release()} {platform.version()} {platform.machine()} {platform.processor()} Python {sys.version}")

model_names = ["qwen3:8b", "qwen3:14b", "qwen3:30b", "qwen3:32b"]

template = """你是顶级的短片作家，
使用{lang},请根据{title}的内容，写一篇50字的精品短文"""
prompt = ChatPromptTemplate.from_template(template)
languages = ["英语", "法语", "俄语", "汉语"]

try:
    for model_name in model_names:
        print(f"\n\n=========== 测试模型: {model_name} ===========")

        llama_model = OllamaLLM(
            model=model_name,
            base_url="http://localhost:11434",
            temperature=0,
            num_gpu=1,
            num_thread=8,
        )

        chain = prompt | llama_model
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
                result = clean_think_sections(result)
                success = True
            except Exception as e:
                result = f"错误: {str(e)}"
                success = False

            print(
                f"执行时间: {execution_time:.2f}s, 系统指标: {metrics}, 执行结果: {result}")

            model_results.append({
                'language': lang,
                'output': result,
                'success': success,
                'metrics': metrics,
                'execution_time': execution_time
            })

        model_filename = model_name.replace(':', '_')
        with open(f"{results_dir}/{model_filename}_performance.json", 'w', encoding='utf-8') as f:
            json.dump(model_results, f, ensure_ascii=False, indent=2)
except KeyboardInterrupt:
    print("\n测试被用户中断")
except Exception as e:
    print(f"\n发生错误: {str(e)}")
