import re
import ast
from textwrap import dedent


class 战术编译器:
    # 转换规则配置（支持链式替换）
    语法规则 = [
        (r'战术行动\s+(\w+)\s*:', r'def \1():'),  # 移除函数定义
        (r'瓦学弟\s+"(\w+)"\s*=\s*(.+)', r'\1 = \2'),  # 变量声明
        (r'报点\s+"(.*?\{.*?\}.*?)"', r'print(f"\1")'),  # 带变量的情况
        (r'报点\s+"(.*?)"', r'print("\1")'),  # 无变量的情况
        (r'战术部署\s+(.+)\s*:', r'if \1:'),  # 条件判断
        (r'执行战术\s+(\d+)\s+次\s*:', r'for _ in range(\1):'),  # 循环结构
        (r'启动协议', r'{函数名}()')  # 入口点
    ]

    @classmethod
    def 编译(cls, 战术脚本):
        代码 = dedent(战术脚本)

        # 提取函数名
        函数名匹配 = re.search(r'战术行动\s+(\w+)\s*:', 代码)
        函数名 = 函数名匹配.group(1) if 函数名匹配 else '任务'

        # 报点优先处理
        代码 = re.sub(r'报点\s+"(.*?\{.*?\}.*?)"', r'print(f"\1")', 代码, flags=re.MULTILINE)

        # 替换规则
        for 模式, 替换 in cls.语法规则[1:]:
            替换 = 替换.replace('{函数名}', 函数名)
            代码 = re.sub(模式, 替换, 代码, flags=re.MULTILINE)

        # 最后替换战术行动行为
        代码 = re.sub(r'战术行动\s+(\w+)\s*:', r'def \1():', 代码)

        # 修复缩进与校验
        代码 = cls._修复缩进(代码)
        cls._语法检查(代码)
        return 代码.strip()

    @classmethod
    def _修复缩进(cls, 代码):
        lines = 代码.split('\n')
        new_lines = []
        indent_stack = [0]

        for i, line in enumerate(lines):
            stripped = line.strip()
            if not stripped:
                new_lines.append('')
                continue

            # 如果上一行是以 ':' 结尾，我们要加一层缩进
            if i > 0 and lines[i - 1].strip().endswith(':'):
                indent_stack.append(indent_stack[-1] + 4)
            elif not line.startswith(' '):
                # 如果本行是顶级（没有缩进），我们回到最外层
                while len(indent_stack) > 1:
                    indent_stack.pop()

            new_lines.append(' ' * indent_stack[-1] + stripped)

        return '\n'.join(new_lines)

    @classmethod
    def _语法检查(cls, 代码):
        """使用AST进行语法验证"""
        try:
            ast.parse(代码)
        except SyntaxError as e:
            raise ValueError(f"战术脚本语法错误: 第{e.lineno}行 - {e.msg}") from None


class 战术执行器:
    @staticmethod
    def 安全执行(编译代码):
        """在隔离环境中执行代码"""
        沙箱 = {
            '__builtins__': {
                'print': print,
                'range': range
            },
            'math': None  # 禁止数学模块
        }

        try:
           # print('开始执行------------')
            exec(编译代码, 沙箱)
            return 沙箱  # 返回执行后的变量状态
        except Exception as e:
            print(f"战术执行失败: {type(e).__name__} - {str(e)}")
            return None


# 测试用例
if __name__ == "__main__":
    测试脚本 = """
战术行动 突袭A点:
    瓦学弟 "主武器" = "暴徒"
    瓦学弟 "弹药" = 25

    战术部署 弹药 > 0:
        报点 "使用【{主武器}】开火！剩余弹药：{弹药}"
        瓦学弟 "弹药" = 弹药 - 10

    执行战术 2 次:
        报点 "战术换弹..."
启动协议
    """


    try:
        # 编译阶段
        编译结果 = 战术编译器.编译(测试脚本)
        #print("✅ 编译成功:\n" + 编译结果)

        # 执行阶段
        战场状态 = 战术执行器.安全执行(编译结果)
        #if 战场状态:
            # print("\n战场最终状态:")
            # print(f"主武器: {战场状态.get('主武器', '未知')}")
            # print(f"剩余弹药: {战场状态.get('弹药', 0)}")

    except ValueError as e:
        print(f"❌ 编译错误: {str(e)}")
