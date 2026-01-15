import tkinter as tk
from tkinter import ttk
import socket
import ntplib # Requiere: pip install ntplib
from time import ctime

# --- Lógica DNS ---
def resolver_dns():
    target = entry_dns.get().strip()
    if not target:
        return

    log_dns(f"\n[INFO] Resolviendo: {target}...")
    
    try:
        # 1. Intentar obtener información de dirección (IPs)
        # getaddrinfo devuelve una lista de tuplas con info de la conexión
        info = socket.getaddrinfo(target, 80, proto=socket.IPPROTO_TCP)
        
        ips_encontradas = set()
        for item in info:
            ip = item[4][0]
            ips_encontradas.add(ip)
        
        for ip in ips_encontradas:
            log_dns(f" -> IP: {ip}")
            
        # 2. Intentar obtener el nombre canónico (si existe)
        try:
            nombre, alias, ips = socket.gethostbyaddr(target)
            log_dns(f" -> Nombre oficial: {nombre}")
        except:
            pass # A veces no resuelve a la inversa, no es crítico
            
        log_dns("[OK] Resolución finalizada.")

    except socket.gaierror:
        log_dns("[ERROR] No se pudo resolver. Verifica el nombre.")
    except Exception as e:
        log_dns(f"[ERROR] {str(e)}")

# --- Lógica NTP ---
def consultar_ntp():
    servidor = entry_ntp.get().strip()
    if not servidor:
        return

    log_ntp(f"\n[INFO] Consultando servidor NTP: {servidor}...")
    
    try:
        client = ntplib.NTPClient()
        response = client.request(servidor, version=3)
        
        # Hora del servidor
        hora_servidor = ctime(response.tx_time)
        
        log_ntp(f"[OK] Respuesta recibida.")
        log_ntp(f" -> Hora Servidor: {hora_servidor}")
        log_ntp(f" -> Stratum (Jerarquía): {response.stratum}")
        log_ntp(f" -> Offset (Diferencia): {response.offset} seg")
        
    except Exception as e:
        log_ntp(f"[ERROR] No se pudo conectar: {str(e)}")
        log_ntp(" Nota: Revisa tu conexión a internet o el firewall.")

# Funciones de Log
def log_dns(msg):
    text_log_dns.config(state=tk.NORMAL)
    text_log_dns.insert(tk.END, msg + "\n")
    text_log_dns.see(tk.END)
    text_log_dns.config(state=tk.DISABLED)

def log_ntp(msg):
    text_log_ntp.config(state=tk.NORMAL)
    text_log_ntp.insert(tk.END, msg + "\n")
    text_log_ntp.see(tk.END)
    text_log_ntp.config(state=tk.DISABLED)

# --- Interfaz Gráfica ---
root = tk.Tk()
root.title("NetworkLab - DNS & NTP Client")
root.geometry("700x500")

# Sistema de Pestañas
tab_control = ttk.Notebook(root)
tab_dns = ttk.Frame(tab_control)
tab_ntp = ttk.Frame(tab_control)
tab_control.add(tab_dns, text='   Pruebas DNS   ')
tab_control.add(tab_ntp, text='   Pruebas NTP   ')
tab_control.pack(expand=1, fill="both")

# --- PESTAÑA DNS ---
frame_top_dns = tk.Frame(tab_dns, pady=10)
frame_top_dns.pack()

tk.Label(frame_top_dns, text="Dominio / Host:").pack(side=tk.LEFT, padx=5)
entry_dns = tk.Entry(frame_top_dns, width=30)
entry_dns.pack(side=tk.LEFT, padx=5)
entry_dns.insert(0, "www.google.com")

btn_dns = tk.Button(frame_top_dns, text="RESOLVER DNS", bg="#2196F3", fg="white", command=resolver_dns)
btn_dns.pack(side=tk.LEFT, padx=10)

# Log DNS (Estilo terminal)
tk.Label(tab_dns, text="Salida / Log:").pack(anchor="w", padx=10)
text_log_dns = tk.Text(tab_dns, height=15, bg="black", fg="#00FF00", font=("Consolas", 10))
text_log_dns.pack(padx=10, pady=(0,10), fill="both", expand=True)


# --- PESTAÑA NTP ---
frame_top_ntp = tk.Frame(tab_ntp, pady=10)
frame_top_ntp.pack()

tk.Label(frame_top_ntp, text="Servidor NTP:").pack(side=tk.LEFT, padx=5)
entry_ntp = tk.Entry(frame_top_ntp, width=30)
entry_ntp.pack(side=tk.LEFT, padx=5)
entry_ntp.insert(0, "pool.ntp.org") # Servidor público estándar

btn_ntp = tk.Button(frame_top_ntp, text="CONSULTAR HORA", bg="#b30000", fg="white", command=consultar_ntp)
btn_ntp.pack(side=tk.LEFT, padx=10)

# Log NTP
tk.Label(tab_ntp, text="Respuesta del Servidor:").pack(anchor="w", padx=10)
text_log_ntp = tk.Text(tab_ntp, height=15, bg="#f0f0f0", fg="black", font=("Consolas", 10))
text_log_ntp.pack(padx=10, pady=(0,10), fill="both", expand=True)

root.mainloop()