시각장애인을 위한 실시간 버스 탑승 알림 시스템(Real-time Bus Boarding Notification System)

- module
1. 비콘
 : 버스-사용자, 버스-버스 정류장, 버스 정류장-사용자
2. 서버(AWS EC2)
 : 음성 인식(목적지), 적절한 버스,음성 합성(버스정보)
3. 데이터베이스(MySQL)
 : 버스 정보, 버스 정류장 정보, 사용자 정보
4. 컨트롤러
 : 목적지 입력, 예/아니오, 뒤로가기


* API
1. STT (Speach-to-Text) : 음성인식
 (1) 인식 정확도
 (2) 가격
 - CLOVA(Naver) : HTTP 기반의 REST API가 X, iOS SDK 형태.
 - Whisper(OpenAI)
 - google
 - kakao
 - pyAudio?
2. TTS (Text-to-Speech) : 음성합성
 (1) 자연스러움
 (2) 가격
 - CLOVA(Naver) : 무료 크레딧O, HTTP 기반의 REST API 형태.

