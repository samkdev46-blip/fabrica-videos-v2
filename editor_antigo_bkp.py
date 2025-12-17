import os
import asyncio
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, ImageClip, AudioFileClip
from rembg import remove
from PIL import Image
import io
import edge_tts

async def gerar_voz_antonio(texto, caminho_audio):
    """Gera a voz do Antônio."""
    # [FIX] Corrigido de camin_audio para caminho_audio
    communicate = edge_tts.Communicate(texto, "pt-BR-AntonioNeural")
    await communicate.save(caminho_audio)

def processar_video_completo(caminho_video, caminho_img_apres, caminho_musica, texto, cor, caminho_saida, volume_musica=0.15):
    try:
        # 1. GERAÇÃO DA VOZ
        audio_locucao_path = "temp/voz_antonio.mp3"
        asyncio.run(gerar_voz_antonio(texto, audio_locucao_path))
        voz_clip = AudioFileClip(audio_locucao_path)

        # 2. VÍDEO BASE (9:16 Vertical)
        clip = VideoFileClip(caminho_video).resize(height=1920)
        if clip.w > 1080:
            clip = clip.crop(x_center=clip.w/2, width=1080)
        
        # 3. TRILHA SONORA
        # [FIX] Corrigido erro de 'size' tratando áudio e vídeo separadamente
        musica = AudioFileClip(caminho_musica).volumex(volume_musica).set_duration(clip.duration)
        
        # Mixagem: Antônio com prioridade
        audio_final = CompositeVideoClip([voz_clip.set_start(0.5), musica]).audio
        clip = clip.set_audio(audio_final)

        # 4. APRESENTADOR (Remoção de fundo e Movimento)
        with open(caminho_img_apres, "rb") as i:
            input_img = i.read()
            output_img = remove(input_img)
            img = Image.open(io.BytesIO(output_img))
            caminho_temp_png = "temp/apres_limpo.png"
            img.save(caminho_temp_png)

        apresentador = (ImageClip(caminho_temp_png)
                        .set_duration(clip.duration)
                        .resize(height=clip.h * 0.45)
                        .set_pos(lambda t: (70 + (25 * t), clip.h - (clip.h * 0.45) - 100))) 

        # 5. LEGENDAS
        txt_clip = (TextClip(texto, fontsize=70, color=cor, font='Arial-Bold', 
                             method='caption', size=(clip.w*0.8, None))
                    .set_duration(clip.duration)
                    .set_pos(('center', 200)))

        # 6. MONTAGEM E RENDERIZAÇÃO
        video_final = CompositeVideoClip([clip, apresentador, txt_clip])
        video_final.write_videofile(caminho_saida, codec="libx264", audio_codec="aac", fps=30, preset="ultrafast")
        
        clip.close()
        video_final.close()
        return True, "Ritual concluído com sucesso!"
    except Exception as e:
        return False, f"O ritual falhou: {str(e)}"