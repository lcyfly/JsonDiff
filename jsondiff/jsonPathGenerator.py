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


if __name__ == '__main__':
    json_path_generator = JsonPathGenerator()
    json_str = {"code": 0, "data": {"list": [
        {"pager": "null", "id": 30465, "number": 5679210103998976, "name": "直考通优惠券a", "restrictList": "null",
         "useMode": 0, "useCondition": 0, "denomination": "20", "amount": 50, "activeTime": 1599667200000,
         "expiredTime": 1600012799000, "drawCount": 1, "useCount": 1, "courseDetailShow": 0, "status": 1,
         "statusName": "上线", "discountType": 1, "expiredType": 0, "limitDrawCount": 10, "creatorId": 1079,
         "spreadWay": 2, "spreadWayName": "优惠券码", "suitMode": 1, "suitModeName": "指定班级", "subjectList": [],
         "subjectName": "", "subjectIds": [], "systemSpreadType": 0, "creditGiftLinked": 0,
         "createTime": [2020, 9, 10, 19, 43, 42], "updateTime": "null", "couponStudentNumber": 0,
         "couponStudentCode": "", "floatType": 0, "floatDay": 0},
        {"pager": "null", "id": 30464, "number": 5679091932891648, "name": "优惠券by0910", "restrictList": "null",
         "useMode": 0, "useCondition": 0, "denomination": "2", "amount": 50, "activeTime": 1599667200000,
         "expiredTime": 1599926399000, "drawCount": 0, "useCount": 0, "courseDetailShow": 0, "status": 4,
         "statusName": "过期", "discountType": 1, "expiredType": 0, "limitDrawCount": 10, "creatorId": 1079,
         "spreadWay": 2, "spreadWayName": "优惠券码", "suitMode": 1, "suitModeName": "指定班级", "subjectList": [],
         "subjectName": "", "subjectIds": [], "systemSpreadType": 0, "creditGiftLinked": 0,
         "createTime": [2020, 9, 10, 19, 13, 38], "updateTime": "null", "couponStudentNumber": 0,
         "couponStudentCode": "", "floatType": 0, "floatDay": 0},
        {"pager": "null", "id": 30463, "number": 5679046643059200, "name": "直考通优惠券by", "restrictList": "null",
         "useMode": 0, "useCondition": 0, "denomination": "5", "amount": 50, "activeTime": 1599667200000,
         "expiredTime": 1600012799000, "drawCount": 0, "useCount": 0, "courseDetailShow": 0, "status": 1,
         "statusName": "上线", "discountType": 1, "expiredType": 0, "limitDrawCount": 10, "creatorId": 1079,
         "spreadWay": 2, "spreadWayName": "优惠券码", "suitMode": 1, "suitModeName": "指定班级", "subjectList": [],
         "subjectName": "", "subjectIds": [], "systemSpreadType": 0, "creditGiftLinked": 0,
         "createTime": [2020, 9, 10, 19, 2, 7], "updateTime": "null", "couponStudentNumber": 0, "couponStudentCode": "",
         "floatType": 0, "floatDay": 0},
        {"pager": "null", "id": 30462, "number": 5679033203591680, "name": "直考通优惠券3", "restrictList": "null",
         "useMode": 0, "useCondition": 0, "denomination": "5", "amount": 50, "activeTime": 1599667200000,
         "expiredTime": 1599839999000, "drawCount": 0, "useCount": 0, "courseDetailShow": 0, "status": 4,
         "statusName": "过期", "discountType": 1, "expiredType": 0, "limitDrawCount": 10, "creatorId": 1079,
         "spreadWay": 2, "spreadWayName": "优惠券码", "suitMode": 1, "suitModeName": "指定班级", "subjectList": [],
         "subjectName": "", "subjectIds": [], "systemSpreadType": 0, "creditGiftLinked": 0,
         "createTime": [2020, 9, 10, 18, 58, 42], "updateTime": "null", "couponStudentNumber": 0,
         "couponStudentCode": "", "floatType": 0, "floatDay": 0},
        {"pager": "null", "id": 30461, "number": 5679013476272640, "name": "直考通优惠券2", "restrictList": "null",
         "useMode": 0, "useCondition": 0, "denomination": "5", "amount": 50, "activeTime": 1599667200000,
         "expiredTime": 1599926399000, "drawCount": 0, "useCount": 0, "courseDetailShow": 0, "status": 4,
         "statusName": "过期", "discountType": 1, "expiredType": 0, "limitDrawCount": 10, "creatorId": 1079,
         "spreadWay": 2, "spreadWayName": "优惠券码", "suitMode": 1, "suitModeName": "指定班级", "subjectList": [],
         "subjectName": "", "subjectIds": [], "systemSpreadType": 0, "creditGiftLinked": 0,
         "createTime": [2020, 9, 10, 18, 53, 41], "updateTime": "null", "couponStudentNumber": 0,
         "couponStudentCode": "", "floatType": 0, "floatDay": 0},
        {"pager": "null", "id": 30460, "number": 5678988614339072, "name": "直考通优惠券1", "restrictList": "null",
         "useMode": 0, "useCondition": 0, "denomination": "5", "amount": 50, "activeTime": 1599667200000,
         "expiredTime": 1599926399000, "drawCount": 0, "useCount": 0, "courseDetailShow": 0, "status": 4,
         "statusName": "过期", "discountType": 1, "expiredType": 0, "limitDrawCount": 10, "creatorId": 1079,
         "spreadWay": 2, "spreadWayName": "优惠券码", "suitMode": 1, "suitModeName": "指定班级", "subjectList": [],
         "subjectName": "", "subjectIds": [], "systemSpreadType": 0, "creditGiftLinked": 0,
         "createTime": [2020, 9, 10, 18, 47, 22], "updateTime": "null", "couponStudentNumber": 0,
         "couponStudentCode": "", "floatType": 0, "floatDay": 0},
        {"pager": "null", "id": 30459, "number": 5678387090524672, "name": "by0910优惠券", "restrictList": "null",
         "useMode": 0, "useCondition": 0, "denomination": "5", "amount": 50, "activeTime": 1599667200000,
         "expiredTime": 1599839999000, "drawCount": 2, "useCount": 1, "courseDetailShow": 0, "status": 4,
         "statusName": "过期", "discountType": 1, "expiredType": 0, "limitDrawCount": 10, "creatorId": 1079,
         "spreadWay": 2, "spreadWayName": "优惠券码", "suitMode": 1, "suitModeName": "指定班级", "subjectList": [],
         "subjectName": "", "subjectIds": [], "systemSpreadType": 0, "creditGiftLinked": 0,
         "createTime": [2020, 9, 10, 16, 14, 23], "updateTime": "null", "couponStudentNumber": 0,
         "couponStudentCode": "", "floatType": 0, "floatDay": 0},
        {"pager": "null", "id": 30458, "number": 5678376844560896, "name": "金囿0910优惠券", "restrictList": "null",
         "useMode": 0, "useCondition": 0, "denomination": "5", "amount": 50, "activeTime": 1599667200000,
         "expiredTime": 1600099199000, "drawCount": 0, "useCount": 0, "courseDetailShow": 0, "status": 2,
         "statusName": "下线", "discountType": 1, "expiredType": 0, "limitDrawCount": 10, "creatorId": 1079,
         "spreadWay": 1, "spreadWayName": "链接", "suitMode": 1, "suitModeName": "指定班级", "subjectList": [],
         "subjectName": "", "subjectIds": [], "systemSpreadType": 0, "creditGiftLinked": 0,
         "createTime": [2020, 9, 10, 16, 11, 47], "updateTime": [2020, 9, 10, 16, 13, 17], "couponStudentNumber": 0,
         "couponStudentCode": "", "floatType": 0, "floatDay": 0},
        {"pager": "null", "id": 30384, "number": 5343123496471040, "name": "一二三四五六七", "restrictList": "null",
         "useMode": 0, "useCondition": 0, "denomination": "999999", "amount": 9999, "activeTime": 1594569600000,
         "expiredTime": 1596211199000, "drawCount": 2, "useCount": 2, "courseDetailShow": 0, "status": 4,
         "statusName": "过期", "discountType": 1, "expiredType": 0, "limitDrawCount": 99, "creatorId": 504,
         "spreadWay": 2, "spreadWayName": "优惠券码", "suitMode": 1, "suitModeName": "指定班级", "subjectList": [],
         "subjectName": "", "subjectIds": [], "systemSpreadType": 0, "creditGiftLinked": 0,
         "createTime": [2020, 7, 13, 11, 12, 27], "updateTime": [2020, 7, 13, 19, 7, 22], "couponStudentNumber": 0,
         "couponStudentCode": "", "floatType": 0, "floatDay": 0}]}, "msg": "null",
                "pager": {"pageNum": 1, "pageSize": 50, "count": 61}}
    result = json_path_generator.get_json_path(json_str, isall=False)
    # result = json_path_generator.get_jsonpath_by_key(json_str, ["number", "name"])
    print(result)
    # for res in result:
    #     res_str = jsonpath.jsonpath(json_str, res)
    #     print(res)
    #     print(res_str)

    target = {
        "store": {
            "book": [{
                "category": "reference",
                "author": "Nigel Rees",
                "title": "Sayings of the Century",
                "price": 8.95
            }, {
                "category": "fiction",
                "author": "Evelyn Waugh",
                "title": "Sword of Honour",
                "price": 12.99
            }, {
                "category": "fiction",
                "author": "Herman Melville",
                "title": "Moby Dick",
                "isbn": "0-553-21311-3",
                "price": 8.99
            }, {
                "category": "fiction",
                "author": "J. R. R. Tolkien",
                "title": "The Lord of the Rings",
                "isbn": "0-395-19395-8",
                "price": 22.99
            }],
            "bicycle": {
                "color": "red",
                "price": 19.95
            }
        },
        "expensive": 10
    }

    result_map = json_path_generator.get_jsonpath_mapping(source=json_str, target=target, key_mapping=[
        ["number1", "price"],
        ["name", "author"]
    ])

    print(result_map)

    # allpath = json_path_generator.get_all_jsonpath(json_str, ignore=["expiredTime", "drawCount", "activeTime"])
    # for i in allpath:
    #     print(i)
