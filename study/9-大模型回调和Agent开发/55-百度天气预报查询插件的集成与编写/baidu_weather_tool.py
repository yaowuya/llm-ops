from typing import Type

import dotenv
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from utils.baidu_map_util import BaiduMapUtil

dotenv.load_dotenv()


class BaiduMapWeatherArgsSchema(BaseModel):
    city: str = Field(description="需要查询天气预报的目标城市，例如：广州")


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


baidu_map_weather = BaiduMapWeatherTool()
print(baidu_map_weather.invoke({"city": "北京"}))
