# -*- coding: utf-8 -*-
# Author : hwijinkim , https://github.com/imbornagainer

# openTSDB의 metrics를  복사하기 위한 class 
# last modified by 20171024

import time
import datetime
import os
import sys
import requests
import json
import argparse
import calendar
import urllib2
from operator import itemgetter, attrgetter
import ast

# OpenTSDB 클래스
# EE db 는 15분 단위의 데이터를 저장하고 있음
# OpenTSDB read, and write
class u_ee_tsdb :

    __cin_stime = None #시작시간
    __cin_etime = None #종료시간
    __cin_url = None
    __cin_recent = None
    __cin_datelist = []
    __cin_metric_name = None

    # 시간은 string type 예) 20160701
    def __init__(self, __url, __st = None, __et = None, __r = None) :
       self._url(__url)
       if __st != None and __et != None and __r != None : exit (" < Input Error > no time info")
       elif __st != None and __et != None : self._set_time_period(__st, __et)
       elif __st != None : self._set_time_period(__st)
       elif __r != None : self.__cin_recent = True
       elif self.__cin_recent != True : self.__cin_datelist = self.makeDateList()

    def _url(self, __url):
        self.__cin_url = __url
        if __url == None :
            # default for test
            self.__cin_url = None

    def _set_time_period(self, __st, __et = None) : 
    # TSDB는 기본적으로 시작/종료 시간필요
    # 최소한 시작 시간 필

        if __et == None :
            _lst = len(__st)
            if _lst < 8 : exit ("... too short data length")
            if _lst < 10 : __st = __st[:8] + '00'
            # 여기까지 진행한 날짜는 2017072912 이런식이라고 가정함.
            self.__cin_stime = __st
            self.__cin_etime = __et
            return

        _lst = len(__st)
        _let = len(__et)

        if _lst < 8 or _let < 8 : exit ("... too short data length")
        if _lst < 10 : __st = __st[:8] + '00'
        if _let < 10 : __et = __et[:8] + '00'
        if __st[:8] > __et[:8] : exit ("... Check start, end date")

        self.__cin_stime = __st
        self.__cin_etime = __et

    def set_metric(self,__m) : #TSDB는 metric 이름을 기준으로 읽고/저장
        self.__cin_metric_name = __m

    def changeTimeForOnePointReading(self, _start):
        _st = self.__cin_stime
        assert(self.__cin_etime == None)
        #print ("change self.__cin_etime = self.__cin_stime+ 1 hour")
        # 날짜는 2017072912 이런식이라고 가정함.
        # datetime.date object
        _tmp_obj = datetime.datetime.strptime(_st[:-2],"%Y%m%d").date()
        _tt = _st[-2:] + '00' + '00'
        _time_obj = datetime.datetime.strptime(_tt, "%H%M%S").time()
        _tmp_obj = datetime.datetime.combine(_tmp_obj, _time_obj)
        _delta_obj = datetime.timedelta(hours = 1)
        # datetime.datetime object
        _tmp_obj = _tmp_obj + _delta_obj
        _tmp = _tmp_obj.strftime('%Y%m%d%H')
        self.__cin_etime = _tmp 
        print _tmp
        assert(self.__cin_stime < self.__cin_etime )
        return _tmp

    ''' 
    함수 : readTSDB
    특정 시간의 TSDB값 반환
    parameter1 (in_st) : 시작 시각
    parameter2 (in_et) : 종료 시각
    parameter3 (mid) : 미터기 아이디
    반환 (packetlist_filter) : database 값 리스트(list) 
    '''

    def read_otsdb(self, __in_st, __in_et, __mid):
        packetlist = []  # split :
        packetlist_filter = []  # integer

        # YYYY/MM/DD-HH:00:00
        start = "%s/%s/%s-%s:00:00" % (__in_st[0:4], __in_st[4:6], __in_st[6:8], __in_st[8:10])
        end = "%s/%s/%s-%s:00:00" % (__in_et[0:4], __in_et[4:6], __in_et[6:8], __in_et[8:10])
        tsdb_url = t_url + start + "&end=" + end + "&m=avg:test_daily_led" + "{MDS_ID=" + str(mid) + "}"

        tsdbdata = urllib2.urlopen(url_tsdb)
        read_query = tsdbdata.read()

        print read_query
        exit(-1)
        # 이부분은 사용하지 않음, ast 함수 사용

        packets = dataParser(read_query)
        packet = packets.split(',')

        for k in range(len(packet)):
            packetlist.append(packet[k].split(":"))
            tmp = packetlist[k][0]
            packetlist_filter.append([int(tmp[1:len(tmp) - 1]), float(packetlist[k][1])])

        #mid 추가
        for k in range(len(packetlist_filter)):
            packetlist_filter[k].append(mid)

        return packetlist_filter

    '''
    ## 함수 : calDate
    특정 시간 사이에 날짜들을 연월일시간(YYMMDDhh)을 반환
    open TSDB는 이런형식으로 날짜입력이 된다
    parameter1 (sttime) : 시작 시각
    parameter2 (ettime) : 종료 시각
    반환 (re_datelist) : 날짜 리스트
    '''
    
    def makeDateList(self):
        w_sttime = self.__cin_stime #start unixtime
        w_ettime = self.__cin_etime #end unixtime
        #make it to 23 hour for the last day, 2016110223
        #if w_ettime[-2:] != '23' : w_ettime = w_ettime[:-2] + '23'

        tmp_w_sttime = w_sttime[0:8]
        first_loop = 0
        re_datelist = []

        print self.__cin_url, self.__cin_stime, self.__cin_etime

        while 1:
            #time.sleep(0.01)
            #print ("   ... Processing Date List ... ")

            if first_loop > 0: # 첫 루프가 아니면, 마지막 루프 (종료 또는 다음날로 진행)
                if w_ettime > self.__cin_etime:
                    # 마지막 이면 : 최초 입력 날짜/시간 보다 종료 시간이 늦으면 종료
                    break
                else:
                    w_sttime = self.nextDate(w_sttime, 'd') # 다음날짜 받아옴
                    tmp_w_sttime = w_sttime[0:8]  # ymd 형식

            w_ettime = tmp_w_sttime + '23' #마지막 23시 표시

            if w_ettime == self.__cin_etime: # 마지막 시간 부분 :
                first_loop = 1 # 다음부터는 첫 루프로 진행
                re_datelist.append([w_sttime, w_ettime])
                break

            else:  # start time != end time, 아직 앞부분
                # 동일한 year 처리
                if dateInt(self.__cin_etime, 'y') == dateInt(w_sttime, 'y'):
                    if dateInt(self.__cin_etime, 'm') > dateInt(w_sttime, 'm'):  
                        # different month
                        # check the last day of start month
                        w_st_calr=calendar.monthrange(int(w_sttime[0:4]),dateInt(w_sttime,'m'))
                        if dateInt(w_sttime, 'd') == w_st_calr[1]:  
                            # current day == the last day of stday
                            # next month
                            re_datelist.append([w_sttime, tmp_w_sttime + '23'])
                            w_sttime = self.nextDate(w_sttime, 'm')
                            first_loop = 1
                            continue
                else: # 시작과 종료가 다른 year
                    tmp_w_sttime = w_sttime[0:4]  # year
                    w_st_calr = calendar.monthrange(int(w_sttime[0:4]), dateInt(w_sttime, 'm'))
                    if dateInt(w_sttime, 'd') == w_st_calr[1]:  
                        # current day == the last day of stday
                        re_datelist.append([w_sttime, w_ettime])
                        if dateInt(w_sttime, 'm') == 12:  # 12 month
                            # next year
                            w_sttime = self.nextDate(w_sttime, 'y')
                            tmp_w_sttime = w_sttime[0:8]
                            first_loop = 1
                            continue
                        else:
                            # next month
                            w_sttime = self.nextDate(w_sttime, 'm')
                            tmp_w_sttime = w_sttime[0:8]
                            first_loop = 1
                            continue
                first_loop = 1
            re_datelist.append([w_sttime, w_ettime])
            # [['2016110100', '2016110123'], ['2016110200', '2016110223'],
        return re_datelist

    '''
    ## 함수 : nextDate
    다음 "연, 월, 일"을 계산, 2016년 12월 30일 이후 31일인지, 아니면 1월1일 인지
    parameter1 (in_time) : 문자형 date 값
    parameter2 (in_mdh) : 연, 월, 일, 시간의 분류 (y, m, d, h)
    반환 (re_mdh) : 계산 된 다음 날
    '''
    def nextDate(self, in_time, in_mdh):
        # next year
        if in_mdh == 'y':
            int_year = dateInt(in_time, 'y')
            next_year = int_year + 1
            re_mdh = str(next_year) + '010000'  # next year/01/01/00

        # next month
        if in_mdh == 'm':
            int_month = dateInt(in_time, 'm')
            next_month = twodigitZero(int_month + 1)
            re_mdh = in_time[0:4] + next_month + '00' + in_time[8:10]  # next month/01/01

        # next day
        elif in_mdh == 'd':
            int_day = dateInt(in_time, 'd')
            next_day = twodigitZero(int_day + 1)
            re_mdh = in_time[0:6] + next_day + in_time[8:10]

        return re_mdh

    '''
    ## 함수 : get_tsdb_value
    데이터베이스에 데이터가 있는지 여부를 확인하고
    데이터가 있으면 측정 수치 수집
    주의 : 메트릭만으로 판단 (tag 까지는 확인 안함, 추후 tag 검색 추가 필요)
    반환 (empty_flag) : 비어있을 경우 1 / 비어있지 않을 경우 0
    '''
    def get_tsdb_value(self, _tag = None):
        _st = self.__cin_stime
        _et = self.__cin_etime
        _m  = self.__cin_metric_name

        # 형식 YYYY/MM/DD-HH:00:00
        starttime = "%s/%s/%s-%s:00:00" % (_st[0:4], _st[4:6], _st[6:8], _st[8:10])
        endtime   = "%s/%s/%s-%s:00:00" % (_et[0:4], _et[4:6], _et[6:8], _et[8:10])

        # 참고 : "{"는 URL창에 %7B 로 표현됨
        url_tsdb = self.__cin_url + "start=" + starttime + "&end=" + endtime + "&m=sum:" + _m + _tag

        try :
            tsdbdata = urllib2.urlopen(url_tsdb)
            _read_buf = tsdbdata.read() # get string of TSDB value

        except urllib2.HTTPError as e:
            error_msg = e.read()
            print "\n < There is no data in TSDB of requested Metric or Tag : %s> \n" %_tag
            #print "\n < BerePi grep error message from Server > \n\n", error_msg
            return False, '[]' 

        except urllib2.URLError as e:
            if hasattr(e, 'reason'):
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'Error code: ', e.code
            print "\n < Timeout error : %s> \n" %_tag
            return False, '[]'
        
        if _read_buf !='[]' : 
            _ext_f = True
            _read_buf = _read_buf[1:-1]
            _buf_dict = ast.literal_eval(_read_buf)
        else : 
            _ext_f = False
            _buf_dict = _read_buf

        #print type(_buf_dict)
        #print _buf_dict

        return _ext_f, _buf_dict

    '''
    ## 함수 : readTSD
    parameter1 (in_datelist) : 시각 리스트
    parameter2 (in_mdsid_list) : 미터기 아이디 리스트
    반환 (retList) : 비어있지 않은 아이디 리스트
    (예) http://xxx.xxx.xxx.xxx:4242/#start=2016/11/01-00:00:00&end=2017/03/01-00:00:00
    &m=sum:origin_data_please{factory_mart=mart,led_inverter=led}
    '''
    def readTSD(self, _tag = None) :
        _m = self.__cin_metric_name
        _p = self.__cin_datelist
        s = ''
        if _tag != None: 
            for (k, v) in _tag.items():
                s += '%s=%s,' % (k, v)
            s = '{' + s[:-1] + '}'

        _existence, _val = self.get_tsdb_value(s)

        if _existence == False : return None
        
        return _val   

    def readTSDrecent(self,  _tag = None, _agg = None, _start = '10m-ago', _end = "10m-later") :
        #if self.__cin_recent != 'True' : exit (" <Error> check call for *recent* ")
        _u = self.__cin_url
        _m = self.__cin_metric_name
        if _agg == None : _agg = 'sum'

        url = '%sstart=%s' % (_u, _start)
        url += '&end=%s' % (_end)
        url += '&m=%s:%s' % (_agg, _m)
                
        #_tag_dict = ast.literal_eval(_tag)
        #assert isinstance(_tag, dict)
        if 0:
            print len(_tag)
            print '5번'
            if (len(_tag) == 0):
                print '6번'
                url += '{'
                for (k, v) in _tag.items():
                    url += '%s=%s,' % (k, v)
                url = url[:-1] + '}'
                print "url : %s" % url
                print '7번'
                try : ret = requests.get(url=url)
                except:
                    print " <Error>... get restful"

        #print "\n Receive OK from server.... " + str(ret) + "\n"
        try : ret = requests.get(url=url)
        except:
            print " <Error>... get restful"
        if ret.ok:            
            data = ret.json()
            assert isinstance(data, (list, tuple))
            return data
            
            dps = data[0]['dps']
            assert isinstance(dps, dict)  # 't' --> value
            if len(dps):
                max_time = sorted(dps.keys())[-1]
                value = dps[max_time]
                epoch = float(max_time)
                ts = datetime.datetime.fromtimestamp(epoch).strftime('%Y-%m-%d %H:%M:%S')
                return (value, ts, epoch)
