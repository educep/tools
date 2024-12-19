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
