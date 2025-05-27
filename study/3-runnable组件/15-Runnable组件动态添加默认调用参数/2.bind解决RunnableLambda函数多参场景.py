import random

from langchain_core.runnables import RunnableLambda


def get_weather(location: str, unit: str, name: str):
    """
    根据传入的位置+温度单位获取对应的天气信息
    :param unit: 单位
    :param name: 姓名
    :return: 天气信息
    """
    print(location, unit, name)
    return f"{location}天气为{random.randint(24, 40)}{unit}"


get_weather_runnable = RunnableLambda(get_weather).bind(unit="摄氏度", name="张三")
resp = get_weather_runnable.invoke("广州")
print(resp)
