import tkinter as tk
from tkinter import messagebox
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading

def enviar_correo():
    # Deshabilitar el botón mientras se envía para evitar clics dobles
    btn_send.config(state=tk.DISABLED)
    
    # 1. Obtener datos de la interfaz
    host = entry_host.get()
    port = entry_port.get()
    user = entry_user.get()
    password = entry_pass.get()
    sender = entry_from.get()
    receiver = entry_to.get()
    subject = entry_subject.get()
    html_content = text_body.get("1.0", tk.END) # Obtener todo el contenido HTML

    # 2. Escribir en el log
    log_message("[INFO] Preparando envío...")

    # Función interna para ejecutar en segundo plano (hilo)
    def thread_task():
        try:
            # Crear el objeto del mensaje
            msg = MIMEMultipart("alternative")
            msg['Subject'] = subject
            msg['From'] = sender
            msg['To'] = receiver

            # Adjuntar el cuerpo en HTML
            part = MIMEText(html_content, "html")
            msg.attach(part)

            log_message(f"[INFO] Conectando a {host}:{port}...")

            # 3. Conexión SMTP
            # Mailtrap funciona mejor con starttls en el puerto 2525 o 587
            with smtplib.SMTP(host, int(port)) as server:
                server.ehlo()
                log_message("[INFO] EHLO")
                
                # Iniciamos STARTLS aunque no haya checkbox, es necesario para Mailtrap
                server.starttls() 
                server.ehlo()
                
                log_message("[INFO] LOGIN...")
                server.login(user, password)
                
                log_message("[INFO] SEND...")
                server.sendmail(sender, receiver, msg.as_string())

            log_message("[OK] Mensaje enviado. Revisa el Inbox de Mailtrap.")
            messagebox.showinfo("Éxito", "Correo enviado correctamente a Mailtrap")

        except Exception as e:
            log_message(f"[ERROR] Fallo en el envío: {str(e)}")
            messagebox.showerror("Error", f"Fallo al enviar: {str(e)}")
        
        finally:
            # Volver a habilitar el botón "Enviar"
            btn_send.config(state=tk.NORMAL)

    # Iniciar el proceso en un hilo separado
    threading.Thread(target=thread_task).start()

# Función auxiliar para escribir en la consola de log (lado derecho)
def log_message(msg):
    text_log.config(state=tk.NORMAL)
    text_log.insert(tk.END, msg + "\n")
    text_log.see(tk.END) # Auto-scroll al final
    text_log.config(state=tk.DISABLED)

# Función para limpiar el log
def limpiar_log():
    text_log.config(state=tk.NORMAL)
    text_log.delete("1.0", tk.END)
    text_log.config(state=tk.DISABLED)

# --- Configuración de la Ventana Principal (GUI) ---
root = tk.Tk()
root.title("Envío SMTP/STARTTLS (Mailtrap / Sandbox)")
root.geometry("950x600")

# Frame Superior: Configuración SMTP
frame_config = tk.LabelFrame(root, text="Configuración SMTP")
frame_config.pack(padx=10, pady=5, fill="x")

# Fila 0
tk.Label(frame_config, text="HOST").grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_host = tk.Entry(frame_config, width=25)
entry_host.grid(row=0, column=1, padx=5, pady=5)
entry_host.insert(0, "sandbox.smtp.mailtrap.io")  # Tu host de la captura

tk.Label(frame_config, text="PORT").grid(row=0, column=2, padx=5, pady=5, sticky="e")
entry_port = tk.Entry(frame_config, width=10)
entry_port.grid(row=0, column=3, padx=5, pady=5)
entry_port.insert(0, "2525") # Puerto estándar para Mailtrap

# Fila 1
tk.Label(frame_config, text="USERNAME").grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_user = tk.Entry(frame_config, width=35)
entry_user.grid(row=1, column=1, padx=5, pady=5, columnspan=2, sticky="w")
entry_user.insert(0, "73e217a6aa136c") # Tu usuario de la captura

tk.Label(frame_config, text="PASSWORD").grid(row=1, column=2, padx=5, pady=5, sticky="e")
entry_pass = tk.Entry(frame_config, show="*", width=20)
entry_pass.grid(row=1, column=3, padx=5, pady=5)

# Fila 2
tk.Label(frame_config, text="FROM").grid(row=2, column=0, padx=5, pady=5, sticky="e")
entry_from = tk.Entry(frame_config, width=35)
entry_from.grid(row=2, column=1, padx=5, pady=5)
entry_from.insert(0, "alumno@prueba.com")

tk.Label(frame_config, text="TO").grid(row=2, column=2, padx=5, pady=5, sticky="e")
entry_to = tk.Entry(frame_config, width=35)
entry_to.grid(row=2, column=3, padx=5, pady=5)
entry_to.insert(0, "profesor@ejemplo.com")

# Fila 3
tk.Label(frame_config, text="SUBJECT").grid(row=3, column=0, padx=5, pady=5, sticky="e")
entry_subject = tk.Entry(frame_config, width=70)
entry_subject.grid(row=3, column=1, columnspan=3, padx=5, pady=5, sticky="w")
entry_subject.insert(0, "Prueba de envío SMTP con Python y Tkinter")

# --- Paneles Centrales (Texto HTML y Log) ---
frame_middle = tk.Frame(root)
frame_middle.pack(padx=10, pady=5, fill="both", expand=True)

# Panel Izquierdo: Cuerpo HTML
frame_body = tk.LabelFrame(frame_middle, text="Cuerpo del correo (HTML)")
frame_body.pack(side=tk.LEFT, fill="both", expand=True, padx=(0, 5))

text_body = tk.Text(frame_body, height=15, width=40)
text_body.pack(padx=5, pady=5, fill="both", expand=True)
# HTML de ejemplo
html_template = """<html>
<body>
  <h2>Hola Mailtrap!</h2>
  <p>Este es un <b>correo de prueba</b> enviado desde mi aplicación Python.</p>
  <p>Fecha: <i>Hoy</i></p>
</body>
</html>"""
text_body.insert(tk.END, html_template)

# Panel Derecho: Log
frame_log = tk.LabelFrame(frame_middle, text="Salida / Log")
frame_log.pack(side=tk.RIGHT, fill="both", expand=True, padx=(5, 0))

text_log = tk.Text(frame_log, height=15, width=40, state=tk.DISABLED, bg="#f0f0f0")
text_log.pack(padx=5, pady=5, fill="both", expand=True)

# --- Botones Inferiores ---
frame_buttons = tk.Frame(root)
frame_buttons.pack(side=tk.BOTTOM, fill="x", padx=10, pady=10)

btn_send = tk.Button(frame_buttons, text="ENVIAR", bg="#b30000", fg="white", font=("Arial", 10, "bold"), command=enviar_correo)
btn_send.pack(side=tk.RIGHT, padx=5)

btn_clean = tk.Button(frame_buttons, text="Limpiar log", command=limpiar_log)
btn_clean.pack(side=tk.RIGHT, padx=5)

# Iniciar la aplicación
root.mainloop()