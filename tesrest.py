__author__ = 'dkooi'
import re
import time
import requests
import http.client
requests.urllib3.disable_warnings()
import  tesclasses
from requests.auth import HTTPBasicAuth
import datetime
import xml2obj 
import base64
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import logging 
import TESObjects

from functools import lru_cache, cache
url = ''
user = ''
password = ''
auth = ''
req = ''
s = ''
objectdict = {}
objectdict['hits']=0
objectdict['misses']=0
class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

xmlpost_old = """\
<?xml version="1.0" encoding="UTF-8" ?>\
<entry xmlns="http://purl.org/atom/ns#">\
	<object.function>\
		<queryCondition><![CDATA[#queryCondition]]></queryCondition>\
		<selectColumns>#selectColumns</selectColumns>\
        <numRows>0</numRows>\
	</object.function>\
</entry>\
"""
xmlpost = """<?xml version="1.0" encoding="UTF-8" ?><entry xmlns="http://purl.org/atom/ns#"><{object}.{function}><queryCondition><![CDATA[{queryCondition}]]></queryCondition><selectColumns>{selectColumns}</selectColumns><numRows>0</numRows></{object}.{function}></entry>"""
xmlpostsorted = """\
<?xml version="1.0" encoding="UTF-8" ?>\
<entry xmlns="http://purl.org/atom/ns#">
	<object.function>
		<queryCondition>#queryCondition</queryCondition>
		<selectColumns>#selectColumns</selectColumns>
        <orderBy>#orderBy</orderBy>
        <numRows>0</numRows>
	</object.function>
</entry>
"""

xmlupd = """\
<?xml version="1.0" encoding="UTF-8" ?>\
<entry xmlns="http://purl.org/atom/ns#">\
<object.function xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"   xmlns:tes="http://www.tidalsoftware.com/client/tesservlet">\
#obj\
</object.function>\
</entry>
"""
def escape( str ):
    if not  "&amp;" in str:
        str = str.replace("&", "&amp;")
    if not "&lt;" in str:
        str = str.replace("<", "&lt;")
    if not "&gt;" in str: 
        str = str.replace(">", "&gt;")
    if not "&quot;" in str:
        str = str.replace("\"", "&quot;")
    return str

class Py2XML():

    def __init__( self ):

        self.data = "" # where we store the processed XML string

    def parse( self, pythonObj, objName=None ):
        '''
        processes Python data structure into XML string
        needs objName if pythonObj is a List
        '''
        if pythonObj == None:
            return ""

        if isinstance( pythonObj, dict ):
            self.data = self._PyDict2XML( pythonObj )

        elif isinstance( pythonObj, list ):
            # we need name for List object
            self.data = self._PyList2XML( pythonObj, objName )

        else:
            self.data = "<%(n)s>%(o)s</%(n)s>" % { 'n':objName, 'o':str( pythonObj ) }

        return self.data

    def _PyDict2XML( self, pyDictObj, objName=None ):
        '''
        process Python Dict objects
        They can store XML attributes and/or children
        '''
        tagStr = ""     # XML string for this level
        attributes = {} # attribute key/value pairs
        attrStr = ""    # attribute string of this level
        childStr = ""   # XML string of this level's children

        for k, v in pyDictObj.items():

            if isinstance( v, dict ):
                # child tags, with attributes
                childStr += self._PyDict2XML( v, k )

            elif isinstance( v, list ):
                # child tags, list of children
                childStr += self._PyList2XML( v, k )

            else:
                # tag could have many attributes, let's save until later
                attributes.update( { k:v } )

        if objName == None:
            return childStr

        # create XML string for attributes
        for k, v in attributes.items():
            attrStr += " %s=\"%s\"" % ( k, v )

        # let's assemble our tag string
        if childStr == "":
            tagStr += "<%(n)s%(a)s />" % { 'n':objName, 'a':attrStr }
        else:
            tagStr += "<%(n)s%(a)s>%(c)s</%(n)s>" % { 'n':objName, 'a':attrStr, 'c':childStr }

        return tagStr

    def _PyList2XML( self, pyListObj, objName=None ):
        '''
        process Python List objects
        They have no attributes, just children
        Lists only hold Dicts or Strings
        '''
        tagStr = ""    # XML string for this level
        childStr = ""  # XML string of children

        for childObj in pyListObj:

            if isinstance( childObj, dict ):
                # here's some Magic
                # we're assuming that List parent has a plural name of child:
                # eg, persons > person, so cut off last char
                # name-wise, only really works for one level, however
                # in practice, this is probably ok
                childStr += self._PyDict2XML( childObj, objName[:-1] )
            else:
                for string in childObj:
                    childStr += string;

        if objName == None:
            return childStr

        tagStr += "<%(n)s>%(c)s</%(n)s>" % { 'n':objName, 'c':childStr }

        return tagStr

