from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import json
import os
from hello_utils import get_system_metrics, clean_think_sections
import platform
import sys
import time
import io

os.environ["OPENAI_API_BASE"] = "http://localhost:1234/v1"
os.environ["OPENAI_API_KEY"] = "sk-hellolmstudio"

results_dir = "profile_log"
os.makedirs(results_dir, exist_ok=True)
print(f"系统信息: {platform.system()} {platform.node()} {platform.release()} {platform.version()} {platform.machine()} {platform.processor()} Python {sys.version}")

# model_names = ["qwen3:8b", "qwen3:14b", "qwen3:30b", "qwen3:32b"]
model_names = ["qwen3-32b", "qwen3-30b-a3b", "qwen3-14b", "qwen3-8b"]

template = """你是顶级的短片作家，
使用{lang},请根据{title}的内容，写一篇50字的精品短文"""
prompt = ChatPromptTemplate.from_template(template)
languages = ["英语", "法语", "俄语", "汉语"]

try:
    for model_name in model_names:
        print(f"\n\n=========== 测试模型: {model_name} ===========")

        lm_studio_model = ChatOpenAI(
            model=model_name,
            timeout=180  # 增加超时等待时间为180秒
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
                print(f"正在调用 {model_name} 使用语言: {lang}...")
                result = chain.invoke({"title": "窗外", "lang": lang})
                endTime = time.time()
                execution_time = endTime - startTime
                metrics = get_system_metrics(execution_time)
                print(f"结果类型: {type(result)}")
                if hasattr(result, 'content'):
                    print(f"结果内容: {result.content}")
                result = clean_think_sections(result)
                success = True
            except Exception as e:
                import traceback
                print(f"详细错误: {traceback.format_exc()}")
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
