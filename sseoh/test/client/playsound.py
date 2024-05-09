import pygame

def play_audio_non_blocking(file_path):
    pygame.mixer.init()  # Pygame의 mixer 모듈을 초기화합니다.
    pygame.mixer.music.load(file_path)  # 재생할 오디오 파일을 로드합니다.
    pygame.mixer.music.play()  # 오디오 파일을 재생합니다.

if __name__ == "__main__":
    audio_file_path = 'audio//output.wav'
    play_audio_non_blocking(audio_file_path)
