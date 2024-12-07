from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse

# Daftar film dan harga tiket
films = {
    "Avatar 2": "Avatar 2",
    "Avengers: Endgame": "Avengers: Endgame",
    "Titanic": "Titanic",
    "Fast X": "Fast X",
    "Spiderman: No Way Home": "Spiderman: No Way Home",
    "Minions: Rise of Gru": "Minions: Rise of Gru"
}
ticket_price = 25000  # Harga tiket

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('index.html', 'r') as file:
                self.wfile.write(file.read().encode())
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == '/process':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = urlparse.parse_qs(post_data.decode())

            # Mengambil data dari form
            nama = data.get('nama')[0]
            film = data.get('film')[0]
            jumlah_tiket = int(data.get('jumlah')[0])

            # Menghitung total harga
            total_harga = jumlah_tiket * ticket_price

            # Menyusun respon kwitansi
            response_content = f"""
            <html>
            <body>
                <h2>Kwitansi Bioskop</h2>
                <p><strong>Nama Pelanggan:</strong> {nama}</p>
                <p><strong>Film:</strong> {film}</p>
                <p><strong>Jumlah Tiket:</strong> {jumlah_tiket}</p>
                <p><strong>Total Harga:</strong> Rp{total_harga:,}</p>
                <a href="/">Kembali</a>
            </body>
            </html>
            """
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(response_content.encode())

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Serving at port {port}')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
