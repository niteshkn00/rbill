import http.server
import socketserver
import urllib.parse
import json

# Menu items and their prices
menu_items = {
    "Burger": 149,
    "Pizza": 299,
    "Pasta": 249,
    "Fries": 99,
    "Salad": 129,
    "Soda": 49,
    "Coffee": 79
}

# Handle GET and POST requests
class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Serve static files (HTML, CSS, JS)
        if self.path == '/':
            self.path = '/static/index.html'
        elif self.path.startswith('/static'):
            self.path = '.' + self.path
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        # Handle form submission for bill calculation
        if self.path == "/calculate_bill":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            post_data = urllib.parse.parse_qs(post_data.decode('utf-8'))

            total = 0
            details = []

            # Calculate the total bill based on input quantities
            for item, price in menu_items.items():
                if item in post_data:
                    quantity = int(post_data[item][0])
                    if quantity > 0:
                        cost = quantity * price
                        total += cost
                        details.append(f"{item} x {quantity} = ₹{cost:.2f}")

            response = {
                "total": f"₹{total:.2f}",
                "details": details
            }

            # Send the response in JSON format
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())

# Run the server
PORT = 8000
Handler = MyRequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler)

print(f"Serving on port {PORT}")
httpd.serve_forever()
