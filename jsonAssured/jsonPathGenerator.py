#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/9/11 18:29
# @Author : Louchengwang
# @File : jsonPathGenerator.py
# @Dream: NO BUG
import json
import jsonpath


class JsonPathGenerator:

    def get_all_jsonpath(self, json_data):
        """
        获取所有字段jsonpath
        :param json_data:
        :return:
        """
        return self.get_json_path(json_data, isall=True)

    def get_json_path(self, json_data, json_path="$", result=[], ignore=[], isall=False):
        """
        获取json数据的jsonpath
        :param json_data:   json数据
        :param json_path:   jsonpath前缀
        :param result:      结果集
        :param ignore:      要忽略的字段
        :param isall:       是否获取所有字段（如果为True list结构也获取所有item）
        :return:
        """
        if isinstance(json_data, dict):
            for k, v in json_data.items():
                temp_json_path = json_path
                temp_json_path += "." + k
                if k not in ignore and not isinstance(v, dict) and not isinstance(v, list):
                    result.append(temp_json_path)
                self.get_json_path(v, temp_json_path, result, ignore,isall)
        elif isinstance(json_data, list):
            if len(json_data) > 0:
                if isall:
                    for index, data in enumerate(json_data):
                        temp_jspath = json_path
                        temp_jspath += "[{}]".format(index)
                        self.get_json_path(json_data[index], temp_jspath, result, ignore, isall)
                else:
                    json_path += "[*]"
                    self.get_json_path(json_data[0], json_path, result, ignore, isall)
        elif isinstance(json_data, int):
            return
        elif isinstance(json_data, str):
            return
        return result

    def get_jsonpath_by_key(self, json_data, keys):
        """
        获取特定key的jsonpath, 默认查询key唯一
        :param json_data: json数据
        :param keys: 查询key列表
        :return:
        """
        if len(keys) <= 0:
            return {}
        key_list = keys
        all_jsonpath = self.get_json_path(json_data)
        res = {}
        path_res = {}
        for jspath in all_jsonpath:
            path_end = jspath.split(".")[-1]
            path_res[path_end] = jspath
        for k in key_list:
            if k in path_res:
                res[k] = path_res[k]
            else:
                print("key: {}字段未在json数据中查询到，请检查该字段是否正确".format(k))
                res[k] = "未找到该字段，检查字段名"

        return res

    def get_jsonpath_mapping(self, source, target, key_mapping):
        """
        获取jsonpath mapping
        :param source: 源数据
        :param target: 目标数据
        :param key_mapping: key映射
        :example:
        key_mapping = [
            ["num", "number"],
            ["user", "user_info"]
        ]
        :return:
        """
        result_mapping = []
        for item in key_mapping:
            source_jspath = self.get_jsonpath_by_key(source, [item[0]])
            target_jspath = self.get_jsonpath_by_key(target, [item[1]])
            result_mapping.append({"source": source_jspath, "target": target_jspath})
        return result_mapping

