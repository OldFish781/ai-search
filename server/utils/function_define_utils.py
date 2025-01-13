from .functions_utils import *  # 延迟导入以避免循环依赖

import inspect

functions = ['perform_search', 'get_current_time']

def get_function_defines():
    """
    动态解析函数的参数名、类型、描述，并生成结构化的定义信息。
    """
    function_definitions = []
    for function_name in functions:
        func = globals().get(function_name)
        if func:
            # 获取函数的签名
            signature = inspect.signature(func)
            # 从函数的文档字符串中提取描述
            doc_lines = func.__doc__.strip().split('\n') if func.__doc__ else []
            description = doc_lines[0] if doc_lines else ""
            parameters = {}
            required = []
            param_section = False
            doc_param_map = {}
            
            # 提取参数描述
            for line in doc_lines:
                if "参数:" in line:
                    param_section = True
                    continue
                if param_section:
                    if line.strip() == "返回:" or line.strip() == "":
                        break  # 停止解析参数部分
                    param_line = line.strip().split(":")
                    if len(param_line) == 2:
                        param_name_type = param_line[0].strip()
                        param_description = param_line[1].strip()
                        param_name, param_type = param_name_type.split(" (")
                        param_type = param_type.rstrip(")")
                        doc_param_map[param_name] = (param_type, param_description)
            
            # 解析参数类型和是否必需
            for param_name, param in signature.parameters.items():
                param_type, param_description = doc_param_map.get(param_name, ("unknown", "No description provided"))
                param_default = param.default != inspect._empty
                parameters[param_name] = {
                    "type": param_type,
                    "description": param_description,
                }
                if not param_default:
                    required.append(param_name)
            
        function_definitions.append({
            "type": "function",
            "function": {
                "name": function_name,
                "description": description,
                "parameters": {
                    "type": "object",
                    "properties": parameters,
                    "required": required
                }
            }
        })
    return function_definitions

if __name__ == "__main__":
    function_defines = get_function_defines()
    print(function_defines)