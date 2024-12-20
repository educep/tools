
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
1. Crear una hoja llamada "API" con:
   - Tu clave API de OpenAI en la celda B1
   - El nombre del modelo (ej. "gpt-4") en la celda B2

2. Crear una hoja llamada "Prompt" donde:
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
- Ejecuta la macro `GetChatGPTResponse`
- Opcionalmente selecciona un rango de datos para incluir como contexto
- La respuesta aparecerá en la celda A5

## Futuras Herramientas
Este repositorio se actualizará con herramientas y utilidades Excel adicionales conforme se desarrollen.

## Requisitos
- Excel con VBA habilitado
- Referencias VBA requeridas:
  - Microsoft XML, v6.0
  - Microsoft Scripting Runtime
- Clave API de OpenAI para la integración con ChatGPT

## Instalación
1. Habilitar VBA en Excel
2. Importar los módulos en tu libro de Excel
3. Agregar las referencias requeridas en el editor VBA (Herramientas → Referencias)
4. Configurar los ajustes específicos de la herramienta como se describe en la sección de configuración

## Contribuciones
¡Siéntete libre de enviar problemas y solicitudes de mejora!

## Licencia
Licencia MIT

## Contacto
 - solutions@datoscout.ec
 - contact@analitika.fr

---
*Nota: Mantén tus claves API seguras y nunca las subas al control de versiones.*


---

# Excel Tools Collection

A collection of useful Excel tools and utilities built with VBA to enhance productivity and automate common tasks.

## Current Tools

### 1. ChatGPT Integration
An Excel-integrated ChatGPT client that allows you to:
- Make queries directly from Excel cells
- Include cell ranges as context in your prompts
- Use both synchronous (cell formula) and asynchronous (macro) modes
- Get responses in Spanish from an Excel/VBA expert assistant

#### Setup
1. Create a sheet named "API" with:
   - Your OpenAI API key in cell B1
   - The model name (e.g., "gpt-4") in cell B2

2. Create a sheet named "Prompt" where:
   - A3 is used for your input prompt
   - A5 will display the response

#### Usage
There are two ways to use the ChatGPT integration:

1. **As a Cell Function:**
```excel
=CallChatGPT("Your prompt here")
=CallChatGPT(A1)  ' Reference a cell containing the prompt
=CallChatGPT(A1, B1:C10)  ' Include a data range for context
```

2. **As a Macro:**
- Type your prompt in cell A3 of the "Prompt" sheet
- Run the `GetChatGPTResponse` macro
- Optionally select a range of data to include as context
- The response will appear in cell A5

## Future Tools
This repository will be updated with additional Excel tools and utilities as they are developed.

## Requirements
- Excel with VBA enabled
- Required VBA References:
  - Microsoft XML, v6.0
  - Microsoft Scripting Runtime
- OpenAI API key for ChatGPT integration

## Installation
1. Enable VBA in Excel
2. Import the modules into your Excel workbook
3. Add the required references in the VBA editor (Tools → References)
4. Configure the tool-specific settings as described in each tool's setup section

## Contributing
Feel free to submit issues and enhancement requests!

## License
MIT License

## Contact
 - solutions@datoscout.ec
 - contact@analitika.fr

---
*Note: Keep your API keys secure and never commit them to version control.*
