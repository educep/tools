
# Colección de Herramientas Excel

Una colección de herramientas y utilidades Excel construidas con VBA para mejorar la productividad y automatizar tareas comunes.

## Herramientas Actuales

### 1. Integración ChatGPT
Un cliente ChatGPT integrado en Excel que permite:
- Realizar consultas directamente desde celdas de Excel
- Incluir rangos de celdas como contexto en tus prompts
- Usar modos síncronos (fórmula de celda) y asíncronos (macro)
- Obtener respuestas en español de un asistente experto en Excel/VBA

#### Configuración
1. En la hoja llamada "API" proveer:
   - Tu clave API de OpenAI en la celda B1
   - El nombre del modelo (ej. "gpt-4") en la celda B2

2. En la una hoja llamada "Prompt":
   - A3 se usa para tu prompt de entrada
   - A5 mostrará la respuesta

#### Uso
Hay dos formas de usar la integración con ChatGPT:

1. **Como Función de Celda:**
```excel
=CallChatGPT("Tu prompt aquí")
=CallChatGPT(A1)  ' Referencia a una celda que contiene el prompt
=CallChatGPT(A1, B1:C10)  ' Incluye un rango de datos como contexto
```

2. **Como Macro:**
- Escribe tu prompt en la celda A3 de la hoja "Prompt"
- Ejecuta la macro `GetChatGPTResponse` cliqueando en el botón enviar pregunta.
- Opcionalmente selecciona un rango de datos para incluir como contexto
- La respuesta aparecerá en la celda A5

## Futuras Herramientas
Este repositorio se actualizará con herramientas y utilidades Excel adicionales conforme se desarrollen.

## Requisitos
- Excel con VBA habilitado
- Habilitar archivos Excel con Macros digitalmente firmadas
- Referencias VBA requeridas:
  - Microsoft XML, v6.0
  - Microsoft Scripting Runtime
- Clave API de OpenAI para la integración con ChatGPT

## Instalación
1. Habilitar VBA en Excel para Macros digitalmente firmadas

En el caso en que debas replicar el archivo:
1. Importar los módulos en tu libro de Excel
2. Agregar las referencias requeridas en el editor VBA (Herramientas → Referencias)
3. Configurar los ajustes específicos de la herramienta como se describe en la sección de configuración

## Contribuciones
¡Siéntete libre de enviar problemas y solicitudes de mejora!

## Licencia
Licencia MIT

## Contacto
 - solutions@datoscout.ec
 - contact@analitika.fr

---
*Nota: Mantén tus claves API seguras y nunca las subas al control de versiones.*

