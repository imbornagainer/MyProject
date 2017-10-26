* metric_copy_khj.py - 메트릭 복사코드 실행방법

	1. parse_args 함수에서 get(얻고)하고 싶은 정보들을 작성한다. (help의 like 형식대로 작성하면 된다.)
		```
		parser.add_argument("-url", default="125.140.110.217", help="URL input, or run fails")
		parser.add_argument("-start", default='2016/07/01-00:00:00', help="start time input, like 2016/07/01-00:00:00")
		parser.add_argument("-end", default='2016/07/02-00:00:00', help="end time input, like 2016/07/02-00:00:00")
		parser.add_argument("-port", default=4242, help="port input, like 4242")
		parser.add_argument("-recent", default="True", help="Time input for recent value")
		parser.add_argument("-m", default="rc04_add_tag_v4", help="metric name")
		```

	2. main 함수에서 new_metric에 값을 넣어준다.
		* get한 data를 입력하고 싶은 metric의 이름을 입력한다.

	3. input_data에 get에서 얻은 tags값을 입력한다.
		* get한 metric이 변경되었다면 data에 따라서 tags의 name들을 get에서 얻은 data에 맞게 변경해주어야 한다. (밑의 소스를 수정하면 됨)
	```
		modem_num = get_list_data[i]['tags']['modem_num']
		mds_id = get_list_data[i]['tags']['_mds_id']
		holiday = get_list_data[i]['tags']['holiday']
		load = get_list_data[i]['tags']['load']
		company = get_list_data[i]['tags']['company']
		device_type = get_list_data[i]['tags']['device_type']
		building = get_list_data[i]['tags']['building']

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
	```
* Metric info - 테스트가 끝나고, 분석에 사용할 데이터 info
	* https://github.com/jeonghoonkang/kdatahub/blob/master/EE-data-analysis/YKPK/KHJ/metrics__info.md

* Data 단계별로 진행되는 사항 - 오라클에서 데이터 읽어오는 부분부터 해서 단계별로 진행되는 사항
    1. 에너지공단에서 (에너지 절감 지원사업)으로 경쟁 모집
    1. 선정된 업체는 현장에 에너지 절감형 LED, 인버터 등을 새로 설치하고, 해당
       비용중 일부를 에너지공단에서 지원받음
    1. 설치시에. 전체 설치중 5% 부분에 대해 LTE 전력량계를 설치함
	1. 이 LTE 전력량계는 (옴니시스템, 누리텔레콤 등)에서 설치함. 해당 LTE 전력량계의 정보는 엑셀파일로 작성 보관함
    1. 이 LTE 전력량계는 15분 단위로 ORACLE DB에 측정 값을 저장한다
	3. ORACLE DB에 저장된 DATA를 OPENTS DB에 전송, 복사 저장한다
		- 이 DATA는 순수한 DATA이다 
        - DEVICE_TYPE에 대한 구분이 없는 모든 DATA라는 것을 뜻함
        - LTE 모뎀 전화번호만 들어있는 경우
	4. OPENTS DB에 저장된 순수한 DATA에 TAG를 붙여 DATA를 분류한다.
		- EX) DEVICE_TYPE을 구분 LED, INVERTER인지
        - 여기서 매트릭을 새롭게 생성하여 데이터를 복사함
	5. OPENTS DB에는 분류된 값들이 METRIC에 저장된다
	6. 필터링된 Energy data를 graph로 출력한다
	* 참고 pptx
		* https://github.com/jeonghoonkang/kdatahub/blob/master/EE-data-analysis/YKPK/KHJ/Process%20of%20reading%20data.pptx
