### Screen이란?
* Screen이란 Linux에서 물리적인 터미널을 여러 개의 가상 터미널로 다중화해주는 도구입니다. 각 가상 터미널은 독립적으로 동작하며 사용자 세션이 분리되어도 동작합니다. 간단히 말하면 이 도구는 백그라운드로 동작하는 다중 터미널을 만들어 줍니다. 이걸 이용해서 백그라운드 작업을 간단히 수행할 수도 있고 회사에서 작업하던 터미널 화면을 집에 가서도 같은 터미널 화면을 보며 작업을 이어 할 수도 있습니다.

* Install
  * screen 이라는 명령어를 실행했을때 명령어가 없다고 나오면 아래와 같이 설치를 해줍니다.

* cygwin
  * apt-cyg install screen

* RedHat계열 (RedHat, CentOS, Fedora 등...)
  * yum install screen
  * Debian 계열(Ubuntu 등..)
  * apt-get install screen

* 사용법 - 참고 url
 * http://dreamlog.tistory.com/470

* 추가 환경 설정
  * 아래와 같이 설정 파일을 추가해주면 Screen 사용 시 좀 더 편해집니다. 적용하시는 것을 추천합니다. 각 가상 터미널의 창 구분도 되고 시계도 표시되는 등 더 보기 편해집니다.
  
* vi ~/.screenrc

```
defscrollback 5000
termcapinfo xterm* ti@:te@
startup_message off
hardstatus on
hardstatus alwayslastline
hardstatus string "%{.bW}%-w%{.rW}%n*%t%{-}%+w %= %c ${USER}@%H"
bindkey -k k1 select 0
bindkey -k k2 select 1
bindkey -k k3 select 2
왼쪽이 추가 환경 설정이 적용된 모습이며 오른쪽이 아무 설정도 하지 않고 screen을 실행했을 시 모습입니다. 추가 환경 설정을 하여 Screen을 사용하고 있는지, 어느 가상 터미널에 있는지 확인할 수 있습니다.
