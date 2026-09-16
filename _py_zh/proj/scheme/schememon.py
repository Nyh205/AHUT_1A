"""schememon GUI 的 Web 服务器。"""
import os

from gui_files.common_server import route, start

# 直接从学生的项目导入 scheme 模块
from scheme import create_global_frame
from scheme_eval_apply import scheme_eval
from scheme_reader import scheme_read, buffer_lines
from scheme_utils import repl_str
from scheme_classes import SchemeError

PORT = 31416
DEFAULT_SERVER = "https://schememon.cs61a.org/"
GUI_FOLDER = "gui_files/"


class SchemeEvaluator:
    """
    一个 python 类，它使用 scheme
    解释器项目中构建的解释器来求值 scheme 表达式

    - __init__() 创建一个新的 SchemeEvaluator
    实例 - evaluate() 求值一些 scheme
    代码以及一个包含 scheme 代码的文件列表
    """

    def __init__(self):
        """
        实例化一个新的 Scheme
        求值器 初始化一个 Scheme
        环境 创建一个全局框架
        """
        self.env = create_global_frame()

    def evaluate(self, filenames, code):
        """
        使用从 scheme 项目构建的 python
        解释器求值 scheme 代码。返回
        scheme 代码最后一行的求值结果。

        - filename：包含所有基础代码的文件
        - code：用于在基础代码之上扩展的代码

        示例文件 (example.scm)
        ：==============
        =============
        (define (square
        n) (* n n) )

        (define
        (sum x y)
        (+ x y) )

        那么，SchemeEvaluator().evaluate("./example.scm", "(square 7)") 将返回 49。
        """
        try:
            all_code = ""

            for filename in filenames:
                with open(filename, 'r') as f:
                    file_content = f.read()
                    all_code += file_content + "\n"
            all_code += code
            lines = all_code.split('\n')
            src = buffer_lines(lines)
            results = []

            try:
                while True:
                    expression = scheme_read(src)
                    result = scheme_eval(expression, self.env)
                    results.append(result)
            except EOFError:
                pass
            return results
        except Exception as e:
            raise SchemeError(f"Error evaluating multiple expressions: {e}")


@route
def verify_scheme_question(scheme_problem, scheme_solution, test_cases, expected_results):
    """
    验证你为 scheme 语句题给出的解答代码是否正确。

    对每个测试用例，API 都会使用 SchemeEvaluator 求值该语句。
    如果有任何测试用例未通过，API 会将 correct 设为 False，否则设为 True。
    """
    try:
        evaluator = SchemeEvaluator()
        result = evaluator.evaluate(["questions.scm"], f"(solution-code (quote {scheme_problem}) (quote {scheme_solution}))")
        scheme_code = repl_str(result[-1])

        for i in range(0, len(test_cases)):
            test_case = test_cases[i]
            expected_result = expected_results[i]
            code = scheme_code + "\n\n" + test_case
            result = evaluator.evaluate([], code)[-1]

            # 特别说明：Python 使用 "True" 和 "False"，而
            # Scheme 使用 "#t" 和 "#f" 这处理了 "in" 过程的情况

            if str(result) == "True":
                result = "#t"
            elif str(result) == "False":
                result = "#f"

            if str(result) != expected_result:
                return {"correct": False}

        return {"correct": True}
    except Exception as e:
        print(f"ERROR in verify_scheme_question: {e}")
        import traceback
        traceback.print_exc()
        return {"correct": False}


if __name__ == "__main__" or "gunicorn" in os.environ.get("SERVER_SOFTWARE", ""):
    app = start(PORT, DEFAULT_SERVER, GUI_FOLDER)