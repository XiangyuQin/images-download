# -*- coding: UTF-8 -*-

import MySQLdb
import common
import config
import MySQLdb.cursors
from Log import Log

class MysqlService(object):
    def __init__(self, log):
        self.log = log
        self.db = MySQLdb.connect("localhost","root", "qinxiangyu", "spider",charset='utf8', cursorclass = MySQLdb.cursors.DictCursor)
    
    def getImages(self):
        cursor = self.db.cursor()
        sql = "select *,COUNT(distinct url) AS disItem from images WHERE ifdown = 0 GROUP BY url ORDER BY id desc limit 100"
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            return results
        except Exception as e:
            self.log.printError("getImages: %s" % (e))
            return []
            
            
    def updateImages(self, images):
        cursor = self.db.cursor()
        try:
            for image in images:
                sql="UPDATE images SET ifdown = '%s' \
                          WHERE id = '%d'" % (image['ifdown'], image['id'])
                cursor.execute(sql)
                self.db.commit()
            return True
        except Exception as e:
            self.log.printError("updateImages: %s" % (e))
            return False
            
    def closeDb(self):
        self.db.close()
    

if __name__ == '__main__':
    service = MysqlService()
    article1={'id':1,"title":"示例文章","url":"www.baiu.com", "image":"/status/image/hello.jpg","date":"2016-02-17","brief":"和咯","type_id":"1","writer":"hello","content":"合理"}
    article2={'id':2,"title":"示例文章","url":"www.baiu.com", "image":"/status/image/hello.jpg","date":"2016-02-17","brief":"和咯","type_id":"1","writer":"hello","content":"合理"}
    articles=[]
    articles.append(article1)
    articles.append(article2)
    image1={"id":1,"url":"www.baidu.com","src":"/status/images/hello.jpg","type":1,"sourceArticles":1,"ifused":1,"ifdown":1}
    image2={"id":2,"url":"www.baidu.com","src":"/status/images/hello.jpg","type":1,"sourceArticles":1,"ifused":2,"ifdown":1}
    images=[]
    images.append(image1)
    images.append(image2)
    print service.getImages()