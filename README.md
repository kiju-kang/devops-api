## Infra api service

- 외부 api 및 기타 기능을 사용자 입장에서 쉽게 사용할 수 있도록 제작 하였습니다.

정책 및 동작

- 사용자의 요청을 redis에 저장하는 api server 와 요청받은 job을 처리하는 redis handler daemon 이 동작 하게 됩니다.
- 사용자의 요청이 들어오면 chat_id 파라미터를 key 값으로 value 값을 member로 redis 에 저장합니다.
- 사용자 요청 return 값으로 job 을 정상적으로 요청 받았다는 응답을 주거나 잘못된 요청일 경우 error code 를 반환 해줍니다.
- redis handler daemon 은 redis에 저장된 사용자 요청을 꺼내 함수를 호출하고 처리 결과를 chat_id 에 맞게 telegram 으로 메시지를 발송합니다.


## Cloudflare API 프로토콜

ㅁ 네트워크 프로토콜
 - HTTP

ㅁ 네트워크 주소
 - 192.168.x.x

ㅁ 네트워크 포트
 - 8080

ㅁ URL
 - http://{네트워크 주소}/api/{버전}/{도메인}/{서비스}?{파라미터}
 - 예제
  > http://192.168.x.x:8080/v1/cf/search?ip=1.1.1.1&chat_id=-12345678

ㅁ 프로토콜

Version | Domain | Method |     Path              |      Query                                                       | Description
------- |--------|--------|-----------------------|------------------------------------------------------------------|------------------
v1	    | cf     | POST	  | /api/v1/cf/block	  | ip = {차단 ip주소},             chat_id = {return 받을 chat_id}	 | ip 차단
v1	    | cf	 | POST	  | /api/v1/cf/release    | ip = {차단해제 ip주소},         chat_id = {return 받을 chat_id}  | ip 차단 해제
v1	    | cf     | GET	  | /api/v1/cf/search     | ip = {차단여부 확인 ip주소},    chat_id = {return 받을 chat_id}  | ip 차단여부 확인



## Telegram API 프로토콜

ㅁ 네트워크 프로토콜
 - HTTP

ㅁ 네트워크 주소
 - 192.168.x.x

ㅁ 네트워크 포트
 - 8080

ㅁ URL
 - http://{네트워크 주소}/api/{버전}/{도메인}/{서비스}?{파라미터}
 - 예제
  > http://192.168.x.x:8080/v1/telegram?chat_id=-123456&text=test message

ㅁ 프로토콜

Version | Domain   | Method | Path                  | Query                                                            | Description
------- |----------|--------|-----------------------|------------------------------------------------------------------|------------------
v1	    | telegram | GET	| /api/v1/telegram	    | chat_id = {message 보낼 채팅방} text = {message 내용}	           | telegram 메시지 발송




1. install requirements python modules

```bash
pip install -r requirements.txt

python redis_handler.py

nohup python -u infra_api_server.py &
```