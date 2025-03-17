import openai
import wolframalpha

# Configura tus claves de API
openai.api_key = 'tu_clave_de_openai'  # Clave de OpenAI para ChatGPT
wolfram_client = wolframalpha.Client('tu_clave_de_wolframalpha')  # Clave de Wolfram Alpha

# Función para preguntar a ChatGPT
def preguntar_a_chatgpt(pregunta):
    respuesta = openai.Completion.create(
        engine="text-davinci-003",  # Modelo de ChatGPT
        prompt=pregunta,
        max_tokens=150
    )
    return respuesta.choices[0].text.strip()

# Función para preguntar a Wolfram Alpha
def preguntar_a_wolfram(pregunta):
    res = wolfram_client.query(pregunta)
    try:
        return next(res.results).text  # Devuelve el primer resultado
    except StopIteration:
        return "No se encontró una respuesta en Wolfram Alpha."

# Simulación de conversación entre IA
def conversacion_entre_IA(pregunta):
    print(f"Usuario: {pregunta}")

    # Paso 1: ChatGPT responde
    respuesta_chatgpt = preguntar_a_chatgpt(pregunta)
    print(f"ChatGPT: {respuesta_chatgpt}")

    # Paso 2: Wolfram Alpha responde (si es una pregunta matemática)
    if "calcula" in pregunta.lower() or "derivada" in pregunta.lower():
        respuesta_wolfram = preguntar_a_wolfram(pregunta)
        print(f"Wolfram Alpha: {respuesta_wolfram}")

# Ejemplo de uso
pregunta_usuario = "Calcula la derivada de x^2 + 3x + 2 y explícamelo."
conversacion_entre_IA(pregunta_usuario)
