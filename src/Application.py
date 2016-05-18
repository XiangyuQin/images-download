# -*- coding: UTF-8 -*-
import os
import uuid
import urllib2
import cookielib
import time
import datetime
import common
import config
import re
from Log import Log
from MysqlService import MysqlService


class Application(object):
    
    def __init__(self):
        self.now = datetime.datetime.now()
        self.log = Log(self.now)

    def run(self):
        nowStr=common.datetime_toStringYMDHMS(self.now)
        self.log.printInfo("program start,now:%s" %(nowStr))
        images = self.loadImagesFromMysql()
        self.log.printInfo("the number of image is %d,which is going to download:" %(len(images)))
        result = self.downloadImages(images)
        self.log.printInfo("the number of image is %d,which had downloaded:" %(len(images)))
        self.updateImages(result)
        self.log.printInfo("program end")
        
    def loadImagesFromMysql(self):
        service = MysqlService(self.log)
        list = service.getImages()
        return list
        
    def updateImages(self, images = {}):
        service = MysqlService(self.log)
        service.updateImages(images)
    
    def downloadImages(self, images):
        print "downloadImages"
        list=[]
        for image in images:
            if(self.downloadImage(image)):
                dict={}
                dict["ifdown"] = config.down
                dict["id"] = image['id']
                list.append(dict)
        return list
        
    def downloadImage(self, image):
        path, name = self.divideSrc(image['src'])
        if path=="" or name == "":
            return False
        url = image['url']   
        #�����ļ�ʱ��ע������Ҫƥ�䣬��Ҫ�����ͼƬΪjpg����򿪵��ļ������Ʊ�����jpg��ʽ������������ЧͼƬ
        data = self.get_file(url)
        if (data != None):
            self.save_file(path, name, data)
            return True
        else:
            return False
        
        
    '''��ȡ�ļ���׺��'''
    def get_file_extension(self, file):  
        return os.path.splitext(file)[1]  

    '''�����ļ�Ŀ¼�������ظ�Ŀ¼'''
    def mkdir(self, path):
        # ȥ���������ߵĿո�
        path=path.strip()
        # ȥ��β�� \����
        path=path.rstrip("\\")
    
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    '''�Զ�����һ��Ψһ���ַ������̶�����Ϊ36'''
    def unique_str(self):
        return str(uuid.uuid1())

    '''
    ץȡ��ҳ�ļ����ݣ����浽�ڴ�
    
    @url ��ץȡ�ļ� ��path+filename
    '''
    def get_file(self, url):
        try:
            cj=cookielib.LWPCookieJar()
            opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            urllib2.install_opener(opener)
            
            req=urllib2.Request(url)
            operate=opener.open(req)
            data=operate.read()
            return data
        except BaseException, e:
            self.log.printError("error in get_file %s" %(e))
            return None

    '''
    �����ļ�������
    
    @path  ����·��
    @file_name �ļ���
    @data �ļ�����
    '''
    def save_file(self, path, file_name, data):
        if data == None:
            return
    
        self.mkdir(path)
        if(not path.endswith("/")):
            path=path+"/"
        file=open(path+file_name, "wb")
        file.write(data)
        file.flush()
        file.close()
        
    def divideSrc(self, src):
        groups = self.regexGroup(src, config.regexSrc)
        print "len(groups):"+str(len(groups))
        if len(groups)>1:
            name = groups[1]
            path = src.replace(name.strip(), "").strip()
            path = config.path + path
            return path, name
        else:
            return "", ""
        
    def regexGroup(self, content, regex):
        m = re.search(regex, content,re.M|re.I)
        if m!=None:
            return m.groups()
        else:
            return ()
            
            
if __name__ == '__main__':
    application = Application()
    application.run()