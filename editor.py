import os
import asyncio
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, ImageClip, AudioFileClip, CompositeAudioClip
from PIL import Image
import edge_tts

async def gerar_voz_antonio(texto, caminho_audio):
    """Gera a voz do Antônio via Edge-TTS (Sem dependências pesadas)"""
    communicate = edge_tts.Communicate(texto, "pt-BR-AntonioNeural")
    await communicate.save(caminho_audio)

def processar_video_completo(caminho_video, caminho_img_apres, caminho_musica, texto, cor, caminho_saida, volume_musica=0.15):
    try:
        # 1. Preparar Áudio (Voz + Trilha)
        audio_locucao_path = "temp/preview_voz.mp3"
        voz_clip = AudioFileClip(audio_locucao_path)
        
        musica_fundo = AudioFileClip(caminho_musica).volumex(volume_musica).set_duration(voz_clip.duration + 1)
        
        audio_final = CompositeAudioClip([
            voz_clip.set_start(0.5).volumex(1.4), 
            musica_fundo
        ])

        # 2. Preparar Vídeo Base (9:16 Vertical)
        clip = VideoFileClip(caminho_video).resize(height=1920)
        if clip.w > 1080:
            clip = clip.crop(x_center=clip.w/2, width=1080)
        
        clip = clip.set_duration(audio_final.duration).set_audio(audio_final)

        # 3. Preparar Apresentador (Sem IA de remoção para evitar erros)
        img = Image.open(caminho_img_apres)
        img_temp_path = "temp/apres_processado.png"
        img.save(img_temp_path)

        apresentador = (ImageClip(img_temp_path)
                        .set_duration(clip.duration)
                        .resize(height=clip.h * 0.45)
                        .set_pos(('left', 'bottom'))) 

        # 4. Legendas Dinâmicas (Corrigido para Hostinger)
        txt_clip = TextClip(
            texto.upper(), 
            fontsize=70, 
            color=cor, 
            font='Arial-Bold',
            method='caption',
            size=(clip.w*0.8, None),
            stroke_color='black',
            stroke_width=2
        ).set_duration(clip.duration).set_pos(('center', 300))

        # 5. Renderização Final de Alta Velocidade
        video_final = CompositeVideoClip([clip, apresentador, txt_clip])
        video_final.write_videofile(
            caminho_saida, 
            codec="libx264", 
            audio_codec="aac", 
            fps=24, 
            preset="ultrafast",
            threads=4
        )
        
        # Limpeza de memória
        clip.close()
        video_final.close()
        voz_clip.close()
        musica_fundo.close()
        
        return True, "Sucesso"
    except Exception as e:
        return False, f"Falha na Fábrica: {str(e)}"