class TESREST:
    def __init__(self, url, user, password):
        self.url = url
        self.user = user
        if type(password) is str:
            self.password = password
        else:
            self.password = base64.b85decode(password).decode('utf-8')
        self.auth = HTTPBasicAuth(self.user, self.password)
        self.s = requests.Session()
        self.req = requests.Request('GET', self.url, auth=self.auth)
        prepped = self.req.prepare()
        self.resp = self.s.send(prepped, verify=False,timeout=15)
        self.jobruncommand = """<?xml version="1.0" encoding="UTF-8"?> 
    <entry xmlns=""http://purl.org/atom/ns#"">
    <id>#id/id>
    <tes:JobRun.#function xmlns:tes="http://www.tidalsoftware.com/client/tesservlet">
        #value
    </tes:JobRun.rerun>
    </entry>
    """
        if not self.resp.ok:
            print(f"Not Connected: {self.resp}")
        else:
            pass
            #print("Connected to CM")

    def connect(self, url, user, password):
        return self.__init__(self, url, user, password)

    def getNodeList(self):
        if self.req is None:
            raise Exception('Not connected to TES')
        self.req = s.Request('GET', self.url + '/Node.getList', auth=self.auth)
        prepped = self.req.prepare()
        self.resp = self.s.send(prepped,verify=False)
        # print self.resp.text
        r2 = re.sub(' xmlns="[^"]+"', '', self.resp.text)
        root = ET.fromstring(r2)
        # feed= root.find('feed')
        el2 = root.findall(".//node")
        nodeList = []
        ET.register_namespace('', 'http://www.tidalsoftware.com/client/tesservlet')
        for entry in root.iter('entry'):
            for node in entry.iter('{http://www.tidalsoftware.com/client/tesservlet}node'):
                nodeList.append(xml2obj.xml2obj(ET.tostring(node)))
        return nodeList
    def getOutputContent(self,jobid):
        if self.req is None:
            raise Exception('Not connected to TES')
        self.req = s.Request('GET', self.url + '/OutputContent.getList', auth=self.auth)
        prepped = self.req.prepare()
        self.resp = self.s.send(prepped,verify=False)
        # print self.resp.text
        r2 = re.sub(' xmlns="[^"]+"', '', self.resp.text)
        root = ET.fromstring(r2)
        # feed= root.find('feed')
        el2 = root.findall(".//node")
        nodeList = []
        ET.register_namespace('', 'http://www.tidalsoftware.com/client/tesservlet')
        for entry in root.iter('entry'):
            for node in entry.iter('{http://www.tidalsoftware.com/client/tesservlet}node'):
                nodeList.append(xml2obj.xml2obj(ET.tostring(node)))
        return nodeList

    async def getTESList(self,objectname, criteria, columns=None, logger=None):
        if self.req is None:
            raise Exception('Not </tes:  + keto TES')
        if columns == None:
            xmlpost = f"""<?xml version="1.0" encoding="UTF-8" ?><entry xmlns="http://purl.org/atom/ns#"><{objectname}.getList><queryCondition><![CDATA[{criteria}]]></queryCondition><numRows>0</numRows><changedOnly><![CDATA[Y]]></changedOnly></{objectname}.getList></entry>"""
        else:
            xmlpost = f"""<?xml version="1.0" encoding="UTF-8" ?><entry xmlns="http://purl.org/atom/ns#"><{objectname}.getList><queryCondition><![CDATA[{criteria}]]></queryCondition><selectColumns>{columns}</selectColumns><numRows>0</numRows><changedOnly><![CDATA[Y]]></changedOnly></{objectname}.getList></entry>"""
        data = {'data': xmlpost}
        self.req = requests.Request('POST',self.url + '/post', data=data, auth=self.auth)
        prepped = self.s.prepare_request(self.req)
        start_time = datetime.datetime.now()
        self.resp = self.s.send(prepped,verify=False)
        elapsed = datetime.datetime.now() - start_time
        mes = "Elapsed time %d " % elapsed.seconds
        root = ET.fromstring(self.resp.text.encode('utf-8'))
        objlist = []
        tesobjlist = []
        ET.register_namespace('', 'http://www.tidalsoftware.com/client/tesservlet')
        for entry in root.iter('{http://www.tidalsoftware.com/client/tesservlet}' + objectname.lower()):
            xml = ET.tostring(entry)
            obji = xml2obj.xml2obj(xml,objectname)
            if len(obji._attrs) > 1:
                obji._attrs['TESObject'] = objectname
                objlist.append(obji)
        if len(tesobjlist) > 0:
            return (tesobjlist, mes + ':' + xmlpost)
        return (objlist, mes + ':' + xmlpost)

    def getTESListSorted(self,objectname, criteria, columns=None, orderBy=None):
        if self.req is None:
            raise Exception('Not </tes:  + keto TES')
        if columns == None:
            xmlpost = f"""<?xml version="1.0" encoding="UTF-8" ?><entry xmlns="http://purl.org/atom/ns#"><{objectname}.getList><queryCondition><![CDATA[{criteria}]]></queryCondition><numRows>0</numRows><orderBy>{orderBy}</orderBy><changedOnly><![CDATA[Y]]></changedOnly></{objectname}.getList></entry>"""
        else:
            xmlpost = f"""<?xml version="1.0" encoding="UTF-8" ?><entry xmlns="http://purl.org/atom/ns#"><{objectname}.getList><queryCondition><![CDATA[{criteria}]]></queryCondition><selectColumns>{columns}</selectColumns><numRows>0</numRows><orderBy>{orderBy}</orderBy><changedOnly><![CDATA[Y]]></changedOnly></{objectname}.getList></entry>"""
        data = {'data': xmlpost}
        self.req = requests.Request('POST',self.url + '/post', data=data, auth=self.auth)
        prepped = self.s.prepare_request(self.req)
        start_time = datetime.datetime.now()
        self.resp = self.s.send(prepped,verify=False)
        elapsed = datetime.datetime.now() - start_time
        mes = "Elapsed time %d " % elapsed.seconds
        root = ET.fromstring(self.resp.text.encode('utf-8'))
        objlist = []
        tesobjlist = []
        ET.register_namespace('', 'http://www.tidalsoftware.com/client/tesservlet')
        for entry in root.iter('{http://www.tidalsoftware.com/client/tesservlet}' + objectname.lower()):
            #            python_object = deserializer.parse(ET.tostring(entry))
            xml = ET.tostring(entry)
            obji = xml2obj.xml2obj(xml,objectname)
            if len(obji._attrs) > 1:
                obji._attrs['TESObject'] = objectname
                objlist.append(obji)
        if len(tesobjlist) > 0:
            return (tesobjlist, mes + ':' + xmlpost)
        return (objlist, mes + ':' + xmlpost)




    def getCalendarForecast(self,calendarid):
        try:
            #calid = self.getCalendarId(calendarname)
            result = self.getTESFunctionResult(objectname= "CalendarYear",function= "getForecast",  criteria= f"<calendarid>{calendarid}</calendarid>")        
            forecastdates = result.split(',')
            return forecastdates
        except Exception as ex:
            print(ex)
            return None

    def getTESFunctionResult(self,objectname,function, criteria, columns=None, logger=None):
        try:
            if self.req is None:
                raise Exception('Not </tes:  + keto TES')
            newxml = xmlupd.replace('object', objectname).replace('function', function).replace('#obj', criteria).replace('#selectColumns', columns if columns != None else '').replace('\n','').replace('\t','')
            data = {'data': newxml}
            self.req = requests.Request('POST',self.url + '/post', data=data, auth=self.auth)
            prepped = self.s.prepare_request(self.req)
            self.resp = self.s.send(prepped,verify=False)
            pattern = "<tes:message>(.*?)</tes:message>"
            substring = re.search(pattern, self.resp.text).group(1)
        except Exception as ex:
            substring =''
        return substring
    #@cache
    def getObjectByName(self,object,name,cached=False):
        id = self.getObjectIdByName(object,name,cached)
        if id !='0':
            return self.getObjectById(object,id,cached)
        return None
    #@cache    
    def getObjectIdByName(self,object,name,cached=False):
        if cached and f"{object}_{name}" in objectdict:
            return objectdict[f"{object}_{name}"]
        r1 = self.getTESList(object, f"lower(name)='{name.lower()}'")
        if len(r1[0])!= 1:
            return '0'
        else:
            objectdict[f"{object}_{name}"] = r1[0][0].id
            return r1[0][0].id
    
    def getObjectById(self,object,id,cached=False):
        if cached and f"{object}_{id}" in objectdict:
            return objectdict[f"{object}_{id}"]
        r1 = self.getTESList(object, f"id='{id}'")
        objectdict['misses'] +=1
        if len(r1[0])!= 1:
            return '0'
        else:
            objectdict[f"{object}_{id}"] = r1[0][0]
            return r1[0][0]

