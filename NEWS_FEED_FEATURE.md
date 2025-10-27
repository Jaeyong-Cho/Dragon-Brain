# News Feed Feature

## Overview
The GUI has been updated to display related sections in a scrollable news feed format, similar to social media feeds. This eliminates the need to click on individual files and provides an intuitive way to browse through all related content.

## Key Features

### 1. **SNS-Style News Feed**
- All related sections are displayed in a single scrollable feed
- No need to click on files to view content
- Automatic sorting by similarity score (highest first)

### 2. **Full Content Display**
- Shows complete section content without truncation
- No text size limits - scroll to read everything
- Full markdown rendering with proper formatting

### 3. **Markdown Rendering**
The feed properly renders:
- **Headers** (H1, H2, H3)
- **Bold** and *italic* text
- `Inline code` and code blocks
- Lists (ordered and unordered)
- Blockquotes
- Tables (if markdown library is installed)

### 4. **Visual Design**
- Card-based layout with shadows and borders
- Color-coded similarity badges:
  - 🟢 **Green** (70%+): High similarity
  - 🟠 **Orange** (50-70%): Medium similarity
  - 🔴 **Red** (<50%): Low similarity
- File name and section headers clearly displayed
- Keyword tags for quick reference

### 5. **Smart Layout**
- Left panel: Target file content (editable)
- Right panel: News feed with all related sections
- 40/60 split ratio optimized for reading

## How to Use

1. **Select Target File**: Choose the markdown file you want to analyze
2. **Select Comparison Files**: Choose files or directory to compare against
3. **Calculate Similarity**: Click the button to analyze
4. **Browse the Feed**: Scroll through the news feed to see all related sections
   - Each card shows the file name, similarity score, section heading, and full content
   - Keywords are displayed at the bottom of each card
   - Content is automatically sorted from most to least similar

## Technical Details

### Dependencies
- `markdown>=3.3.0`: For advanced markdown rendering (optional)
- Falls back to basic regex-based rendering if not installed

### Installation
```bash
pip install markdown
```

Or install all requirements:
```bash
pip install -r requirements.txt
```

## Benefits

1. **No Clicking Required**: Just scroll to see everything
2. **Full Context**: Read complete sections without truncation
3. **Visual Hierarchy**: Similarity scores and color coding make it easy to prioritize
4. **Efficient Browsing**: All information in one continuous feed
5. **Beautiful Rendering**: Proper markdown formatting makes content readable

## Example Use Case

When you edit a section in your target file:
1. Hit "Refresh" to recalculate similarity
2. The news feed instantly updates with all related sections
3. Scroll through to see which sections from other files are most relevant
4. Read the full content of each section directly in the feed
5. Use keyword tags to understand the main topics at a glance

This makes it perfect for:
- Research and note-taking
- Finding related content across your knowledge base
- Discovering connections between different topics
- Quick reference while writing
