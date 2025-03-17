import openai
import wolframalpha
import tkinter as tk
from tkinter import simpledialog, messagebox
import turtle
from authlib.integrations.requests_client import OAuth2Session
from google.oauth2 import service_account
import google.auth.transport.requests

# Función para autenticar al usuario
def autenticar_usuario(usuario, contrasena, contrasena_maestra):
    if contrasena == contrasena_maestra:
        messagebox.showinfo("Autenticación", "Autenticación exitosa.")
        return True
    else:
        messagebox.showerror("Autenticación", "Autenticación fallida.")
        return False

# Configurar claves de API
def configurar_claves(oauth_tokens):
    openai.api_key = oauth_tokens['openai']
    wolfram_client = wolframalpha.Client(oauth_tokens['wolfram'])
    credentials = service_account.Credentials.from_service_account_file(
        oauth_tokens['google'], scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    google_auth_req = google.auth.transport.requests.Request()
    credentials.refresh(google_auth_req)
    return credentials

# Preguntar a ChatGPT
def preguntar_a_chatgpt(pregunta):
    respuesta = openai.Completion.create(
        engine="text-davinci-003",
        prompt=pregunta,
        max_tokens=150
    )
    return respuesta.choices[0].text.strip()

# Preguntar a Wolfram Alpha
def preguntar_a_wolfram(pregunta):
    res = wolfram_client.query(pregunta)
    try:
        return next(res.results).text
    except StopIteration:
        return "No se encontró una respuesta en Wolfram Alpha."

# Generar imagen con DALL-E
def generar_imagen(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    return response['data'][0]['url']

# Simulación de conversación entre IA
def conversacion_entre_IA(pregunta):
    respuesta_chatgpt = preguntar_a_chatgpt(pregunta)
    if "calcula" in pregunta.lower() or "derivada" in pregunta.lower():
        respuesta_wolfram = preguntar_a_wolfram(pregunta)
    else:
        respuesta_wolfram = respuesta_chatgpt
    url_imagen = generar_imagen(respuesta_wolfram)
    return respuesta_chatgpt, respuesta_wolfram, url_imagen

# Interfaz gráfica
def iniciar_interfaz():
    root = tk.Tk()
    root.title("Consultas IA")

    tk.Label(root, text="Usuario:").grid(row=0, column=0)
    usuario_entry = tk.Entry(root)
    usuario_entry.grid(row=0, column=1)

    tk.Label(root, text="Contraseña:").grid(row=1, column=0)
    contrasena_entry = tk.Entry(root, show="*")
    contrasena_entry.grid(row=1, column=1)

    def autenticar_y_consultar():
        usuario = usuario_entry.get()
        contrasena = contrasena_entry.get()
        if autenticar_usuario(usuario, contrasena, "tu_contraseña_maestra"):
            pregunta = simpledialog.askstring("Pregunta", "¿Qué quieres preguntar?")
            if pregunta:
                oauth_tokens = {
                    'openai': simpledialog.askstring("OpenAI Key", "Introduce tu clave de OpenAI:"),
                    'wolfram': simpledialog.askstring("Wolfram Key", "Introduce tu clave de Wolfram Alpha:"),
                    'google': simpledialog.askstring("Google Credentials Path", "Introduce la ruta de tus credenciales de Google:")
                }
                configurar_claves(oauth_tokens)
                resp_chatgpt, resp_wolfram, url_imagen = conversacion_entre_IA(pregunta)
                messagebox.showinfo("Respuesta ChatGPT", resp_chatgpt)
                messagebox.showinfo("Respuesta Wolfram Alpha", resp_wolfram)
                messagebox.showinfo("Imagen generada", url_imagen)

    tk.Button(root, text="Autenticar y Consultar", command=autenticar_y_consultar).grid(row=2, column=0, columnspan=2)

    root.mainloop()

if __name__ == "__main__":
    iniciar_interfaz()