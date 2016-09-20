import MySQLdb
import schedule, time
import datetime
from kits import getdbinfo
from pymongo import MongoClient
import copy
import numpy as np



def getDBconnection(dbinfor,dbname):
    dbconnection = MySQLdb.connect(user = dbinfor['usr'],
                                  passwd = dbinfor['pwd'],
                                  host = dbinfor['host'],
                                  port = dbinfor['port'],
                                  db = dbname)
    return dbconnection

def getMysqlCon(dbhost,dbname):
    DBinfo = getdbinfo(dbhost)
    DBname = dbname

    try:
        DBconnection = getDBconnection(DBinfo,DBname)
    except Exception as e:
        time.sleep(20)
        return getRemoteCon()

    dbCur = DBconnection.cursor()

    return [DBconnection,dbCur]

def readAss():
    assCon,assCur = getMysqlCon("ASS_GTBU","glocalme_ass")
    typeDict = dict()
    query = """
    SELECT t1.imei,t1.usercode,t1.logindatetime,
    CASE WHEN t2.imsi IS NULL THEN 'F' ELSE 'L' END AS flag
    FROM
    t_usmguserloginonline AS t1
    LEFT JOIN glocalme_css.t_css_vsim_binding AS t2
    ON t1.usercode = t2.user_code
    """
    assCur.execute(query)
    deResult = assCur.fetchall()
    for row in deResult:
        imei = str(row[0])
        typeDict[imei]=[row[1],row[2],row[3]]

    assCon.close()
    return typeDict

def queryandinser():
    remoteCon,remoteCur = getMysqlCon("REMOTE","login_history")
    query="""
    SELECT fValue FROM t_loginhistory_dic WHERE ftype = 'partner'
    """
    remoteCur.execute(query)
    result = remoteCur.fetchall()
    parentlist = list()
    for row in result:
        parentlist.append(row[0])

    for parent in parentlist:
        print parent
        
if __name__=="__main__":
    queryandinsert()

