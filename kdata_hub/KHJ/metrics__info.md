### OpenTSDB Metric에 대한 info
##### OpenTSDB URL : http://125.140.110.217:4242

#### metric : rc04_add_tag_v4
	* rc04_simple_data_v3의 data를 get하여 excel의 data를 참고하여 device_type을 구분하여 tag를 추가한 metric
	* tag의 info는 excel을 참조함
		* https://github.com/imbornagainer/MyProject/blob/master/kdata_hub/KHJ/ref_list_kjh.xlsx
	* rc04_simple_data_v3에 tag를 추가함 (밑은 추가한 tag lists)
		* modem_num 	- 모뎀시리얼넘버
		* _mds_id   	- 계량기시리얼넘버
		* company   	- 기업유형(사업장)
		* building  	- 건물용도
		* load      	- 부하형태
		* device_type	- 계측 설비형태
		* holiday	- 주일(토,일)

#### metric : rc03_add_led_tag_v9
	* rc04_simple_data_v3의 data를 get하여 _input_list_17_0906.py의 Modem_list의 값만 뽑아서 device_type로 구분하여 tag를 추가한 metric
	* tag의 info는 py을 참조함
		* https://github.com/imbornagainer/MyProject/blob/master/kdata_hub/lib/_input_list_17_0906.py
	* rc04_simple_data_v3에 tag를 추가함 (밑은 추가한 tag lists)
		* modem_num 			- 모뎀시리얼넘버
		* _mds_id   			- 계량기시리얼넘버
		* modem_led_inverter 		- 계측 설비형태
		* holiday			- 주일(토,일)
		
#### metric : rc04_khj_copy_v5
	* rc04_add_tag_v4의 metric을 copy한 metric
	* tag가 아닌 시간을 기준으로 get함
		* ex) From 2016/07/01-00:00:00 ~ To 2017/05/01-00:00:00
	* rc04_add_tag_v4의 data를 get한 후 copy (밑은 copy된 tag lists)
		* modem_num 	- 모뎀시리얼넘버
		* _mds_id   	- 계량기시리얼넘버
		* company   	- 기업유형(사업장)
		* building  	- 건물용도
		* load      	- 부하형태
		* device_type	- 계측 설비형태
		* holiday	- 주일(토,일)
