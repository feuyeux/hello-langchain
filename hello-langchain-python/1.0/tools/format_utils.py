"""
统一的输出格式化工具
"""


def format_response(response):
    """
    统一格式化响应内容

    Args:
        response: 模型响应对象或字符串

    Returns:
        str: 格式化后的内容字符串
    """
    if hasattr(response, "content"):
        return response.content
    return str(response)


def extract_content_after_think(text):
    """
    提取<think>标签之后的内容，如果没有<think>标签则返回原文本

    Args:
        text: 原始文本或消息对象

    Returns:
        str: 处理后的内容
    """
    if isinstance(text, str):
        if "</think>" in text:
            content = text.split("</think>", 1)[1].lstrip()
            return content
        return text

    if hasattr(text, "content"):
        content = text.content
        if "</think>" in content:
            return content.split("</think>", 1)[1].lstrip()
        return content

    return str(text)


def print_section_header(title, width=60):
    """
    打印章节标题

    Args:
        title: 标题文本
        width: 总宽度
    """
    print(f"\n{'='*width}")
    print(f"  {title}")
    print(f"{'='*width}")


def print_content(content, width=60):
    """
    打印内容区域

    Args:
        content: 要打印的内容
        width: 分隔线宽度
    """
    print(f"\n{'-'*width}")
    print(content)
    print(f"{'-'*width}\n")


def print_model_result(model_name, func, width=60):
    """
    统一打印模型结果的格式

    Args:
        model_name: 模型名称
        func: 执行函数
        width: 输出宽度
    """
    import time

    print_section_header(model_name, width)
    try:
        start_time = time.time()
        response = func()
        end_time = time.time()

        content = format_response(response)
        print(f"\n响应时间: {end_time - start_time:.2f}秒")
        print_content(content, width)
    except Exception as e:
        print(f"❌ 错误: {e}\n")


def print_language_result(lang, func, title, width=60):
    """
    打印特定语言的结果

    Args:
        lang: 语言名称
        func: 执行函数
        title: 主题
        width: 输出宽度
    """
    import time

    print_section_header(f"语言: {lang}", width)
    try:
        start_time = time.time()
        result = func(title, lang)
        end_time = time.time()

        content = extract_content_after_think(result)
        print(f"\n响应时间: {end_time - start_time:.2f}秒")
        print_content(content, width)
    except Exception as e:
        print(f"❌ 错误: {str(e)}\n")
