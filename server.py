import http.server
import socketserver
import os
import json
from urllib.parse import unquote

PORT = 8000

class MusicRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # API pour lister les fichiers music
        if self.path == '/api/music':
            music_dir = 'music'
            if os.path.exists(music_dir):
                files = []
                for filename in os.listdir(music_dir):
                    if filename.lower().endswith('.mp3'):
                        files.append({
                            'name': filename.replace('.mp3', ''),
                            'url': f'/music/{filename}'
                        })
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(files).encode())
            else:
                self.send_error(404, "Music directory not found")
            return
                
        # Servir les autres fichiers normalement
        super().do_GET()

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

if __name__ == "__main__":
    # Créer le dossier music s'il n'existe pas
    if not os.path.exists('music'):
        os.makedirs('music')
        print("📁 Dossier 'music' créé - Ajoutez vos fichiers MP3 dedans")
    
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    with socketserver.TCPServer(("", PORT), MusicRequestHandler) as httpd:
        print(f"🎵 Serveur démarré sur http://localhost:{PORT}")
        print("📁 Dossier musique: http://localhost:8000/music/")
        print("🎵 API musique: http://localhost:8000/api/music")
        print("📄 Interface web: http://localhost:8000/")
        print("🛑 Arrêtez avec Ctrl+C")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Serveur arrêté")