from constant import AUDIO
from google.cloud import texttospeech        
from google.cloud import storage
from google.oauth2 import service_account

def text_to_speech(text):
    # 왜 환경변수 설정이 안될까?
    credentials = service_account.Credentials.from_service_account_file('/home/hyelim/bbns-416110-ea8d5da13b61.json')
    client = storage.Client(credentials=credentials)

    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.types.SynthesisInput(text=text)

    voice = texttospeech.types.VoiceSelectionParams(
        language_code='ko-KR',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)

    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    response = client.synthesize_speech(synthesis_input, voice, audio_config)

    with open(AUDIO, 'wb') as out:
        out.write(response.audio_content)
        print('Audio content written to file AUDIO')
    
    
    # # 최대 길이를 200으로 지정 (지나치게 길어지면 에러 발생)
    # max_length = 200   
    # # . 단위로 문장 분리
    # words = text.split('. ')
    # sentences = []
    # current_sentence = ''
    # for word in words:
    #     if len(current_sentence + word) <= max_length:
    #         current_sentence += word + ' '
    #     else:
    #         sentences.append(current_sentence.strip() + '.')
    #         current_sentence = word + ' '
    # if current_sentence:
    #     sentences.append(current_sentence.strip() + '.')

    
    # # 빈 배열 생성
    # audio_data = []

    # # 문장 개수 단위로 텍스트 변환
    # for sentence in sentences:
    #     input_text = texttospeech.SynthesisInput(text=sentence)

    #     # 오디오 설정 (예제에서는 한국어, 남성C)
    #     voice = texttospeech.VoiceSelectionParams(
    #         language_code="ko-KR",
    #         name="ko-KR-Neural2-C",
    #         ssml_gender=texttospeech.SsmlVoiceGender.MALE,
    #     )

    #     audio_config = texttospeech.AudioConfig(
    #         audio_encoding=texttospeech.AudioEncoding.MP3
    #     )

    #     response = client.synthesize_speech(
    #         request={"input": input_text, "voice": voice, "audio_config": audio_config}
    #     )

    #     audio_data.append(response.audio_content)
  
    # audio_data = b"".join(audio_data)
    
    # # audio 폴더 안에 output.mp3라는 이름으로 파일 생성
    # with open(AUDIO, "wb") as out:        
    #     out.write(audio_data)
    #     print('오디오 파일 생성')
