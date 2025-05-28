from typing import Type

import dotenv
from langchain_community.tools import GoogleSerperRun
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_core.messages import ToolMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from utils.baidu_map_util import BaiduMapUtil

dotenv.load_dotenv()


class BaiduMapWeatherArgsSchema(BaseModel):
    city: str = Field(description="需要查询天气预报的目标城市，例如：广州")


class GoogleSerperArgsSchema(BaseModel):
    query: str = Field(description="执行谷歌搜索的查询语句")


class BaiduMapWeatherTool(BaseTool):
    """根据传入城市名称查询天气预报"""

    name: str = "baidu_map_weather"
    args_schema: Type[BaseModel] = BaiduMapWeatherArgsSchema
    description: str = "当你想查询天气或者天气相关的问题时可以使用的工具"

    def _run(self, *args, **kwargs):
        try:
            city = kwargs.get("city", "")
            baidu_map_util = BaiduMapUtil()
            # 根据city获取location
            city_response = baidu_map_util.get_city_admin_code(city)
            city_location = city_response.get("result", {}).get("location", {})
            lng = city_location.get("lng", "")  # 经度值
            lat = city_location.get("lat", "")  # 纬度值
            # 根据location获取天气信息
            weather_response = baidu_map_util.get_weather(location=f"{lng},{lat}")
            return weather_response
        except Exception as e:
            return f"获取{kwargs.get('city', '')}天气预报信息失败,{e}"


# 1.定义工具列表
baidu_map_weather = BaiduMapWeatherTool()
google_serper = GoogleSerperRun(
    name="google_serper",
    description=(
        "一个低成本的谷歌搜索API。" "当你需要回答有关时事的问题时，可以调用该工具。" "该工具传递的参数是搜索查询语句。"
    ),
    args_schema=GoogleSerperArgsSchema,
    api_wrapper=GoogleSerperAPIWrapper(),
)

tool_dict = {baidu_map_weather.name: baidu_map_weather, google_serper.name: google_serper}
tools = [tool for tool in tool_dict.values()]
# 2.创建Prompt
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "你是由OpenAI开发的聊天机器人，可以帮助用户回答问题，必要时刻请调用工具帮助用户解答，如果问题需要多个工具回答，请一次性调用所有工具，不要分步调用",
        ),
        ("human", "{query}"),
    ]
)
# 3.创建大语言模型并绑定工具
llm = ChatOpenAI(model="gpt-4o")
llm_with_tool = llm.bind_tools(tools=tools)

# 4.创建链应用
chain = {"query": RunnablePassthrough()} | prompt | llm_with_tool
# 5.调用链应用，并获取输出响应
query = "上海现在天气怎样，并且请用谷歌搜索工具查询一下2024年巴黎奥运会中国代表团共获得几枚金牌？"
resp = chain.invoke(query)
tool_calls = resp.tool_calls
# 6.判断是工具调用还是正常输出结果
if len(tool_calls) <= 0:
    print("生成内容: ", resp.content)
else:
    # 7.将历史的系统消息、人类消息、AI消息组合
    messages = prompt.invoke(query).to_messages()
    messages.append(resp)

    # 8.循环遍历所有工具调用信息
    for tool_call in tool_calls:
        tool = tool_dict.get(tool_call.get("name"))  # 获取需要执行的工具
        print("正在执行工具: ", tool.name)
        content = tool.invoke(tool_call.get("args"))  # 工具执行的内容/结果
        print("工具返回结果: ", content)
        tool_call_id = tool_call.get("id")
        messages.append(
            ToolMessage(
                content=content,
                tool_call_id=tool_call_id,
            )
        )
    print("输出内容: ", llm.invoke(messages).content)
