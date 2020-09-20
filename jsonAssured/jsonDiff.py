#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/9/10 17:32
# @Author : Louchengwang
# @Site : 
# @File : jsonDiff.py
# @Software: PyCharm
import yaml
import os
from jsonAssured.jsonPathGenerator import *
import sys
import codecs
import json
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())


class JsonPathDiff:

    def __init__(self, config_path, source_path, target_path):
        self.config_path = config_path
        self.source_path = source_path
        self.target_path = target_path
        self.config = None
        self.source = None
        self.target = None
        self.jsonpath_mapping = None
        self.json_generator = JsonPathGenerator()

    def jsondiff_run(self):
        self.get_config()
        self.source = self.get_file(self.source_path)
        self.target = self.get_file(self.target_path)

        # 根据mapping生成jsonpath mapping
        is_allflag = self.config["is_allflag"]
        if self.config["ignore"]:
            ignore = self.config["ignore"]
        else:
            ignore = []

        if is_allflag:
            print("————————————————开始进行全量比对——————————————————")
            self.all_jsonpath = self.json_generator.get_json_path(self.source, ignore=ignore, isall=True)
            result = self.json_diff_allpath(self.source, self.target, self.all_jsonpath)
            print("————————————————全量比对完成——————————————————")
            for index, res in enumerate(result):
                print("error-{}: {}".format(index, res))
        else:
            print("————————————————开始进行字段比对——————————————————")
            keymapping = self.config["keyMappings"]
            key_mapping = []
            for item in keymapping:
                key_mapping.append([item["source"], item["target"]])
            print("————————————————获取比对字段mapping——————————————————")
            for item in key_mapping:
                print(item)
            # 写入yaml文件
            if "keyJsonPathMappings" not in self.config:
                print("————————————————获取字段jsonpath mapping——————————————————")
                mappings = self.json_generator.get_jsonpath_mapping(self.source, self.target, key_mapping)
                print(json.dumps(mappings, indent=4, separators=(', ', ': ')))
                self.config["keyJsonPathMappings"] = mappings
                with open(self.config_path, 'w', encoding='utf-8') as f:
                    yaml.dump(self.config, f)
                self.get_config()
            result = self.json_diff_keypath(self.source, self.target, self.config["keyJsonPathMappings"])
            print("————————————————字段比对完成——————————————————")
            for index, res in enumerate(result):
                print("error-{}: {}".format(index, res))

    def get_config(self):
        """
        获取config配置
        :param config_path: mapping配置文件路径
        :return:
        """
        print("————————————————————开始读取mapping配置————————————————————")
        if os.path.exists(self.config_path):
            with open(self.config_path, "r", encoding="utf-8") as f:
                config = yaml.load(f, Loader=yaml.Loader)
                self.config = config
                print("mapping文件读取成功")
                print(json.dumps(config, indent=4, separators=(', ', ': ')))
        else:
            print("路径:{}错误，未找到该mapping文件".format(self.config_path))

    def get_file(self, file_path):
        """
         读取文件内容
        :param file_path: 文件路径
        :return:
        """
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                f_strs = f.read()
                return json.loads(f_strs)
        else:
            print("路径：{}错误，未找到该文件".format(file_path))

    def get_value_by_jsonpath(self, soure, jsonpath_str):
        """
         获取jsonpath下的数据
        :param soure: 数据json
        :param jsonpath_str: jsonpath
        :return: 结果集list
        """
        result = jsonpath.jsonpath(soure, jsonpath_str)
        if not result:
            result = []
            print("检查jsonpath语法是否正确")
        return result

    def json_diff_allpath(self, source, target, jsonpaths):
        result = {
            "error_list": [],
        }
        for jsonpath in jsonpaths:
            source_res = self.get_value_by_jsonpath(source, jsonpath)
            target_res = self.get_value_by_jsonpath(target, jsonpath)
            if source_res != target_res:
                result["error_list"].append(jsonpath)
        return result

    def json_diff_keypath(self, source, target, mappings):
        """
        json比对
        :param soure:  源json数据
        :param target: 目标json数据
        :param pathMappings: pathmappings
        :return:
        """
        result = {
            "res_list": [],
        }

        for mapping in mappings:
            source_key = list(mapping["source"].keys())[0]
            print(source_key)
            soure_res = self.get_value_by_jsonpath(source, mapping["source"][source_key])
            print("soure res : {}".format(soure_res))
            target_key = list(mapping["target"].keys())[0]
            target_res = self.get_value_by_jsonpath(target, mapping["target"][target_key])
            print("target res: {}".format(target_res))
            if type(soure_res) != type(target_res):
                result["message"] = "校验格式错误"
                return result
            if len(soure_res) != len(target_res):
                result["message"] = "数据量不匹配"
                return result
            check_set = set()
            for soure_res_value in soure_res:
                check_set.add(soure_res_value)
            for index, target_res_value in enumerate(target_res):
                if target_res_value not in check_set:
                    result["res_list"].append("index= {},  value={}未在源数据中".format(index, target_res_value))
        return result

    def get_all_key_jsonpath(self, json_str):
        pass

def main():
    config_path = sys.argv[1]
    source_path = sys.argv[2]
    target_path = sys.argv[3]

    jsonAssured = JsonPathDiff(config_path, source_path, target_path)
    jsonAssured.jsondiff_run()


if __name__ == '__main__':

    # mapping_path = "/Users/bjhl/Desktop/code/py-rest-assured/mapping.yaml"
    # source_path = "/Users/bjhl/Desktop/code/py-rest-assured/source.json"
    # target_path = "/Users/bjhl/Desktop/code/py-rest-assured/target_all.json"
    # jsonAssured = JsonPathDiff(mapping_path, source_path, target_path)
    # res = jsonAssured.json_diff(soure_str, target_str, path_mappings)
    # print(res)

    # jsonAssured.jsondiff_run()
   main()

