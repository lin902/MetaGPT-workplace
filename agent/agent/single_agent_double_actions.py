# 添加以下库

import os
import re
import subprocess
import asyncio

import fire
import sys
from metagpt.llm import LLM
from metagpt.actions import Action
from metagpt.roles import Role
from metagpt.schema import Message
from metagpt.logs import logger


class SimpleWriteCode(Action):  # 继承Action类

    PROMPT_TEMPLATE: str = """
    Write a python function that can {instruction} and provide two runnnable test cases.
    Return ```python your_code_here ```with NO other texts,
    your code:
    """  # 一个类属性,存储了一个多行的字符串模板，含有一个占位符{instruction}，提供一个标准化的格式

    name: str = "SimpleWriteCode"  # 类属性

    # 定义了一个名为run的异步方法,它接受一个instruction参数,并返回一个生成的包含代码的文本
    async def run(self, instruction: str):
        prompt = self.PROMPT_TEMPLATE.format(instruction=instruction)
        # 使用format()方法将PROMPT_TEMPLATE中的{instruction}占位符替换为传入的instruction参数。
        rsp = await self._aask(prompt)  # 名为_aask的异步方法,并传入了生成的prompt。await关键字确保方法等待_aask的结果
        code_text = SimpleWriteCode.parse_code(rsp)  # 提取python代码
        return code_text

    @staticmethod
    # 这是一个静态方法，不需要用self就能访问，不需要访问类的实例属性和方法，一般用于实现辅助功能，比如这里的提取大模型返回的python代码
    # 通过正则表达式提取python部分
    def parse_code(rsp):
        pattern = r'```python(.*)```'  # 以```python开头，.*除了换行符外的任意字符，又是以```结尾
        match = re.search(pattern, rsp, re.DOTALL)  # 匹配，re.DOTALL，re.DOTALL 标志确保 . 字符可以匹配任何字符,包括换行符
        code_text = match.group(1) if match else rsp  # group(0)是整个匹配的字符 1是第一个匹配的字符组
        return code_text


class SimpleRunCode(Action):

    name: str = "SimpleRunCode"

    async def run(self, code_text: str):
        # 在Windows环境下，result可能无法正确返回生成结果，在windows中在终端中输入python3可能会导致打开微软商店
        # subprocess.run() 函数来执行外部命令和程序，"python3" 是 Python 解释器的路径，-c 选项告诉 Python 执行后面的代码
        # capture_output=True 选项用于捕获执行命令的输出,包括标准输出和标准错误，text=True 选项告诉 subprocess.run() 以字符串形式返回捕获的输出,而不是字节类型。
        result = subprocess.run(["python3", "-c", code_text], capture_output=True, text=True)
        # 采用下面的可选代码来替换上面的代码
        # result = subprocess.run(["python", "-c", code_text], capture_output=True, text=True)
        # import sys
        # result = subprocess.run([sys.executable, "-c", code_text], capture_output=True, text=True)
        code_result = result.stdout
        logger.info(f"{code_result=}")
        return code_result


class RunnableCoder(Role):

    name: str = "Alice"
    profile: str = "RunnableCoder"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([SimpleWriteCode, SimpleRunCode])
        self._set_react_mode(react_mode="by_order")

    async def _act(self) -> Message:
        logger.info(f"{self._setting}: 准备 {self.rc.todo}")
        # 通过在底层按顺序选择动作
        # 首先是 SimpleWriteCode() 然后是 SimpleRunCode()
        todo = self.rc.todo

        msg = self.get_memories(k=1)[0] # 得到最近的一条消息
        result = await todo.run(msg.content)

        msg = Message(content=result, role=self.profile, cause_by=type(todo))
        self.rc.memory.add(msg)
        return msg


async def main():
    msg = "write a function that calculates the sum of a list"
    role = RunnableCoder()
    logger.info(msg)
    result = await role.run(msg)
    logger.info(result)

asyncio.run(main())
