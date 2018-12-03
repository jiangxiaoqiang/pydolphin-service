import urllib,urllib2
import re,os
import time
class RestTest(object):
     def __init__(self):
         self.__ResPath__ = './'

     def Rest(self,method,url,restName,**param):
         print "aa"
         jsessionStr=r'"jsessionid":"(.*?)"'
         new_jsessionStr = re.compile(jsessionStr)
         if method=='GET':
            data = self.UrlParam(param)
            new_url=url+'?'+data
            result = urllib.urlopen(new_url).read()
            print  restName+'\n'+result
            self.WriteRes(result,restName)
            return ''.join(new_jsessionStr.findall(result))
         if method=='POST':
            data = self.UrlParam(param)
            req = urllib2.Request(url,data)
            response = urllib2.urlopen(req)
            result = response.read()
            print  restName+'\n'+result
            self.WriteRes(result,restName)
            return ''.join(new_jsessionStr.findall(result))

     def UrlParam(self,param):
        return urllib.urlencode(param)

     def WriteRes(self, result, restName):
         res = result.find('success')
         fw_flag = open('%sTestRes.txt' % self.__ResPath__, 'a')
         if res > 0:
             fw_flag.write('%s : pass\n' % restName)
         else:
             fw_flag.write('%s : fail\n' % restName)
         fw_flag.close()
         fw_response = open('%s%s.txt' % (self.__ResPath__, restName), 'w')
         fw_response.write(result)
         fw_response.close()

if __name__ == '__main__':
    Test = RestTest()
    session_id = Test.Rest('GET','https://api.github.com/users/octocat/orgs','login',login_flag=0)