########## end of class u_tsdb

'''
## 함수 : dateInt
문자열 date를 정수형으로 변환
parameter1 (in_time) : 문자형 date 값
parameter2 (mdh) : 연, 월, 일, 시간의 분류 (y, m, d, h)
반환 (re_mdh) : 변환 된 정수
'''
def dateInt(in_time, mdh):
    # year
    if mdh == 'y': re_mdh = int(in_time[0:4])
    # month
    if mdh == 'm':
        if in_time[4] == '0': re_mdh = int(in_time[5])
        else: re_mdh = int(in_time[4:6])
    # day
    elif mdh == 'd':
        if in_time[6] == '0': re_mdh = int(in_time[7])
        else: re_mdh = int(in_time[6:8])
    # hour
    elif mdh == 'h':
        if in_time[8] == '0': re_mdh = int(in_time[9])
        else: re_mdh = int(in_time[8:10])
    return re_mdh

'''
## 함수 : twodigitZero
한자리 정수 에 0을 추가
'''
def twodigitZero(in_num):
    if in_num < 10: re_num = '0' + str(in_num)
    else:
        re_num = str(in_num)
    return re_num

def parse_args():
    story = 'OpenTSDB needs many arguments URL, start time, end time, port '
    usg = '\n python tsdb_read.py  -url x.x.x.x -port 4242 -start 20161101 -end 20161102, --help for more info'
    parser = argparse.ArgumentParser(description=story, usage=usg, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-url", default="125.140.110.217", help="URL input, or run fails")
    parser.add_argument("-start", default='2016/07/01-00:00:00', help="start time input, like 2016/07/01-00:00:00")
    parser.add_argument("-end", default='2016/07/02-00:00:00', help="end time input, like 2016/07/02-00:00:00")
    parser.add_argument("-port", default=4242, help="port input, like 4242")
    parser.add_argument("-recent", default="True", help="Time input for recent value")
    parser.add_argument("-m", default="rc04_add_tag_v4", help="metric ")
    args = parser.parse_args()
    
    #check args if valid
    url = args.url
    _ht = 'http://'
    if ( url[:7] != _ht ) : url = _ht + url
    port = args.port
    if  port == 80 : port = ''
    else : port = ":"+ str(port)
    url = url + port +'/api/query?'    

    start = args.start
    if start != None : start = args.start
    end = args.end
    if end != None : end = args.end

    recent = args.port
    if recent != None : recent = args.recent

    m = args.m
    if m == None : exit("... please input metric name")
    
    return url, port, start, end, recent, m

def ptest(__url, __st, __et, __m):
    tsdbclass = u_ee_tsdb(__url, __st, __et)
    tag = __m
    if (tag == None) : return
    tsdbclass.set_metric(tag)
    print tsdbclass.readTSD()

def rtest(__url, __m, __tag, __stime, __etime):
    tsdbclass = u_ee_tsdb(__url, None, None, True)
    tsdbclass.set_metric(__m)    
    #tag = __tag
    tag = ""    # tag가 없는 관계로 빈값을 입력
    stime = __stime
    etime = __etime
    #if (tag == None) : return
    
    # print tsdbclass.readTSDrecent(tag, 'sum', __stime)
    list_data = tsdbclass.readTSDrecent(tag, 'none', stime, etime)
    return list_data

def point(__url, __m, __time, __tag):
    tsdbclass = u_ee_tsdb(__url, __time)
    tsdbclass.set_metric(__m)
    tag = __tag
    if (tag == None) : return
    print tsdbclass.readOnePoint(__time, tag, 'sum')

def printProgress (iteration, total, prefix = '', suffix = '', decimals = 1, barLength = 100):
    formatStr = "{0:." + str(decimals) + "f}"
    percent = formatStr.format(100 * (iteration / float(total)))
    filledLength = int(round(barLength * iteration / float(total)))
    bar = '#' * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percent, '%', suffix)),
    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()

