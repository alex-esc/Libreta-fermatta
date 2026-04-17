# Automatización

En la versión 4 se comenzó a transcribir de texto de puño y letra a texto plano digital de manera manual. Este es un proceso manual muy laborioso. La transcripción se complica por los siguientes factores:

* Letra difícil de leer, mala caligrafía
* Texto en Español en su mayoría, pero con tecnicismos en Ingles
* Texto de la libreta esta entre mezclado con imágenes, gráficos y partituras musicales
* Todos los elementos (texto, partitura, gráficos, tablas) no siempre están escritos de derecha a izquierda, arriba-abajo
* De vez en cuando el texto esta interrumpido por tangentes que se mencionaron en clase

Estos factores complican la transcripción manual, pero hacen el OCR imposible! Muchos modelos de OCR son buenos para reconocer letra escrita a mano, pero tienen dificultades con texto en español - y al mezclar idiomas esto resulta mas complicado para programas de OCR.

Incluso, si un buen programa de OCR para este caso existiera y fuera capaz de entender mi mala caligrafía, tendría que entender texto entremezclado con notación musical, tablas y gráficos!

Muchas paginas de mis libretas están acomodadas en columnas que cambian libremente. A veces hay dos columnas por pagina. A veces una sola pagina tiene 2 columnas, luego 3 comunas y luego 1 columna, todo en la misma pagina. Entonces si un programa OCR lee el texto de derecha a izquierda estaría combinando varios párrafos. 

Por estas razones decidí transcribir la libreta de manera manual.

El proceso de transcribir manualmente una pagina se puede dividir en los siguientes pasos:

* Transcribir texto
* Crear ecuaciones etilo LaTeX*
* Crear gráficos / flechas / imágenes / tablas*
* Transcribir notación musical*
* Acomodar en columnas como en la libreta original

Los pasos con asteriscos "*" no son necesarios en todas las paginas. Una pagina tiene como mínimo texto que trascribir y formato / columnas por acomodar. Dependiendo del tema se necesitaran gráficos, notación musical o ecuaciones.

Cuando inicie la V4 en 16 Noviembre 2025 hice pruebas para averiguar cuanto tiempo me tomaría transcribir manualmente una sola pagina (de 317 totales). Averigüé en mis pruebas que puedo hacer al rededor de una hoja por día. Esto incluye transcripción de texto, notación musical, formato y columnas. A ese ritmo me tomaría al rededor de **un año ininterrumpido** en transcribir toda las libretas.

Unos días después (19 Nov.) empecé a probar OCR, pero por las complicaciones del material no me dio buenos resultados. También probé varios modelos de inteligencia especial, incluyendo variantes de ChatGPT, DeepSeek y Gemini.

El mas efectivo con mi caligrafía fue Gemini 2.5 Flash Image (Nano Banana), que fue actualizado solo un mes atrás. En Google AI studio use estas preferencias para optimizar la transcripción:

```
Temperature = 0
System prompt = "Transcribe el texto de esta imagen a solo texto, no resumas nada, dame el texto literal"
```

Con esto solo tengo que darle la imagen de la pagina al modelo y me entregaba el texto transcrito con muy buen margen de error (aprox menos de 20%). Para facilitar la transcripción con Nano Banana desarrolle este proceso:

* Tomar screenshot de solo una porción de una pagina (no la pagina entera)
* Importar screenshot a paint (editor de fotos) para borrar palabras y ecuaciones tachadas, borrar fragmentos del screenshot que hablan de otro tema
* Copiar imagen editada
* Pegar imagen en AI studio
* Esperar a que Nano Banana de resultado (10 segundos a 3 minutos)
* Copiar el texto plano que genero Nano Banana
* Cambiar apps a mi editor de texto (ALT + TAB)
* Pegar texto transcrito
* Crear ecuaciones etilo LaTeX*
* Crear gráficos / flechas / imágenes / tablas*
* Transcribir notación musical*
* Acomodar en columnas como en la libreta original

Esto me ayuda a no transcribir manualmente, pero agrega muchos pasos al proceso. A pesar de tener mas pasos, la transcripción es MUY rápida. Con este proceso logre transcribir 10-15 paginas por día. A esta velocidad podría terminar la transcripción con un mes de días de trabajo ininterrumpido.

Por mi horario de trabajo podría invertir 1 a 2 días de trabajo a este proyecto por semana. Lo que significa que realisticamente me tomaría 7 meses en terminar la transcripción. Si tomamos en cuenta vacaciones y "burnout" regresamos a un estimado de un año de trabajo.