#/, \, ^, –, ?, +, (, ), [, ], {, and } 
    def replaceChars(self,name):
        new_name = ''
        _strs = """\<>(),*?'"""
        count_single_quote= name.count("'") 
        count_double_quote= name.count('"')

        for x in name:
            if x in _strs:
                if x == "'":
                    if count_single_quote % 2 == 0:
                        new_name += '\\' + x
                    else:
                        new_name += x
                elif x == '"':
                    if count_double_quote % 2 == 0:
                        new_name += '\\' + x
                    else:
                        new_name += x
                else:
                    new_name += '\\' + x
            else:
                new_name += x
        #if new_name != name:
        #    print(f'Name changed from {name} to {new_name}')
        return new_name

    def getJobbyName(self,name):
        tname = self.replaceChars(name)
        results = self.getTESList("Job",f"job.name like '{tname}'",None,logging)    
        if len(results[0]) == 1:
            jobid = results[0][0]['id']
            newjob = results[0][0]
        else:
            jobid = None
            newjob = xml2obj.xml2obj(TESObjects.Job,'job')
            newjob['name'] = name
            newjob['parentname'] = ''
        return jobid, newjob
    def getJobClass(self,name):
        tname = self.replaceChars(name)
        results = self.getTESList("JobClass",f"LOWER(name) like '{tname.lower()}'",None,logging)    
        if len(results[0]) == 1:
            jobclassid = results[0][0]
        else:
            jobclassid = '0'
        return jobclassid

    def getJobClassId(self,name):
        tname = self.replaceChars(name)
        results = self.getTESList("JobClass",f"LOWER(name) like '{tname.lower()}'",None,logging)    
        if len(results[0]) == 1:
            jobclassid = results[0][0]['id']
        else:
            jobclassid = '0'
        return jobclassid
    
    def getTag(self,name):
        tname = self.replaceChars(name)
        results = self.getTESList("Tag",f"LOWER(name) like '{tname.lower()}'",None,logging)    
        if len(results[0]) == 1:
            tagid = results[0][0]['id']
        else:
            tagid = '0'
        return tagid
        
    def getAllJobsbyName(self,name):
        tname=  name.replace('(','\\(').replace(')','\\)').replace(',','\\,').replace('=','\\=')
        results = self.getTESList("Job",f"job.name = '{tname}'",None,logging)    
        return results[0]
    
    def getOwner(self,name):
        n = name.split('\\')[-1]
        retvalue,_ = self.getTESList("Owners",f"name='{n}'")
        if retvalue !=None:
            return retvalue[0]['id']
        else:
            return self.getRuntimeUserId(name)
    def getOwnerId(self,name):
        n = name.split('\\')[-1]
        retvalue,_ = self.getTESList("Owners",f"name='{n}'")
        if len(retvalue) ==1:
            return retvalue[0]['id']
        else:
            return self.getUserId(n)
            
        
    def getVariable(self,name):
        retvalue,_ = self.getTESList("Variable",f"name='{name}'")
        if len(retvalue) !=0:
            return retvalue[0]
        else:
            return '0'
    def getEvent(self,name,type='Job'):
        retvalue,_ = self.getTESList(f"Events{type}",f"name='{name}'")
        if len(retvalue) !=0:
            return retvalue[0]
        else:
            return '0'
    def getEventId(self,name):
        retvalue,_ = self.getTESList("Events",f"name='{name}'")
        if len(retvalue) !=0:
            return retvalue[0]['id']
        else:
            return '0'
    def getEventsLike(self,name):
        retvalue,_ = self.getTESList("Events",f"name like '{name}'")
        return retvalue

    def del_getRuntimeUser(self,rtu):
        if rtu.find('\\')> -1:
            domain , name = rtu.split('\\')
            to_r = self.getTESList("Users", f"lower(name)='{name.lower()}' and lower(domain)='{domain.lower()}'")  
        else:
            to_r = self.getTESList("Users", f"lower(name)='{rtu.lower()}' and (domain is null or domain='')")
        if len(to_r[0]) == 1:
            return  to_r[0][0] 
        else:
            return '0'
    def getUserId(self,u):
        if u.find('\\')> -1:
            domain , name = u.split('\\')
        else:
            name = u
        to_r = self.getTESList("Users", f"name='{name}'")  
        if len(to_r[0]) == 1:
            return  to_r[0][0]['id'] 
        else:
            return '0'

    def getRuntimeUser(self,rtu):
        if rtu.find('\\')> -1:
            domain , name = rtu.split('\\')
            to_r = self.getTESList("Users", f"lower(name)='{name.lower()}' and lower(domain)='{domain.lower()}'")  
        else:
            to_r = self.getTESList("Users", f"lower(name)='{rtu.lower()}' and (domain is null or domain='')")
        if len(to_r[0]) == 1:
            return  to_r[0][0] 
        else:
            return '0'
    def getRuntimeUserId(self,rtu):
        res = self.getRuntimeUser(rtu)
        if res != '0':
            return res['id']
        else:
            return res

    def getJob(self,name,parent, cached=True):
        if cached:
            if f"job_{name}_{parent}" in objectdict:
                objectdict['hits'] +=1
                return objectdict[f"job_{name}_{parent}"]['id'],objectdict[f"job_{name}_{parent}"]
            else:
                objectdict['misses'] +=1
        tparent = parent.replace('\\','\\\\') 
        tname=  name.replace('(','\\(').replace(')','\\)').replace(',','\\,').replace('=','\\=')            
        tparent= tparent.replace('(','\(').replace(')','\)').replace(',','\,').replace('=','\\=')
            #if cfg.API_VERSION=='6.3':
            #    tparent = '\\' + tparent.strip('\\') 
        if tname == None or tname == '':
            results = self.getTESList("Job",f"LOWER(job.fullpath) = '{tparent.lower()}'",None,logging)
        else:
            if tparent == '':
                results = self.getTESList("Job",f"job.parentname is Null and LOWER(job.name) like'{tname.lower()}'",None,logging)
            else:
                if '*' in tparent and '*' in tname:
                    results = self.getTESList("Job",f"LOWER(job.parentname) like '{tparent.lower()}' and LOWER(job.name) like '{tname.lower()}'",None,logging)
                else:
                    if '*' in tparent:
                        results = self.getTESList("Job",f"LOWER(job.parentname) like '{tparent.lower()}' and LOWER(job.name) = '{tname.lower()}'",None,logging)
                    else:
                        if '*' in tname:
                            results = self.getTESList("Job",f"LOWER(job.parentname) = '{tparent.lower()}' and LOWER(job.name) like '{tname.lower()}'",None,logging)
                        else:
                            results = self.getTESList("Job",f"LOWER(job.parentname) = '{tparent.lower()}' and LOWER(job.name) = '{tname.lower()}'",None,logging)

        if len(results[0]) == 1:
            jobid = results[0][0]['id']
            newjob = results[0][0]
            if newjob['typename'] =='FTPJOB':
                id = newjob['id']
                results = self.getTESList("FTPJob",f"job.id = '{id}'",None,logging)
                newjob = results[0][0]
                #newjob = xml2obj.xml2obj(TESObjects.FTPJob,'FTPJob')

            objectdict[f"job_{name}_{parent}"] = results[0][0]
        else:
            jobid = None
            #logging.info('Not found', name, parent)
            newjob = xml2obj.xml2obj(TESObjects.Job,'job')
            if newjob['typename'] =='FTPJOB':
                newjob = xml2obj.xml2obj(TESObjects.FTPJob,'ftpjob')
            newjob['name'] = name
            newjob['parentname'] = parent
        return jobid, newjob

    def getCalendarId(self,name):
        if name =='':
            return '0'
        if name != name.replace('(','\\(').replace(')','\\)').replace(',','\\,').replace ('&','&amp;'):
            pass
        name = name.replace('(','\\(').replace(')','\\)').replace(',','\\,').replace ('&','&amp;')
        r1 = self.getTESList("Calendar", f"name='{name.strip()}'")
        if len(r1[0]) == 1:
            return  r1[0][0]['id']            
        else:
            r1 = self.getTESList("Calendar", f"lower(name)='{name.strip().lower()}'")
            if len(r1[0]) == 1:
                return  r1[0][0]['id']
            else:
                logging.info(f'Calendar not found 2 {name}')
                return '0'
    def getResourceId(self,name):
        r1 = self.getTESList("Resource", f"name='{name}'")
        if len(r1[0])== 0:
            return '0'
        else:
            return r1[0][0].id

    def getActionId(self,name):
        r1 = self.getTESList("Actions", f"name='{name}'")
        if len(r1[0])== 0:
            return '0'
        else:
            return r1[0][0].id
    def getAction(self,name):
        r1 = self.getTESList("Actions", f"name='{name}'")
        if len(r1[0])== 0:
            return '0'
        else:
            return r1[0][0]

    def getAgentId(self,name):
        r1 = self.getTESList("Node", f"name='{name}'")
        if len(r1[0])== 0:
            return '0'
        else:
            return r1[0][0].id
    
    def getAgentListId(self,name):
        r1 = self.getTESList("AgentList", f"name='{name}'")
        if len(r1[0])== 0:
            return '0'
        else:
            return r1[0][0].id


    def TESLogout(self):
        newxml = xmlpost.replace('object', 'Users').replace('function', 'logoutSession').replace('#queryCondition', '')
        data = {'data': newxml}
        self.req = requests.Request('POST', self.url + '/post', data=data, auth=self.auth)
        prepped = self.req.prepare()
        self.resp = self.s.send(prepped,verify=False)

    def __del__(self):

        #print('Objectdict hits',objectdict['hits'])
        #print('Objectdict misses',objectdict['misses'])
        if False:
            newxml = xmlpost.replace('object', 'Users').replace('function', 'logoutSession').replace('#queryCondition', '')
            data = {'data': newxml}
            self.req = requests.Request('POST', self.url + '/post', data=data, auth=self.auth)
            prepped = self.s.prepare_request(self.req)
            self.resp = self.s.send(prepped,verify=False)
    def compare_jobs(self,job_data,save_job_data):
        diff = False
        try:
            for attr in job_data._attrs:
                val1 =  str(job_data[attr]).strip() if job_data[attr]!= None else ''
                val2 =  str(save_job_data[attr]).strip() if save_job_data[attr]!= None else ''
                if (attr =='timewindowfromtimeasstring' and val1[8:]=='240000' and val2[8:]=='000000') or \
                   (attr == 'agentlistid' and (str(val1) or '') =='0' and (val2 or '') =='') or \
                   (attr == 'variables' and val1 =='<variables></variables>' and val2 =='') or \
                    (attr == 'xmlns'):
                    pass
                elif val1 != val2:
                    diff=True
                    print("Different",attr, val1,val2)
                    break
        except Exception as ex:
            logging.error(ex)        
        return diff, attr




    def dict2Xml(self, objectname, obj):
        if  'variables' in obj:
            obj['variables'] = obj['variables'].replace("<name>", "<variables:name>").replace("</name>", "</variables:name>").replace("<row>", "<variables:row>").replace("</row>", "</variables:row>").replace("<value>", "<variables:value>").replace("</value>", "</variables:value>").replace("<id>", "<variables:id>").replace("</id>", "</variables:id>")
        #xml = "<" + objectname + ' xmlns:tes="http://www.tidalsoftware.com/client/tesservlet" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
        xml = "<" + objectname + ' xmlns:tes="http://www.tidalsoftware.com/client/tesservlet" >'
        try:
            for key, val in obj._attrs.items():
                if type(val) == str or val == None:
                    if key in ['extendedinfo','parameters','variables']:
                        if val != None:                    
                            xml += "<tes:" + key + ">" + escape(val) + "</tes:" + key + ">" 
                        else:
                            # tes:null="Y"                                
                            xml += "<tes:" + key + " tes:null=\"Y\" />"  

                    else:
                            if val != None:                    
                                xml += "<tes:" + key + ">" + escape(val) + "</tes:" + key + ">"
                            else:
                                # tes:null="Y"                                
                                xml += "<tes:" + key + " tes:null=\"Y\" />"  
                else:
                    #xml += "<tes:" + key + "/>"        
                    pass
            xml += "</" + objectname + ">"
        except:
            for key, val in obj.items():
                if type(val) == str:
                    if key in ['extendedinfo','parameters','variables']:
                        if val != None:                    
                            xml += "<tes:" + key + ">" + escape(val) + "</tes:" + key + ">" 
                    else:
                            xml += "<tes:" + key + ">" + escape(val) + "</tes:" + key + ">" 
                else:
                    xml += "<tes:" + key + "/>"
                    pass
            xml += "</" + objectname + ">"
        return xml

    def fixVariables(self, job):
        if not 'variables' in job:
            return
        if job.variables != '':
            job['variables'] = job['variables'].replace("<name>", "<variables:name>").replace("</name>", "</variables:name>").replace("<row>", "<variables:row>").replace("</row>", "</variables:row>").replace("<value>", "<variables:value>").replace("</value>", "</variables:value>").replace("<id>", "<variables:id>").replace("</id>", "</variables:id>");



    def updTESObj(self,  function,objname, obj, logger):
        """
        :rtype: Result
        """
        if self.req is None:
            raise Exception('Not connected to TES')
        if 'typename' in obj._attrs:
            if obj._attrs['typename'].lower() =='jobgroup':
                obj.TESObject = 'JobGroup'
                obj._attrs.pop('command', None)
            if obj._attrs['typename'].lower() =='job':
                obj.TESObject = 'Job'
            if obj._attrs['typename'].lower() =='jobrun':
                obj.TESObject = 'JobRun'
            if obj._attrs['typename'].lower() =='servicejob':
                obj.TESObject = 'ServiceJob'
            if obj._attrs['typename'].lower() =='ftpjob':
                obj.TESObject = 'FTPJob'
            if obj._attrs['typename'].lower() =='osjob':
                obj.TESObject = 'OSJob'
        else:
            if obj.TESObject.lower() =='job':
                if obj.type == '8':
                    obj.TESObject = 'ServiceJob'
                if obj.type == '6':
                    obj.TESObject = 'FTPJob'
                if obj.type == '1':
                    obj.TESObject = 'JobGroup'
                if obj.type == '2':
                    obj.TESObject = 'Job'
        if isinstance(obj,str):
            newxml = xmlupd.replace('object', objname).replace('function', function).replace('#obj',str(obj))
        else:
            newxml = xmlupd.replace('object', objname).replace('function', function).replace('#obj',self.dict2Xml(objname,obj))
        data = {'data': newxml.replace('\n','').replace('\t','')}
        if logger != None:
            logger.debug(data['data'])
        headers = {'Content-Type': 'application/atom xml'}
        self.req = requests.Request('POST', self.url + '/post', data=data, auth=self.auth)
        prepped = self.s.prepare_request(self.req)
        self.resp = self.s.send(prepped,verify=False)
        # r2 = re.sub(' xmlns="[^"]+"', '', self.resp.text)
        # root = ET.fromstring(r2)
        root = ET.fromstring(self.resp.text)
        if logger != None:
            logger.debug(self.resp.text)
        result = tesclasses.Result
        result.message = f" {self.resp.status_code} {self.resp.reason}"
        ET.register_namespace('', 'http://www.tidalsoftware.com/client/tesservlet')
        for entry in root.iter('{http://www.tidalsoftware.com/client/tesservlet}operation'):
            result.operation = entry.text
        for entry in root.iter('{http://www.tidalsoftware.com/client/tesservlet}ok'):
            result.ok = entry.text
        for entry in root.iter('{http://www.tidalsoftware.com/client/tesservlet}message'):
            result.message = entry.text
        for entry in root.iter('{http://www.tidalsoftware.com/client/tesservlet}objectid'):
            result.objectid = entry.text
        for entry in root.iter('{http://www.tidalsoftware.com/client/tesservlet}objectname'):
            result.objectname = entry.text
        return result

    def createTESObjAction(self,  function, objname,content):
        if isinstance(content,tesclasses.TESObject):
            newxml = xmlupd.replace('object', objname).replace('function', function).replace('#obj',str(content))
        else:
            newxml = xmlupd.replace('object', objname).replace('function', function).replace('#obj',content)
        return newxml

    def applyTESObjAction(self,content,logger):
        if self.req is None:
            raise Exception('Not connected to TES')
        data = {'data': content.rstrip('\n')}
        headers = {'Content-Type': 'application/atom xml'}
        self.req = requests.Request('POST', self.url + '/post', data=data, auth=self.auth)
        prepped = self.s.prepare_request(self.req)
        self.resp = self.s.send(prepped,verify=False)
        result = tesclasses.Result()
        root = ET.fromstring(self.resp.text)
        if logger != None:
            logger.debug(self.resp.text)
        result.message = f" {self.resp.status_code} {self.resp.reason}"
        ET.register_namespace('', 'http://www.tidalsoftware.com/client/tesservlet')
        for entry in root.iter('{http://www.tidalsoftware.com/client/tesservlet}operation'):
            result.operation += entry.text
        for entry in root.iter('{http://www.tidalsoftware.com/client/tesservlet}ok'):
            result.ok += entry.text
        for entry in root.iter('{http://www.tidalsoftware.com/client/tesservlet}message'):
            result.message += ' ' + entry.text
        for entry in root.iter('{http://www.tidalsoftware.com/client/tesservlet}objectid'):
            result.objectid = entry.text
        for entry in root.iter('{http://www.tidalsoftware.com/client/tesservlet}objectname'):
            result.objectname = entry.text
        for entry in root.iter('{http://www.tidalsoftware.com/client/tesservlet}source'):
            result.source = entry.text

        return result


    def updTESObjAction(self,  function, objname,content,logger):
        """
        :rtype: Result
        """
        if self.req is None:
            raise Exception('Not connected to TES')
        if isinstance(content,tesclasses.TESObject):
            #serializer = Py2XML()
            newxml = xmlupd.replace('object', objname).replace('function', function).replace('#obj',str(content))
        else:
            newxml = xmlupd.replace('object', objname).replace('function', function).replace('#obj',content)
        #data = {'data': newxml.replace('\n','').replace('\t','')}
        data = {'data': newxml.rstrip('\n')}
        if logger != None:
            logger.debug(newxml)
        #else:
        #    print(newxml)
        headers = {'Content-Type': 'application/atom xml'}
        self.req = requests.Request('POST', self.url + '/post', data=data, auth=self.auth)
        prepped = self.s.prepare_request(self.req)
        self.resp = self.s.send(prepped,verify=False)
        # r2 = re.sub(' xmlns="[^"]+"', '', self.resp.text)
        # root = ET.fromstring(r2)
        result = tesclasses.Result()
        #result.message = s
        root = ET.fromstring(self.resp.text)
        if logger != None:
            logger.debug(self.resp.text)
        result.message = f" {self.resp.status_code} {self.resp.reason}"
        ET.register_namespace('', 'http://www.tidalsoftware.com/client/tesservlet')
        for entry in root.iter('{http://www.tidalsoftware.com/client/tesservlet}operation'):
            result.operation += entry.text
        for entry in root.iter('{http://www.tidalsoftware.com/client/tesservlet}ok'):
            result.ok += entry.text
        for entry in root.iter('{http://www.tidalsoftware.com/client/tesservlet}message'):
            result.message += ' ' + entry.text
        for entry in root.iter('{http://www.tidalsoftware.com/client/tesservlet}objectid'):
            result.objectid = entry.text
        for entry in root.iter('{http://www.tidalsoftware.com/client/tesservlet}objectname'):
            result.objectname = entry.text
        for entry in root.iter('{http://www.tidalsoftware.com/client/tesservlet}source'):
            result.source = entry.text
        if result.objectid == '0':
            try:
                #print("exception, Update failed: " + result.message.split('\n')[1])
                result.message = result.message.split('\n')[1]
            except:
                pass
                #print(result.message)
        else:
            if function.lower()=='create':
                object_id = '0'
                loop_cnt=0
                while object_id =='0' and loop_cnt < 10:
                    time.sleep(0.1)
                    if objname != result.objectname:
                        object_id = self.getObjectById(objname,result.objectid,False)
                    else:
                        object_id = self.getObjectById(result.objectname,result.objectid,False)
                    loop_cnt +=1
                    if  loop_cnt % 10 == 0 : 
                        print(f"Create loop {objname} {result.objectid}, tried to find times: {loop_cnt}",end='\r')
                if object_id =='0' and loop_cnt % 10 == 0:
                    print(f"Created but not found after 10 tries {objname} {result.objectid}")
                else:
                    pass
                    #print(f"Create {result.objectname} {result.objectid}, found after {loop_cnt} times ")
            if function.lower()=='delete':
                object_id = '0'
                loop_cnt=0
                while object_id !='0' and loop_cnt < 100:
                    time.sleep(0.1)
                    if objname != result.objectname:
                        object_id = self.getObjectById(objname,result.objectid,False)
                    else:
                        object_id = self.getObjectById(result.objectname,result.objectid,False)
                    loop_cnt +=1
                    if  loop_cnt % 100 == 0 : print(f"Delete loop {result.objectname} {result.objectid}, tried to find times: {loop_cnt}")
                if object_id !='0' and loop_cnt % 10 == 0:
                    print(f"Deleted but still found after 100 tries {result.objectname} {result.objectid}")
                else:
                    pass
                    #print(f"Create {result.objectname} {result.objectid}, found after {loop_cnt} times ")

 
        return result


    def JobRunCommand(self, function, obj):
        """
        :rtype: Result
        """
        if self.req is None:
            raise Exception('Not connected to TES')
        if isinstance(obj,tesclasses.TESObject):
            serializer = Py2XML()
            newxml = xmlupd.replace('object', obj.TESObject).replace('function', function).replace('#obj',str(obj))
        else:
            newxml = xmlupd.replace('object', obj.TESObject).replace('function', function).replace('#obj',self.dict2Xml(obj.TESObject,obj))
        data = {'data': newxml}
        headers = {'Content-Type': 'application/atom xml'}
        self.req = requests.Request('POST', self.url + '/post', data=data, auth=self.auth)
        prepped = self.s.prepare_request(self.req)
        self.resp = self.s.send(prepped,verify=False)
        # r2 = re.sub(' xmlns="[^"]+"', '', self.resp.text)
        # root = ET.fromstring(r2)
        root = ET.fromstring(self.resp.text)
        result = tesclasses.Result()
        ET.register_namespace('', 'http://www.tidalsoftware.com/client/tesservlet')
        for entry in root.iter('{http://www.tidalsoftware.com/client/tesservlet}operation'):
            result.operation = entry.text
        for entry in root.iter('{http://www.tidalsoftware.com/client/tesservlet}ok'):
            result.ok = entry.text
        for entry in root.iter('{http://www.tidalsoftware.com/client/tesservlet}message'):
            result.message = entry.text
        for entry in root.iter('{http://www.tidalsoftware.com/client/tesservlet}objectid'):
            result.objectid = entry.text
        for entry in root.iter('{http://www.tidalsoftware.com/client/tesservlet}objectname'):
            result.objectname = entry.text

        return result


