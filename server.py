import http.server
import socketserver
import os
import json
import threading
from urllib.parse import unquote
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = 8000

class MusicRequestHandler(BaseHTTPRequestHandler):
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
        
        # Servir index.html pour la racine
        elif self.path == '/' or self.path == '/index.html':
            self.path = '/index.html'
            return self.serve_static_file()
        
        # Servir les fichiers statiques
        elif self.path.startswith('/music/') or self.path.endswith(('.html', '.css', '.js', '.png', '.jpg', '.jpeg')):
            return self.serve_static_file()
                
        else:
            self.send_error(404, "File not found")
    
    def serve_static_file(self):
        try:
            # Sécuriser le chemin
            path = self.path.split('?')[0]  # Enlever les paramètres
            if path == '/':
                path = '/index.html'
            
            # Empêcher les accès en dehors du répertoire
            if '..' in path:
                self.send_error(403, "Forbidden")
                return
            
            # Servir le fichier
            super().do_GET()
        except Exception as e:
            self.send_error(500, f"Server error: {str(e)}")
    
    def log_message(self, format, *args):
        # Log personnalisé avec l'IP et le thread
        thread_name = threading.current_thread().name
        print(f"[{thread_name}] {self.address_string()} - {format % args}")
    
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

class ThreadedHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    """Serveur avec support des threads pour gérer plusieurs connexions"""
    daemon_threads = True  # Les threads se ferment quand le serveur s'arrête
    allow_reuse_address = True  # Permet de réutiliser l'adresse rapidement

def run_server():
    # Créer le dossier music s'il n'existe pas
    if not os.path.exists('music'):
        os.makedirs('music')
        print("📁 Dossier 'music' créé - Ajoutez vos fichiers MP3 dedans")
    
    # Vérifier si index.html existe
    if not os.path.exists('index.html'):
        print("❌ Fichier index.html non trouvé!")
        print("📁 Assurez-vous que index.html est dans le même dossier que ce script")
        exit(1)
    
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Utiliser le serveur threadé
    with ThreadedHTTPServer(("", PORT), MusicRequestHandler) as httpd:
        print(f"🎵 Serveur BEATSTREET MULTI-UTILISATEUR démarré sur http://0.0.0.0:{PORT}")
        print("📁 Dossier musique: http://localhost:8000/music/")
        print("🎵 API musique: http://localhost:8000/api/music")
        print("🚀 Interface BEATSTREET: http://localhost:8000/")
        print("")
        print("🌟 Fonctionnalités multi-utilisateurs:")
        print("   ✅ Plusieurs clients simultanés")
        print("   ✅ Threads séparés pour chaque connexion")
        print("   ✅ Streaming audio pour tous les utilisateurs")
        print("   ✅ Pas de blocage entre les requêtes")
        print("")
        print("📊 Statistiques:")
        print(f"   Port: {PORT}")
        print(f"   Répertoire: {os.getcwd()}")
        print(f"   Fichiers MP3 trouvés: {len([f for f in os.listdir('music') if f.endswith('.mp3')])}")
        print("")
        print("🛑 Arrêtez avec Ctrl+C")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Serveur arrêté")

if __name__ == "__main__":
    run_server()
