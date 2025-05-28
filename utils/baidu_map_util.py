import hashlib
import os
import urllib
from typing import Dict, Optional

import requests


class BaiduMapUtil:
    """百度地图API封装类，支持SN签名方式"""

    BASE_URL = "https://api.map.baidu.com"
    OUTPUT_FORMAT = "json"

    def __init__(self, ak: Optional[str] = None, sk: Optional[str] = None):
        """
        初始化百度地图API客户端
        """
        self.ak = ak or os.environ.get("BAIDU_MAP_AK")
        self.sk = sk or os.environ.get("BAIDU_MAP_SK")
        if not self.ak or not self.sk:
            raise ValueError("AK和SK不能为空，请设置环境变量或在初始化时提供。")

    @classmethod
    def _generate_query_str(cls, url_path: str, params: Dict[str, str]):
        params_copy = params.copy()
        # 2. 对参数键进行字典序排序
        sorted_keys = sorted(params_copy.keys())
        # 3. 构造查询字符串（不进行URL编码）
        query_parts = []
        for key in sorted_keys:
            value = str(params_copy[key])
            query_parts.append(f"{key}={value}")

        # 4. 构造待签名字符串: URL路径 + ? + 查询参数
        query_str = f"{url_path}?{'&'.join(query_parts)}"
        return query_str

    def _generate_sn(self, query_str: str) -> str:
        """
        生成SN签名 - 严格按照百度官方文档实现

        Args:
            query_str (str): 查询url
            params (Dict[str, str]): 请求参数

        Returns:
            str: 生成的SN签名
        """
        # 5. 对queryStr进行转码，safe内的保留字符不转换
        encoded_str = urllib.request.quote(query_str, safe="/:=&?#+!$,;'@()*[]")
        # 在最后直接追加上您的SK
        raw_str = encoded_str + self.sk
        # 计算sn
        sn = hashlib.md5(urllib.parse.quote_plus(raw_str).encode("utf8")).hexdigest()
        return sn

    def make_request(self, url_path: str, params: dict) -> Dict:
        """
        查询城市行政编码

        Args:
            url_path (str): 地址
            params (dict): 参数

        Returns:
            Dict: API响应结果
        """
        query_str = self._generate_query_str(url_path, params)
        # 生成SN签名
        sn = self._generate_sn(query_str)
        query_url = f"{self.BASE_URL}{query_str}&sn={sn}"
        try:
            response = requests.get(query_url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"status": -1, "message": f"请求失败: {str(e)}"}

    def get_city_admin_code(self, city_name: str) -> Dict:
        """
        查询城市行政编码

        Args:
            city_name (str): 城市名称

        Returns:
            Dict: API响应结果
        """
        url_path = "/geocoding/v3/"

        # 构造请求参数（不包含ak，ak将在请求时添加）
        params = {
            "address": city_name,
            "output": self.OUTPUT_FORMAT,
            "ak": self.ak,
        }
        response_data = self.make_request(url_path, params)
        return response_data

    def get_region_search(self, keyword: str):
        """行政区划搜索"""
        url_path = "/api_region_search/v1/"

        # 构造请求参数（不包含ak，ak将在请求时添加）
        params = {
            "keyword": keyword,
            "boundary": "0",
            "boundarycode": "adcode",
            "ak": self.ak,
        }
        response_data = self.make_request(url_path, params)
        return response_data

    def get_weather(self, location: str, data_type: str = "all"):
        url_path = "/weather/v1/"

        # 构造请求参数（不包含ak，ak将在请求时添加）
        params = {
            "location": location,
            "output": self.OUTPUT_FORMAT,
            "data_type": data_type,
            "ak": self.ak,
        }
        response_data = self.make_request(url_path, params)
        return response_data