Para el 28 Noviembre de 2025 logre transcribir un total de 75 paginas con ayuda de Nano Banana, que aproxima 25% de la libreta transcrita.

Por razones familiares todo diciembre 2025 y enero 2026 no pude continuar con el proyecto. Para febrero retome mis estudios de maestría, inicie un nuevo trabajo y empecé a grabar un disco. El proyecto de mi libreta se convirtió en mi ultima prioridad.

El primero de Abril 2026 Google lanzo "Gemma 4", un nuevo modelo de LLM que puedes correr localmente en tu computadora! Casualmente el mismo día despego la misión Artemis 2 y comenzó la grabación de voces finales del disco. Durante la transmisión de Artemis y la grabación solo podía pensar en las posibilidades de Gemma 4 ... Tal vez una LLM local podría servir para automatizar muca parte del proceso.

Para el 3 de Abril pude empezar a investigar Gemma 4. Aprendí a usarlo en LM studio e inmediatamente empecé a trabajar en como automatizar el proceso. Para el día siguiente hice un script de python para automatizar el proceso! 

```
import os
import base64
from openai import OpenAI

# --- SET YOUR FOLDERS HERE ---
input_folder = r"C:\Users\YOUR_PATH_HERE\input"
output_folder = r"C:\Users\YOUR_PATH_HERE\input"

# Point the program to LM Studio's Local Server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

def encode_image(image_path):
    """Converts the image into a format the AI can read."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Create output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Get a list of all images in the folder
valid_extensions = ('.png', '.jpg', '.jpeg')
files = [f for f in os.listdir(input_folder) if f.lower().endswith(valid_extensions)]

print(f"Found {len(files)} images. Starting transcription...")

# Loop through every image file
for filename in files:
    print(f"\nProcessing: {filename}...")
    image_path = os.path.join(input_folder, filename)
    
    # 1. Convert image to base64
    base64_image = encode_image(image_path)
    
    # 2. Send to LM Studio
    try:
        response = client.chat.completions.create(
            model="local-model", # LM Studio automatically uses whatever model you have loaded
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text", 
                            "text": "Transcribe el texto de esta imagen a solo texto, no resumas nada, dame el texto literal"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            temperature=0.0, # Keeps the AI focused and less "creative"
        )
        
        # 3. Get the text the AI replied with
        transcription = response.choices[0].message.content
        
        # 4. Save to a text file with the same name
        name_without_extension = os.path.splitext(filename)[0]
        text_filename = f"{name_without_extension}.txt"
        text_filepath = os.path.join(output_folder, text_filename)
        
        with open(text_filepath, "w", encoding="utf-8") as text_file:
            text_file.write(transcription)
            
        print(f"Success! Saved to {text_filename}")

    except Exception as e:
        print(f"Error processing {filename}: {e}")

print("\nAll done! You can now turn off the server in LM Studio.")
```

El script necesita un folder "input" y "output". En "Input" puse cada pagina del PDF V2 en formato de imagen. El siguiente paso es cargar Gemma 4 en LM studio y encender el servidor.

En LM studio use estas preferencias (con el GUI)

```
Temperature = 0
System prompt =
	No uses latex para equaciones, usa texto plano

	todos los simbolos representalos con texto plano. Ejemplo flechas, usa tetxo plano para todo, nada de formato espacial
Enable Thinking = FALSE
Limit Responce Lenght = TRUE
Max Responce Lenght (tokens) = 1024
```

En pruebas encontré que Gemma 4 entregaba ecuaciones en texto plano, pero escritas en LaTeX, esto agregaría un paso adicional de re interpretar texto plano como LaTeX, para evitar este paso especifique en el system prompt que use formato de ecuaciones en texto plano.

También apague el modo "pensante" por que en pruebas inspeccione el proceso de pensamiento y el dialogo interno de Gemma era algo así:

> Debo escribir todo literal, sin modificar el texto, la primera palabra dice "acbkuvald" pero esto no tiene sentido, tal vez quiso decir "abracadabra" entonces escribiré eso en texto plano.

Esto resultaba en que palabras con suficientemente mala caligrafía eran erróneamente corregidas. Esto luego conlleva a modificar el resto del texto. Luego de "corregir" una palabra, el pensamiento de Gemma decía algo como esto:

