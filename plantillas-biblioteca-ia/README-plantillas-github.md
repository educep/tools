# 📚 Plantillas — Biblioteca Personal con IA y Obsidian

Plantillas y prompts para construir tu propia biblioteca de conocimiento organizada, navegable en grafo, y mantenida automáticamente con Claude (Cowork o Claude chat + Desktop Commander).

> Creado como material complementario del artículo **"Cómo organizar tu biblioteca personal de libros con IA y Obsidian"** en [analitika.fr](https://analitika.fr)

---

## ¿Qué hay aquí?

| Archivo | Para qué sirve |
|---------|----------------|
| `plantilla-index.md` | El índice maestro de tu biblioteca — punto de entrada del vault en Obsidian |
| `plantilla-topic-moc.md` | Un hub de tema (Map of Content) — conecta libros de la misma área |
| `plantilla-book-note.md` | Una ficha de libro — con metadatos YAML completos para el grafo |
| `prompt-agregar-libros.txt` | Los prompts listos para darle a Claude — 3 casos de uso cubiertos |

---

## Cómo usar estas plantillas

### Opción A — Dejar que Claude lo haga todo (recomendado)

1. Crea tu carpeta raíz y pon tus PDFs dentro sin renombrarlos
2. Abre Cowork (o Claude chat + Desktop Commander) y selecciona la carpeta
3. Copia el prompt de **"Configuración inicial"** del archivo `prompt-agregar-libros.txt`
4. Claude crea toda la estructura, las notas, y el índice por ti

### Opción B — Configurar manualmente

1. Copia `plantilla-index.md` → renómbralo `00 - INDEX.md` → ponlo en `_vault/`
2. Por cada tema, copia `plantilla-topic-moc.md` → renómbralo `NN - Nombre del Tema.md` → ponlo en `_vault/Topics/`
3. Por cada libro, copia `plantilla-book-note.md` → renómbralo `Título (Autor).md` → ponlo en `_vault/Books/`
4. Abre la carpeta `_vault/` como vault en Obsidian

---

## Convención de nombres para los archivos

Todos los PDFs y EPUBs siguen este formato:

```
YYYY [Autor1~Autor2] Título Completo del Libro.pdf
```

Ejemplos:
```
2024 [Iusztin~Labonne] LLM Engineer's Handbook.pdf
2022 [Raschka~Liu~Mirjalili] Machine Learning with PyTorch and Scikit-Learn.epub
2025 [Auffarth~Kuligin] Generative AI with LangChain.pdf
```

Los archivos se ordenan automáticamente por año en el explorador, y es imposible tener duplicados con el mismo nombre.

---

## Estructura de carpetas resultante

```
📁 Mi Biblioteca/
│
├── 📁 01 - Fundamentos/
├── 📁 02 - Machine Learning/
│   └── 2022 [Raschka~Liu~Mirjalili] Machine Learning with PyTorch.pdf
├── 📁 03 - Deep Learning/
│
└── 📁 _vault/                ← abrir esto como vault en Obsidian
    ├── 📄 00 - INDEX.md
    ├── 📁 Books/
    │   └── 📄 Título del Libro (Autor).md
    └── 📁 Topics/
        └── 📄 NN - Nombre del Tema.md
```

---

## Grafo en Obsidian

Abre **Graph View** (`Ctrl+P` → "Open graph view") y configura grupos por tema para colorear los nodos:

```
path:"Topics"                        → amarillo  (hubs de tema)
"[[02 - Machine Learning]]"          → azul
"[[03 - Deep Learning]]"             → naranja
"[[05 - Large Language Models]]"     → rojo
"[[07 - AI Agents & MLOps]]"         → morado
```

---

## Requisitos

- [Obsidian](https://obsidian.md) — gratuito, sin cuenta requerida
- Acceso a Claude con archivos locales, ya sea via:
  - **Cowork** — app de escritorio de Anthropic *(recomendado)*
  - **Claude chat + [Desktop Commander MCP](https://github.com/wonderwhy-er/DesktopCommanderMCP)** — alternativa gratuita

> ⚠️ Si usas Cowork y tienes Desktop Commander instalado, desactívalo en **Configuración → Conectores** antes de trabajar para evitar conflictos.

---

## Licencia

MIT — usa, adapta, y comparte libremente.
