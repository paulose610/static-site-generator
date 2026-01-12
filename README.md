Static Site Generator (Markdown → HTML)

A simple Python-based static site generator that recursively converts Markdown files into HTML using a block-level and inline-level parsing pipeline.

All Markdown content is placed in content/, processed through a structured conversion pipeline, and the generated HTML is output to docs/.

Project Overview

This project implements a two-stage Markdown parsing system:

Block-level processing (paragraphs, lists, headings, etc.)

Inline-level processing (bold, italic, code, links, images)

The design emphasizes clean decomposition, testability, and clear data flow from raw text to HTML output.

Directory Structure
.
├── content/        # Input markdown files (recursively processed)
├── docs/           # Generated HTML output         src/
│   └── tests/      # Unit tests
|   └──helper/      # Core parsing and conversion and pipeline components
├── static/         # Static assets (CSS, images, etc.)
├── template.html   # Base HTML template
├── main_helper.py  # End-to-end generation pipeline
├── main.sh         # Run script
└── README.md

High-Level Architecture
Markdown Files
      ↓
Block Splitting (double newline)
      ↓
Block Classification (Paragragh, Code Block, Quote, Unordered List, Ordered List, Heading)
      ↓
Block → HTML Parent Nodes
      ↓
Line Splitting (newline)
      ↓
Inline Parsing (bold, italic, code, links, images)
      ↓
TextNodes
      ↓
HTML Leaf Nodes
      ↓
Final HTML Output

Markdown Processing Pipeline
1. Input Discovery

All files inside content/ are:

Recursively traversed

Converted from Markdown to HTML

Copied into docs/ with the same directory structure

2. Block-Level Processing

Each Markdown file is split by double newlines into blocks.

Each block is classified into one of six supported block types.

Each block is converted into an HTML Parent Node (no direct content, only children).

3. Line-Level Processing

Each block is further split by single newlines

Each line is processed based on its block characteristics

Each line becomes a parent HTML node, added as children to the block HTML Parent node

4. Inline-Level Processing

Each line is recursively decomposed into inline components using fixed Markdown patterns.

This continues until the line is fully decomposed into TextNodes.


5. Node Conversion

TextNode

Used for clean problem decomposition

Represents the smallest meaningful unit of text

TextNodes are converted into HTML Leaf Nodes

Leaf nodes contain content

No children

Each leaf node is attached to its respective parent node.

Core Components
helper/

Contains:

HTML Node classes

Parent nodes

Child (leaf) nodes

Block-level parsing functions

Inline-level parsing functions

TextNode

A dedicated class used to:

Simplify inline parsing

Separate concerns between parsing and rendering

Enable clean recursion and testing

main_helper.py

Handles file traversal and copying

Orchestrates the full pipeline:

Read → Parse → Convert → Render → Write

Acts as the single entry point for content generation

template.html

Base HTML layout

Injects generated content into a common structure

static/

Contains static assets such as CSS or images

Copied directly to docs/ without modification

Tests

All unit tests are located in:

src/tests/


They validate:

Block classification

Inline parsing

Node generation

Edge cases in Markdown handling

How to Run the Project
1. Clone the Repository
git clone <repository-url>
cd <repository-name>

2. Prepare Content

Sample content already exists in:

content/

static/

You may:

Modify it

Replace it

Or use it as-is for testing

3. Run Locally

From the project root:

./main.sh


Generated HTML will appear in the docs/ directory.