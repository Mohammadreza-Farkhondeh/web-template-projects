import http.server
import json
import jwt

SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"
PORT = 8000


class JWTRequestHandler(http.server.BaseHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        http.server.SimpleHTTPRequestHandler.end_headers(self)

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        request_body = self.rfile.read(content_length)

        request_data = json.loads(request_body)
        print(request_data)
        print(self.path)
        if self.path == "/auth/signup/":
            self.handle_signup(request_data)
        elif self.path == "/auth/token/obtain/":
            self.handle_obtain(request_data)
        elif self.path == "/auth/token/refresh/":
            self.handle_refresh(request_data)
        else:
            self.send_error(404, "Not Found")

    def handle_signup(self, request_data):
        username = request_data.get("username")
        password1 = request_data.get("password1")
        password2 = request_data.get("password1")
        if password2 != password1:
            response_data = {"message": "Password not match"}
        else:
            print(f"Signup: {username}, {password1}")
            response_data = {"message": "Signup successful"}

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response_data).encode())

    def handle_obtain(self, request_data):
        username = request_data.get("username")
        password = request_data.get("password")

        valid = True

        if valid:
            access_payload = {
                "username": username,
                "type": "access"
            }

            refresh_payload = {
                "username": username,
                "type": "refresh"
            }

            access_token = jwt.encode(access_payload, SECRET_KEY, ALGORITHM)
            refresh_token = jwt.encode(refresh_payload, SECRET_KEY, ALGORITHM)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            response_data = {
                "accessToken": access_token,
                "refreshToken": refresh_token
            }
            self.wfile.write(json.dumps(response_data).encode())
        else:
            self.send_error(401, "Unauthorized")

    def handle_refresh(self, request_data):
        refresh_token = request_data.get("refreshToken")

        try:
            refresh_payload = jwt.decode(refresh_token, SECRET_KEY, ALGORITHM)

            if refresh_payload["type"] == "refresh":
                username = refresh_payload["username"]

                access_payload = {
                    "username": username,
                    "type": "access"
                }

                access_token = jwt.encode(access_payload, SECRET_KEY, ALGORITHM)

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                response_data = {
                    "access_token": access_token
                }
                self.wfile.write(json.dumps(response_data).encode())
            else:
                self.send_error(400, "Bad Request")
        except jwt.InvalidTokenError:
            self.send_error(401, "Unauthorized")


server = http.server.HTTPServer(("", PORT), JWTRequestHandler)
print(f"Server running on port {PORT}")
server.serve_forever()
