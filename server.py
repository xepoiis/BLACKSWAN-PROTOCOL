import http.server
import socketserver
import socket
import os
import threading

# --- 1. LÓGICA DEL SERVIDOR WEB (HTTP) ---
class CaptivePortalHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        """Atrapa cualquier petición HTTP y entrega la pantalla roja"""
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        
        ruta_html = os.path.join(os.path.dirname(__file__), 'index.html')
        try:
            with open(ruta_html, 'rb') as file:
                self.wfile.write(file.read())
        except FileNotFoundError:
            self.wfile.write(b"<h1>Error: index.html no encontrado.</h1>")

# --- 2. LÓGICA DEL SECUESTRO DNS (El Auto-Popup) ---
def construir_respuesta_dns(data, ip_local):
    """Construye un paquete de red crudo para mentirle al celular"""
    paquete = data[:2] # ID de transacción
    paquete += b'\x81\x80' # Flags: Respuesta estándar sin errores
    paquete += data[4:6] + data[4:6] + b'\x00\x00\x00\x00' # Contadores
    paquete += data[12:] # La pregunta original del celular
    paquete += b'\xc0\x0c\x00\x01\x00\x01\x00\x00\x00\x3c\x00\x04' # Punteros DNS
    paquete += bytes(map(int, ip_local.split('.'))) # Inyectamos nuestra IP
    return paquete

def iniciar_dns_sinkhole(ip_local):
    puerto_dns = 53
    try:
        udps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udps.bind(('', puerto_dns))
        print(f"[DNS] Secuestro DNS activo en puerto {puerto_dns}. Forzando Auto-Popup...")
        while True:
            data, addr = udps.recvfrom(1024)
            respuesta = construir_respuesta_dns(data, ip_local)
            udps.sendto(respuesta, addr)
    except Exception as e:
        print(f"[ADVERTENCIA DNS] Windows bloqueó el puerto 53. El auto-popup no funcionará, ingresar IP manualmente. Error: {e}")

# --- 3. INICIO DE SERVICIOS ---
def obtener_ip_local():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def iniciar_servidor(puerto=80):
    ip_local = obtener_ip_local()
    
    # Lanzar el secuestrador DNS en un hilo paralelo
    hilo_dns = threading.Thread(target=iniciar_dns_sinkhole, args=(ip_local,), daemon=True)
    hilo_dns.start()
    
    # Lanzar el Servidor Web Multihilo
    httpd = socketserver.ThreadingTCPServer(("", puerto), CaptivePortalHandler)
    print(f"[WEB] Servidor Mesh alojando el portal en el puerto {puerto}...")
    httpd.serve_forever()