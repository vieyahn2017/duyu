#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'm00291095'
from string import Template
import os

s = """#!/usr/bin/python
# -*- coding: utf-8 -*-
from UnifiedStorage.Application.DataBase.TestCase.Oracle.SLOB.Longevity.SlobBase import *
from performance_reporter.performance_reporter import PerformanceReporter
from UniAutos.Util.Time import sleep
import datetime
import re
from database.oracle.oracle import Oracle
class TC_SlobUpdate50_${schema}_${thread}(SlobBase):
    \"""
    CaseId:
    RunLevel:
    EnvType:
    CaseName:
    Slob50%update ${schema} schema,${thread} threads per schema
    PreCondition:
    TestStep:
    PostCondition:
    \"""

# 测试用例参数配置.
    def createMetaData(self):
        \"""添加测试Parameter.
        \"""
        super(TC_SlobUpdate50_${schema}_${thread}, self).createMetaData()\n
    # 测试执行前配置等准备操作.
    def preTestCase(self):
        \"""添加测试用例预置条件等.
        \"""
        self.logInfo("Prepare for the case:\\na.Check GI Status.\\nb.Get Device")
        # 获取主机对象
        self.host1 = self.getDevice("host", "1")\n
    # 测试步骤
    def procedure(self):
        \"""添加测试用例测试步骤.
        \"""\n
        #采用slob工具下发IO，50%更新，运行20分钟
        self.slob_conf.update({
            "UPDATE_PCT": "50",
            "THREADS_PER_SCHEMA": "${thread}",
        })\n
        self.pid = DBIOTools(self.host1).slob.runit(schema_num="${schema}", conf_params=self.slob_conf, nohup="yes")
        sleep(60)
        # 获取当前时间和slob运行时长
        self.runtime = int(self.slob_conf["RUN_TIME"])
        self.time1 = datetime.datetime.now()
        # 采集性能监控数据
        self.reporter = PerformanceReporter(self.testSet.runningTest, self.performanceParams)
        self.reporter.start()
        # 在slob运行结束前2分钟停止性能监控数据采集
        sleep(self.runtime-120)
        self.reporter.stop()\n
    # 测试执行完成后清理等操作.
    def postTestCase(self):
        \"""添加测试用例清理操作.
        \"""
        # 通过时差等待slob运行完成
        self.time2 = datetime.datetime.now()
        if int((self.time2 - self.time1).seconds) < int(self.runtime):
            DBIOTools(self.host1).slob.wait_slobrun(time=int(self.runtime-(self.time2 - self.time1).seconds), pid=self.pid)
        else:
            self.logInfo("The slob is run over ! ")
        
        #获取SLOB工具目录下的awr报告到指定路径
        Oracle(self.host1).download_file({
                                         "source_dir": "/home/oracle/UniAutos/SLOB/",
                                         "local_dir": (self.testCaseId + "_awr"),
                                         "postfix": "html.gz"
                                         })
"""



result = Template(s)
cnt = 11
for schema in range(1, cnt):
    for thread in range(1, cnt):
        filename = "TC_SlobUpdate50_%s_%s.py" % (schema,thread)
        fp = open(filename,"wb")
        Testcasefile = result.substitute(schema=schema, thread=thread)
        fp.write(Testcasefile)
        fp.close()

