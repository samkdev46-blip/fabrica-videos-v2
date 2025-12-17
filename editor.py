from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import os

def processar_video(caminho_input, caminho_output, texto, cor):
    try:
        # Carrega o vídeo
        clip = VideoFileClip(caminho_input)
        
        # Cria o texto (Overlay)
        # Nota: Na VPS, certifique-se de ter o ImageMagick instalado para o TextClip funcionar
        txt_clip = TextClip(texto, fontsize=70, color=cor, font='Arial-Bold', method='caption', size=(clip.w*0.8, None))
        
        # Define a posição e duração do texto
        txt_clip = txt_clip.set_pos('center').set_duration(clip.duration)
        
        # Sobrepõe o texto ao vídeo
        video_final = CompositeVideoClip([clip, txt_clip])
        
        # Salva o arquivo final
        video_final.write_videofile(caminho_output, codec='libx264', audio_codec='aac', fps=24)
        
        # Fecha os clips para liberar memória da VPS
        clip.close()
        txt_clip.close()
        
        return True, "Sucesso"
    except Exception as e:
        return False, str(e)