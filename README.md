# Static Site Generator (Markdown → HTML)

A simple Python-based static site generator that recursively converts Markdown files into HTML using a block-level and inline-level parsing pipeline.

All Markdown content is placed in `content/`, processed through a structured conversion pipeline, and the generated HTML is output to `docs/`.

---

## Project Overview

This project implements a two-stage Markdown parsing system:

- **Block-level processing**: Handles structural elements like paragraphs, lists, and headings.
- **Inline-level processing**: Handles text formatting like bold, italic, code, links, and images.

The design emphasizes clean decomposition, testability, and clear data flow from raw text to HTML output.

---

## Directory Structure

```text
.
├── content/           # Input markdown files (recursively processed)
├── docs/              # Generated HTML output
├── src/
│   ├── tests/         # Unit tests
│   └── helper/        # Core parsing, conversion, and pipeline components
├── static/            # Static assets (CSS, images, etc.)
├── template.html      # Base HTML template
├── main_helper.py     # End-to-end generation pipeline
├── main.sh            # Run script
└── README.md
```

## High-Level Architecture

- Markdown Files
- Block Splitting: Separated by double newlines
- Block Classification  
  (Paragraph, Code Block, Quote, Unordered List, Ordered List, Heading)
- Block → HTML Parent Nodes
- Line Splitting: Separated by single newlines
- Inline Parsing  
  (bold, italic, code, links, images)
- TextNodes
- HTML Leaf Nodes
- Final HTML Output

---

## Markdown Processing Pipeline

### 1. Input Discovery

All files inside `content/` are:

- Recursively traversed
- Converted from Markdown to HTML
- Copied into `docs/` while maintaining the original directory structure

---

### 2. Block-Level Processing

- Each Markdown file is split by double newlines into blocks
- Each block is classified into one of six supported block types
- Each block is converted into an HTML Parent Node  
  (no direct content, only children)

---

### 3. Line-Level Processing

- Each block is further split by single newlines
- Each line is processed based on its block characteristics
- Each line becomes a parent HTML node, added as a child to the block HTML Parent node

---

### 4. Inline-Level Processing

- Each line is recursively decomposed into inline components using fixed Markdown patterns
- This continues until the line is fully decomposed into TextNodes

---

### 5. Node Conversion

- **TextNode**: Used for clean problem decomposition; represents the smallest meaningful unit of text
- **HTML Leaf Nodes**: Contain content but no children
- Each leaf node is attached to its respective parent node

---

## Core Components

### `helper/`

Contains the primary logic for:

- HTML Node classes: Parent and Leaf node definitions
- Parsing functions: Modular block and inline parsing logic

---

### `TextNode`

A dedicated class used to:

- Simplify inline parsing
- Separate concerns between parsing and rendering
- Enable clean recursion and testing

---

### `main_helper.py`

The orchestrator of the generation pipeline:

- Handles file traversal and directory copying
- Manages the Read → Parse → Convert → Render → Write flow
- Acts as the single entry point for the application

---

### `template.html`

Base HTML layout used to inject generated content into a consistent design.

---

### `static/`

Contains static assets like CSS or images. These are copied directly to `docs/` without modification.

---

### Tests

Located in `src/tests/`, these validate:

- Block classification accuracy
- Inline parsing logic (regex patterns)
- Correct nesting of HTML nodes

---

## How to Run the Project

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Prepare Content

Sample content is available in `content/` and `static/`. You can modify these files or replace them with your own.

---

### 3. Run Locally

Execute the script from the root directory:

```bash
chmod +x main.sh
./main.sh
```