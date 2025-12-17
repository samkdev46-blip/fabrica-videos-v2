import yt_dlp
import os

class MotorNewPipe:
    def __init__(self):
        self.ydl_opts = {
            # Busca o melhor vídeo vertical (formato Shorts/Reels/TikTok)
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
            'quiet': True,
            'no_warnings': True,
            # Disfarce de Android (Igual ao NewPipe)
            'user_agent': 'Mozilla/5.0 (Android 11; Mobile; rv:94.0) Gecko/94.0 Firefox/94.0',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
        }

    def buscar_e_preparar(self, termo):
        """
        Busca no YouTube/TikTok/Instagram usando a lógica de extração direta.
        """
        busca = f"ytsearch5:{termo} achadinhos"
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            # Extraímos apenas os metadados primeiro (rápido como um flash)
            info = ydl.extract_info(busca, download=False)
            results = []
            for entry in info['entries']:
                results.append({
                    'titulo': entry.get('title'),
                    'url': entry.get('webpage_url'),
                    'duracao': entry.get('duration'),
                    'thumbnail': entry.get('thumbnail')
                })
            return results

    def baixar_alvo(self, url):
        """
        O sequestro final do vídeo para edição.
        """
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return ydl.prepare_filename(info)