class Py2XML():

    def __init__( self ):

        self.data = "" # where we store the processed XML string

    def parse( self, pythonObj, objName=None ):
        '''
        processes Python data structure into XML string
        needs objName if pythonObj is a List
        '''
        if pythonObj == None:
            return ""

        if isinstance( pythonObj, dict ):
            self.data = self._PyDict2XML( pythonObj )

        elif isinstance( pythonObj, list ):
            # we need name for List object
            self.data = self._PyList2XML( pythonObj, objName )

        else:
            self.data = "<%(n)s>%(o)s</%(n)s>" % { 'n':objName, 'o':str( pythonObj ) }

        return self.data

    def _PyDict2XML( self, pyDictObj, objName=None ):
        '''
        process Python Dict objects
        They can store XML attributes and/or children
        '''
        tagStr = ""     # XML string for this level
        attributes = {} # attribute key/value pairs
        attrStr = ""    # attribute string of this level
        childStr = ""   # XML string of this level's children

        for k, v in pyDictObj.items():

            if isinstance( v, dict ):
                # child tags, with attributes
                childStr += self._PyDict2XML( v, k )

            elif isinstance( v, list ):
                # child tags, list of children
                childStr += self._PyList2XML( v, k )

            else:
                # tag could have many attributes, let's save until later
                attributes.update( { k:v } )

        if objName == None:
            return childStr

        # create XML string for attributes
        for k, v in attributes.items():
            attrStr += " %s=\"%s\"" % ( k, v )

        # let's assemble our tag string
        if childStr == "":
            tagStr += "<%(n)s%(a)s />" % { 'n':objName, 'a':attrStr }
        else:
            tagStr += "<%(n)s%(a)s>%(c)s</%(n)s>" % { 'n':objName, 'a':attrStr, 'c':childStr }

        return tagStr

    def _PyList2XML( self, pyListObj, objName=None ):
        '''
        process Python List objects
        They have no attributes, just children
        Lists only hold Dicts or Strings
        '''
        tagStr = ""    # XML string for this level
        childStr = ""  # XML string of children

        for childObj in pyListObj:

            if isinstance( childObj, dict ):
                # here's some Magic
                # we're assuming that List parent has a plural name of child:
                # eg, persons > person, so cut off last char
                # name-wise, only really works for one level, however
                # in practice, this is probably ok
                childStr += self._PyDict2XML( childObj, objName[:-1] )
            else:
                for string in childObj:
                    childStr += string;

        if objName == None:
            return childStr

        tagStr += "<%(n)s>%(c)s</%(n)s>" % { 'n':objName, 'c':childStr }

        return tagStr

        
