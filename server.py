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
                self.end_headers()
                self.wfile.write(json.dumps(files).encode())
            else:
                self.send_error(404, "Music directory not found")
            return
        
        # Servir index.html pour la racine
        elif self.path == '/' or self.path == '/index.html':
            self.path = '/index.html'
            return super().do_GET()
                
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
    
    # Créer un index.html basique s'il n'existe pas
    if not os.path.exists('index.html'):
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write('''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Serveur Musique</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f0f0f0; }
        .player { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        audio { width: 100%; margin: 20px 0; }
        .playlist { list-style: none; padding: 0; }
        .playlist li { padding: 10px; margin: 5px 0; background: #e0e0e0; border-radius: 5px; cursor: pointer; }
        .playlist li:hover { background: #d0d0d0; }
    </style>
</head>
<body>
    <div class="player">
        <h1>🎵 Mon Serveur Musique</h1>
        <audio id="audioPlayer" controls></audio>
        <h3>Playlist:</h3>
        <ul id="playlist" class="playlist"></ul>
    </div>

    <script>
        async function loadPlaylist() {
            try {
                const response = await fetch('/api/music');
                const musicList = await response.json();
                const playlist = document.getElementById('playlist');
                const audioPlayer = document.getElementById('audioPlayer');

                musicList.forEach(music => {
                    const li = document.createElement('li');
                    li.textContent = music.name;
                    li.onclick = () => {
                        audioPlayer.src = music.url;
                        audioPlayer.play();
                    };
                    playlist.appendChild(li);
                });

                if (musicList.length > 0) {
                    audioPlayer.src = musicList[0].url;
                }
            } catch (error) {
                console.error('Erreur:', error);
                document.getElementById('playlist').innerHTML = '<li>Erreur de chargement</li>';
            }
        }

        loadPlaylist();
    </script>
</body>
</html>''')
        print("📄 Fichier index.html créé automatiquement")
    
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
