### openTSDB을 위한 Folder

* 시간계 DB - data를 받아서 graph로 출력해줌
* 참고할만한 site가 없다. 밑의 documents를 보며 참고하는 것 외에는...
    * http://opentsdb.net/docs/build/html/user_guide/
    * opentsdb.net/docs/build/html/user_guide/query/examples.html

### Grafana 
* http://125.140.110.217:3000
* admin / admin
* snapshop capture : https://github.com/jeonghoonkang/kdatahub/blob/master/EE-data-analysis/report/howto/grafana.png

### OpenTSDB
* 접속 ssh opentsdb@125.140.110.217
```
opentsdb@PaaS:~$ screen -list
  There are screens on:
     * 4027.tcollector (2017년 10월 24일 13시 10분 29초)       (Detached)
     * 3753.opentsdb   (2017년 10월 24일 13시 10분 13초)       (Detached)
     * 2 Sockets in /var/run/screen/S-opentsdb.
opentsdb@PaaS:~$ screen -r opentsdb

CTRL + C - (openTSDB restart)
↑ 키 눌러서  02_~~~~ 쉘스크립트 실행

Ctrl A + D (화면만 나옴 - 입력된 명령어는 실행중)
```

### Screen 명령어

1. 쉘모드 명령어
(1) screen

- screen 을 시작 하는 기본 명령입니다.
- 기본 세션명으로 시작합니다.

(2) screen -S 세션명
-S 다음에 주는 세션명으로 시작합니다.
- screen -list
: -list 옵션을 주고 실행하면 이전에 작업했었던 screen 리스트가 있으면 세션명과 함께 리스트를 보여줍니다.

(3) screen -R 세션명

: 이전에 세션이 있을 경우 -R 다음에 오는 세션명으로 이전 작업을 불러옵니다.
: -R 다음에 세션명을 주지 않았을 경우에는 이전 세션이 한개만 있을 경우 그 작업을 불러옵니다.
: 이전 작업이 여러개 있을 경우에는 이전 작업 리스트를 보여줍니다.
: 세션명을 가진 세션이 없다면 새로운 세션을 만들어서 보여줌. (안만들려면 소문자 -r을 사용할 것)

(3) screen -D -r 세션명

: 이전 세션이 Attach 된 상태라면 Detach하고 세션을 복원해 줌.

2. screen 실행후 명령어

screen 실행후의 명령어는 Ctrl-a로 시작합니다:
Ctrl-a, c : (create) 새로운 쉘이 생기면서 그 쉘로 이동
Ctrl-a, a : 바로 전 창으로 이동
Ctrl-a, n : (next) 다음 창으로 이동
Ctrl-a, p : (previous) 이전 창으로 이동
Ctrl-a, 숫자 : 숫자에 해당하는 창으로 이동
Ctrl-a, ' : 창번호 또는 창이름으로 이동 ( ' => 싱글 쿼테이션 )
Ctrl-a, " : 창번호를 보여준다. ( " => 더블 쿼테이션 )
Ctrl-a, A : 현재 창의 title을 수정
Ctrl-a, w : 창 리스트 보여주기
Ctrl-a, esc : Copy 모드로 전환. Copy 모드에서는 vi의 이동키로 이동을 할 수 있다.
Crtl-a, [ 커서 이동을 할 수 있고 특정 블럭을 복사하는 기능으로 사용한다.
먼저 시작 위치에서 space 바를 누르고 끝 위치에서 space 바를 누르면 해당 부분이 buffer로 복사된다.
Ctrl-a, ] : buffer의 내용을 stdin으로 쏟아 넣는다.
이 기능은 vi의 입력모드에서 사용하면 유용하다.
Ctrl-a, :(콜론) : 명령행 모드로 전환
Ctrl-a, d : (detach) 현재 작업을 유지하면서 screen 세션에서 빠져나옴
세션이 종료 되지 않습니다.
Ctrl-a, x : lock screen
아래 부분은 창을 나눠서 사용하는 명령입니다.
Ctrl-a, S : (split) 창을 나눔 (region)
Ctrl-a, Tab : 다른 region으로 이동
Ctrl-a, Q : 현재 region을 제외한 나머지 숨기기

그리고 마지막 명령으로 세션을 완전히 빠져 나오는 명령입니다.
exit : screen 의 쉘상에서 exit 를 치고 엔터를 하면 세션이 완전히 종료 됩니다.
