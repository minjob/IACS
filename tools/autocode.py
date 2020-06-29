#!/usr/bin/ python
# -*- coding:utf-8 -*-
import time, os, sys,shutil
import xlrd
from flask import Flask
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData, create_engine
metadata = MetaData()
import json
import datetime

app = Flask(__name__)

from tools.MESLogger import MESLogger
logger = MESLogger('../logs', 'log')

from dbset.database.db_operate import DB_URL
engine = create_engine(DB_URL)
conn = engine.connect()
Session = sessionmaker(bind=engine)
db_session = Session()

PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))

global classCount, lastClassName


class MakeModel:
    def __init__(self):

        self.name = 'Xujin'

    # 类型替换
    def changeDataTpye(self,s,length):
        strRe = s
        if 'VARCHAR' in s.upper():
            strRe = s.upper().replace("VARCHAR","Unicode")+"("+str(length)+")"
        elif s.upper() == 'DATETIME':
            strRe = 'DateTime'
        elif s.upper() == 'INT':
            strRe = 'Integer'
        elif s.upper() == 'DINT':
            strRe = 'BigInteger'
        elif s.upper() == 'TRUE':
            strRe = 'True'
        elif s.upper() == 'FALSE':
            strRe = 'False'
        elif s.upper() == 'BOOL':
            strRe = 'BIT'
        elif s.upper() == 'FLOAT':
            strRe = 'Float(53)'
        elif s.upper() == 'REAL':
            strRe = 'Float(24)'
        return strRe

    # 写入开发信息
    def makeDevNotes(self):
        st = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        notes = '\n'
        notes += '#/******************************************************************************************\n'
        notes += '# ************* STK make model usage:\n'
        notes += '# ************* version: print python3.6.3  version\n'
        notes += '# ************* make: make Python file\n'
        notes += '# ************* STK makemodel.py 1.0.0\n'
        notes += '# ************* @author ' + self.name + '\n'
        notes += '# ************* @date ' + st + '\n'
        notes += '# ************* @Model \n'
        notes += '# ******************************************************************************************/\n'
        return notes

    # 引入所使用数据库开发引擎信息
    def makeImportNotes(self):
        notes = '\n'
        notes += '#引入必要的类库\n'
        notes += 'from sqlalchemy.ext.declarative import declarative_base\n'
        notes += 'from sqlalchemy.orm import sessionmaker, relationship\n'
        notes += 'from sqlalchemy import create_engine, Column,ForeignKey, Table, DateTime, Integer, String\n'
        notes += 'from sqlalchemy import Column, DateTime, Float, Integer, String, Unicode,BigInteger\n'
        notes += 'from sqlalchemy.dialects.mssql.base import BIT\n'
        notes += 'from dbset.database.db_operate import GLOBAL_DATABASE_CONNECT_STRING\n'
        notes += 'from datetime import datetime\n'
        notes += 'from flask_login import LoginManager\n'
        notes += 'from werkzeug.security import generate_password_hash, check_password_hash\n'
        return notes

    # 引入使用数据库引擎
    def makeDBNotes(self):
        notes = '\n'
        notes += '#引入mssql数据库引擎\n'
        notes += 'import pymssql\n'

        return notes

    # 创建对象的基类
    def makeBaseModel(self):
        notes = ''
        sqlstring = "GLOBAL_DATABASE_CONNECT_STRING"
        notes = '\n'
        notes += '# 创建对象的基类\n'
        notes += "engine = create_engine(" + "\n\t\t"
        notes += "{0}, deprecate_large_types=True,"""+"\n\t\t"
        notes += "max_overflow=0,  # 超过连接池大小外最多创建的连接\n\t\t"
        notes += "pool_size=100,  # 连接池大小\n\t\t"
        notes += "pool_timeout=50,  # 池中没有线程最多等待的时间，否则报错\n\t\t"
        notes += "pool_recycle=-1  # 多久之后对线程池中的线程进行一次连接的回收（重置）\n\t\t"
        notes += " # echo = True   #输出SQL\n"
        notes += ")\n"
        notes += "SessionFactory = sessionmaker(bind=engine)\n"
        notes += "session = SessionFactory()\n"
        notes += 'Base = declarative_base(engine)\n'
        notes = notes.replace("{0}",sqlstring)
        return notes

    def makeEndImplement(self):
        notes = '\n'
        notes += '# 生成表单的执行语句_START\n'
        notes += 'Base.metadata.create_all(engine)\n'
        # notes += "def init_db():\n\t"
        # notes += "try:\n\t\t"
        # notes += "Base.metadata.create_all(engine)\n\t"
        # notes += "except Exception as err:\n\t\t"
        # notes += "raise Exception('创建数据库出错！错误信息为：' + str(err))\n"
        notes += "\n"
        notes += '# 生成表单的执行语句_END\n'

        return notes

    # 创建对象的基类
    def makeORMObjectModel(self):
        notes = '\n'
        notes = '\n'
        notes += '# 定义user对象\n\t'
        return notes

    # 创建通用列
    def makeGeneralKeyModel(self,comment,name,type,primarykey,autoincrement,nullable,length):
        notes = '\n\t'
        notes += '#' + comment + ':\n\t'
        notes += '{0} = Column({1}, primary_key = {2}, autoincrement = {3}, nullable = {4})\n\t'
        notes = notes.replace("{0}", name)
        type = self.changeDataTpye(type,length)
        notes = notes.replace("{1}", type)
        primarykey = self.changeDataTpye(primarykey,"")
        notes = notes.replace("{2}", primarykey)
        autoincrement = self.changeDataTpye(autoincrement,"")
        notes = notes.replace("{3}", autoincrement)
        nullable = self.changeDataTpye(nullable,"")
        notes = notes.replace("{4}", nullable)
        return notes

    def makeGeneralKeyTableModel(self,comment,name,type,primarykey,autoincrement,nullable):
        notes = '\n\t'
        notes += '#' + comment + ':\n\t'
        notes += '{0} = Column({1}, primary_key = {2}, autoincrement = {3}, nullable = {4}),\n\t'
        notes = notes.replace("{0}", name)
        type = self.changeDataTpye(type)
        notes = notes.replace("{1}", type)
        primarykey = self.changeDataTpye(primarykey)
        notes = notes.replace("{2}", primarykey)
        autoincrement = self.changeDataTpye(autoincrement)
        notes = notes.replace("{3}", autoincrement)
        nullable = self.changeDataTpye(nullable)
        notes = notes.replace("{4}", nullable)
        return notes

    # 创建外键
    def makeForeignkeyModel(self, comment,name, type, foreignkey, autoincrement, nullable):
        notes = '\n\t'
        notes += '#' + comment + ':\n\t'
        notes += '{0} =Column({1}, ForeignKey("{2}"), nullable=False, primary_key=False)\n'
        notes = notes.replace("{0}", name)
        type = self.changeDataTpye(type)
        notes = notes.replace("{1}", type)
        notes = notes.replace("{2}", foreignkey)
        return notes

    def makeForeignkeyTableModel(self, comment,name, type, foreignkey, autoincrement, nullable):
        notes = '\n\t'
        notes += '#' + comment + ':\n\t'
        notes += 'Column("{0}",{1}, ForeignKey("{2}"), nullable=False, primary_key=False),\n'
        notes = notes.replace("{0}", name)
        type = self.changeDataTpye(type)
        notes = notes.replace("{1}", type)
        notes = notes.replace("{2}", foreignkey)
        return notes

    # 创建关系
    def makeRelationModel(self, name, relation):
        notes = '\n\t'
        notes +=  '#Relation ' + name + ':\n\t'
        notes += """{0} = relationship("{0}", secondary={1})""" + '\n\t'
        notes = notes.replace("{0}", name)
        notes = notes.replace("{1}", relation)
        return notes

    # 创建关系表表头
    def makeRelationFrontModel(self, name):
        notes = '\n'
        notes += '#中间表' + name+ ':\n'
        notes += """{0} = Table(\n\t"{0}",\n\t
    Base.metadata,""" + '\n\t'
        notes = notes.replace("{0}", name)
        return notes

    # 创建ORM类前文件
    def makeORMFrontModel(self, name):
        notes = '\n'
        notes += '#' + name + '_START:\n'
        notes += """class {0}(Base):""" + '\n\t'
        notes += """__tablename__ = "{0}" """+"\n\t"
        notes = notes.replace("{0}", name)
        return notes

    def checkFileExists(self, fileName):
        fn = fileName + '.py'
        if os.path.exists(fn):
            print ('File already exists, please check file and try again.')
            sys.exit()

    def makeModelPythonFile(self, fileName,fileString):
        # self.checkFileExists(fileName)
        # print('Make \'' + fileName + '\' waiting...')
        f = open(fileName, 'w',encoding='utf-8')
        f.write(fileString)
        f.close()

    def ModifyModel(self,AFilename,ATableName):
        currentPath = os.path.abspath('.')
        model_path = PATH(currentPath + r'\\' + AFilename)
        i = 0
        tmp = ""
        try:
            if not os.path.exists(model_path):
                print("不存在！")
            else:
                # print("存在!!")
                with open(AFilename, 'r', encoding='UTF-8') as f:
                    lines = f.readlines()
                    i = 0
                    strTbStart = "#" + ATableName + "_START"
                    strTbEnd = "#" + ATableName + "_END"
                    strExecStart = "# 生成表单的执行语句_START"
                    strExecEnd = "# 生成表单的执行语句_END"
                    isExist = "FLASE"
                    for line in lines:
                        iposstart = line.find(strTbStart)
                        iposend = line.find(strTbEnd)
                        istart = line.find(strExecStart)
                        iend = line.find(strExecEnd)
                        if iposstart >= 0:
                            isExist = "TRUE"
                            i = 1
                            continue
                        elif iposend >= 0:
                            i = 0
                            continue
                        elif istart >= 0:
                            i = 1
                            continue
                        elif iend >= 0:
                            i = 0
                            continue
                        elif i == 1:
                            continue
                        tmp += line
                if tmp is "":
                    tmp += self.makeDevNotes()
                    tmp += self.makeImportNotes()
                    tmp += self.makeDBNotes()
                    tmp += self.makeBaseModel()
                    tmp += self.makeEndImplement()
                if isExist == "TRUE":
                    ATableNameNew = ATableName + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    sql = "EXEC sp_rename '" +ATableName+"', '"+ATableNameNew+"'"
                    db_session.execute(sql)
                    db_session.commit()
            f = open(AFilename, 'w', encoding='utf-8')
            f.write(tmp)
            f.close()
            return tmp
        except Exception as e:
            print(e)
            os.remove("make_model_test.txt")
            db_session.rollback()
            logger.error(e)


    def makeModelBySheet(self):
        #读取配置文件
        #获取工程所在的路径，如果加入目录名字切换到该目录下
        currentPath = os.path.abspath('.')
        models_xls_path = currentPath + '\\models\\'
        modelsxls = models_xls_path + 'model_Test20180317.xlsx'
        try:
            book = xlrd.open_workbook(modelsxls)
        except Exception as e:
            print('打开出错，错误为：' + e)

        #循环所有Sheet
        for sheet in book.sheets():
            pythonFileName = sheet.name
            sheetRowscount = sheet.nrows
            prewRowName = ''
            nowRowName = ''
            tpl = ''
            tpl += self.makeDevNotes()
            tpl += self.makeImportNotes()
            tpl += self.makeDBNotes()
            tpl += self.makeBaseModel()

            # 遍历sheet表中所有行，生成通用的类
            prewRowName = ''
            for i in range(1, sheetRowscount):
                nowRowName = sheet.cell(i,1).value
                if prewRowName != nowRowName:
                    if prewRowName == '':
                        tpl += self.makeORMFrontModel(sheet.cell(i,1).value)
                        tpl += self.makeGeneralKeyModel(sheet.cell(i,5).value,sheet.cell(i,3).value,sheet.cell(i,4).value,
                                                        sheet.cell(i,6).value,sheet.cell(i,7).value,
                                                        sheet.cell(i,8).value)
                    else:
                        tpl += '\n'
                        tpl += '#' + prewRowName + '_END:\n'
                        tpl += self.makeORMFrontModel(sheet.cell(i, 1).value)
                        tpl += self.makeGeneralKeyModel(sheet.cell(i, 5).value, sheet.cell(i, 3).value,
                                                        sheet.cell(i, 4).value,
                                                        sheet.cell(i, 6).value, sheet.cell(i, 7).value,
                                                        sheet.cell(i, 8).value)
                else:
                    tpl += self.makeGeneralKeyModel(sheet.cell(i, 5).value,sheet.cell(i, 3).value, sheet.cell(i, 4).value,
                                                    sheet.cell(i, 6).value, sheet.cell(i, 7).value,
                                                    sheet.cell(i, 8).value)
                prewRowName = nowRowName
            tpl += '\n'
            tpl += '#' + prewRowName + '_END:\n'
            if len(tpl) > 10:
                tpl += self.makeEndImplement()
                self.makeModelPythonFile(pythonFileName, tpl)

    def makeModel(self, data, AModifyString, tableName):
        try:
            import os, configparser
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            pythonFileName = os.path.join(BASE_DIR, r'models\SystemManagement\core.py')
            tpl = ''
            # tpl += self.makeDevNotes()
            # tpl += self.makeImportNotes()
            # tpl += self.makeDBNotes()
            # tpl += self.makeBaseModel()
            tpl += self.makeORMFrontModel(tableName)
            if tableName == "User":
                tpl += self.makeGeneralKeyModel("id", "id", "Integer", "True", "True", "False", "")
            else:
                tpl += self.makeGeneralKeyModel("ID", "ID", "Integer", "True", "True", "False", "")
            str = data[1:-1].split(";")
            for i in str:
                i = json.loads(i)
                tpl += self.makeGeneralKeyModel(i.get("comment"), i.get("FieldName"), i.get("type"),
                                                i.get("primarykey"), i.get("autoincrement"), i.get("nullable"), i.get("length"))

            tpl += '\n'
            tpl += '#' + tableName + '_END:\n'
            if len(tpl) > 10:
                tpl += self.makeEndImplement()
                notes = AModifyString + tpl
                self.makeModelPythonFile(pythonFileName, notes)
        except Exception as e:
            os.remove("make_model_test.txt")
            print(e)
            logger.error(e)

    def ModifyAddModel(self,AModifyString):
        #读取配置文件
        #获取工程所在的路径，如果加入目录名字切换到该目录下
        currentPath = os.path.abspath('.')
        models_xls_path = currentPath + '\\models\\'
        modelsxls = models_xls_path + 'model_Test20180317.xlsx'
        try:
            book = xlrd.open_workbook(modelsxls)
        except Exception as e:
            print('打开出错，错误为：' + e)

        #循环所有Sheet
        for sheet in book.sheets():
            pythonFileName = sheet.name
            sheetRowscount = sheet.nrows
            prewRowName = ''
            nowRowName = ''
            tpl = ''
            tpl += self.makeDevNotes()
            tpl += self.makeImportNotes()
            tpl += self.makeDBNotes()
            tpl += self.makeBaseModel()

            # 遍历sheet表中所有行，生成通用的类
            prewRowName = ''
            for i in range(1, sheetRowscount):
                nowRowName = sheet.cell(i,1).value
                if prewRowName != nowRowName:
                    if prewRowName == '':
                        tpl += self.makeORMFrontModel(sheet.cell(i,1).value)
                        tpl += self.makeGeneralKeyModel(sheet.cell(i,5).value,sheet.cell(i,3).value,sheet.cell(i,4).value,
                                                        sheet.cell(i,6).value,sheet.cell(i,7).value,
                                                        sheet.cell(i,8).value)
                    else:
                        tpl += '\n'
                        tpl += '#' + prewRowName + '_END:\n'
                        tpl += self.makeORMFrontModel(sheet.cell(i, 1).value)
                        tpl += self.makeGeneralKeyModel(sheet.cell(i, 5).value, sheet.cell(i, 3).value,
                                                        sheet.cell(i, 4).value,
                                                        sheet.cell(i, 6).value, sheet.cell(i, 7).value,
                                                        sheet.cell(i, 8).value)
                else:
                    tpl += self.makeGeneralKeyModel(sheet.cell(i, 5).value,sheet.cell(i, 3).value, sheet.cell(i, 4).value,
                                                    sheet.cell(i, 6).value, sheet.cell(i, 7).value,
                                                    sheet.cell(i, 8).value)
                prewRowName = nowRowName
            tpl += '\n'
            tpl += '#' + prewRowName + '_END:\n'
            if len(tpl) > 10:
                tpl += self.makeEndImplement()
                notes = AModifyString + tpl
                self.makeModelPythonFile(pythonFileName, notes)

def make_model_main(data):
    try:
        import os,configparser
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        oldFileName = os.path.join(BASE_DIR,r'models\SystemManagement\core.py')
        backFileName = os.path.join(BASE_DIR,r'models\SystemManagement\core_black.py')
        shutil.copyfile(oldFileName, backFileName)
        newFileName = "make_model_test.txt"
        os.rename(backFileName,newFileName)
        model = MakeModel()
        notes = ""
        tableName = data.get("tableName")
        datastr = data.get("Field")
        notes = model.ModifyModel("make_model_test.txt",tableName)
        model.makeModel(datastr, notes, tableName)
        os.system("python "+oldFileName)
        os.remove(newFileName)
        return 'OK'
    except Exception as e:
        print(e)
        os.remove(newFileName)
        logger.error(e)