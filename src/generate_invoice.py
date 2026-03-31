from http.server import SimpleHTTPRequestHandler, HTTPServer
import json
from invoice import generate_invoice

class RequestHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/generate_invoice':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)

            customer_name = data['customer_name']
            items = data['items']
            total_btc = data['total_btc']

            invoice_path = generate_invoice(customer_name, items, total_btc)

            with open(invoice_path, 'rb') as f:
                self.send_response(200)
                self.send_header('Content-type', 'application/pdf')
                self.send_header('Content-Disposition', f'attachment; filename="{invoice_path}"')
                self.end_headers()
                self.wfile.write(f.read())
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    server_address = ('', 5000)
    httpd = HTTPServer(server_address, RequestHandler)
    print("Servidor iniciado en http://localhost:5000")
    httpd.serve_forever()