> El texto dice "Do, Re, Mi, Fa, Sol" pero eso no tiene sentido con la palabra anterior "abracadabra", probablemente este sea un texto de magia entonces el usuario quiso decir "Dos retratos del sol en la magia, abracadabra" entonces escribire eso en texto plano.

El modelo de pensamiento creaba un juego de teléfono descompuesto y si hay errores de transcripción el texto perdía sentido poco a poco dependiendo de que tan al inicio de la hoja se cometió el error. Por eso decidí apagar el modo "thinking".

Por ultimo, en el periodo de pruebas encontré que el output en raras ocasiones genera ciclos infinitos de texto donde un carácter o una palabra se repite infinitamente. Por lo tanto nunca se termina de procesar la imagen actual, por lo tanto se atora el proceso y nunca se avanzara a la siguiente imagen.

Mediante pruebas encontré que la pagina promedio es de entre 35 y 40 renglones. Y en promedio eso necesita 500 tokens. Entonces estime que ninguna pagina debe superar los 1,000 tokens. Redondeando a potencias de 2 configure el limite de tokens en 1,024.

Con los problemas básicos resueltos ejecute el script toda la noche del 11 de abril, para el dia siguiente el modelo transcribió toda la libreta!

Según mis estimaciones el modelo (corriendo solo en el CPU, tamaño es de 18 GB) transcribe a una velocidad de 55 paginas por hora. Aprox una hoja por minuto! 
 
* Transcribir texto ✅
* Crear ecuaciones etilo LaTeX* ✅
* Crear gráficos / flechas / imágenes / tablas*
* Transcribir notación musical*
* Acomodar en columnas como en la libreta original

Esto significa que los primeros dos pasos del proceso fueron completamente automatizados! Y tomo solamente 5 días en lugar de el año entero!

De todas las hojas procesadas por gemma4, solo 8 tuvieron un error donde un carácter o palabra se repetía indefinidamente. Pero gracias al limite de tokens, el txt fue cortado a los 65-100 renglones y el script pudo continuar procesando las siguientes imágenes. 

Pero existe un problema, ahora tengo cientos de archivos TXT y cada uno con el texto correspondiente a cada pagina. Tendría que manualmente copiar y pegar el texto en mi editor de texto. Explore automatizar el proceso de copy paste - ear todo el texto, pero calcule que el trabajo manual tomaría 2 días de trabajo. Y que automatizar el proceso seria mucho mas complicado que la transcripción en si, por que necesitaría de varios agentes que interactúan y toman control de la computadora. Estime que me tomaría una o dos emanas aromatizar ese proceso. Por lo tanto seria mas eficiente hacer el copy paste manualmente. Y eso hice.

En Versiones.md registre el proceso:

* __Ver 4__ actualmente en progreso... 
	- Transcribiendo imágenes a texto manualmente: (305 pág totales)
		* Progreso manual   2%, 16 Noviembre 2025
		* Progreso manual   5%, 18 Noviembre 2025
		* Progreso manual 13%, 19 Noviembre 2025
		* Progreso manual 20%, 24 Noviembre 2025
		* Progreso manual 25%, 28 Noviembre 2025
	- Transcribiendo imágenes a texto automáticamente: 
		* Creación de Script de automatización,  3-4 Abril 2026
		* Test y debugging de Script,                     10 Abril 2026
		* Progreso automatizado  36%,  11 Abril 2026
		* Progreso automatizado 100%, 12 Abril 2026
	- Implementación de transcripción a documento: 
		* Progreso manual     24%, 13 Abril 2026
		* Progreso manual     77%, 14 Abril 2026
		* Progreso manual   100%, 15 Abril 2026
		
Con "Implementación de transcripción a documento" me refiero a copiar y pegar cada .txt en el documento de la versión 4. Me tomo 3 días, de los 2 dias estimados, pero aun así fue un proceso sencillo y rápido (comparado con el año de trabajo que tomaría la transcripción manual o transcripción con Nano Banana).

* Transcribir texto ✅
* Crear ecuaciones etilo LaTeX* ✅
* Corrección Manual
* Crear gráficos / flechas / imágenes / tablas*
* Transcribir notación musical*
* Acomodar en columnas como en la libreta original

Este método necesita un paso adicional, la correccional manual. Gemini 4 es bueno, mejor que Nano Banana. Pero no es perfecto. Bajo is pruebas encontré que en la hoja de mi libreta promedio Gemini 4 cometería 2-5 errores (palabras equivocadas). Esto es un muy bajo margen de error! Pero la corrección manual es necesaria de todas formas!