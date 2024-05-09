import pygame


def play_audio_non_blocking(file_path):
    pygame.init()  # pygame 전체를 초기화
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

if __name__ == "__main__":
    audio_file_path = 'audio/output.wav'
    play_audio_non_blocking(audio_file_path)