if __name__ == "__main__":
    u, p, stime, etime, recent, metric = parse_args()
    
    put_url = "http://125.140.110.217:4242/api/put" # api/put에 값을 주지 않는다면 db는 받질 않는다.
    new_metric = 'rc04_khj_copy_v4'                 # 새로 put할 metric 설정하는 변수 (원하는 metric명을 입력하면 된다.)
    progress_num = 0
    
    if recent == 'True' :
        tag = ""    # 특정 tag가 없음(시간을 기준으로 get한 모든 값을 얻기 위함)
        get_list_data = rtest(u, metric, tag, stime, etime)
    else:
        print "Sorry... Not ready to Get"
        exit()
    
    print '<총 {0!r}개의 데이터 추출>\n'.format(len(get_list_data))
    for i in range(len(get_list_data)):        
        modem_num = get_list_data[i]['tags']['modem_num']
        mds_id = get_list_data[i]['tags']['_mds_id']
        holiday = get_list_data[i]['tags']['holiday']
        load = get_list_data[i]['tags']['load']
        company = get_list_data[i]['tags']['company']
        device_type = get_list_data[i]['tags']['device_type']
        building = get_list_data[i]['tags']['building']
        
        progress_num += 1        
        for (unix_time, value) in get_list_data[i]['dps'].items():
            input_data = {
                "metric": new_metric,
                "timestamp": unix_time,
                "value": value,
                "tags": {
                    "_mds_id": mds_id,
                    "modem_num": modem_num,
                    "device_type": device_type,
                    "company": company,
                    "load": load,
                    "building":building,
                    "holiday": holiday,
                }
            }
            try:
                input_data=json.dumps(input_data)
                ret = requests.post(put_url, input_data)
            except urllib2.HTTPError as e:
                error_msg = e.read()
                print ( "exception during requests HTTP", error_msg)
        print '<총 {0!r}/{1!r}개의 Data를 처리>'.format(progress_num, len(get_list_data))
        printProgress(progress_num, len(get_list_data[i]['dps']), 'Progress:', 'Complete', 1, 50) # show progress
        print '\n'
    print 'end!\n'
    
