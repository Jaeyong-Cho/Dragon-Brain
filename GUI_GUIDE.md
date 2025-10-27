# Dragon Brain GUI Guide

## Quick Start

### Launch the GUI

**Option 1: Using the launcher script (macOS/Linux)**
```bash
./run_gui.sh
```

**Option 2: Direct Python command**
```bash
python gui.py
```

## GUI Overview

The Dragon Brain GUI provides an intuitive interface for analyzing markdown file similarity with three main panels:

### 1. Left Panel - Target File Content
- Displays and **allows editing** of your target file
- In-app markdown editor with edit detection
- **Real-time section tracking**: Shows which section you're editing
- Automatically loads when you select a target file
- Changes are saved when you click the refresh button

### 2. Middle Panel - Results List
- Shows all comparison files ranked by similarity
- Color-coded results:
  - 🟢 **Green (70%+)**: High similarity
  - 🟡 **Yellow (50-70%)**: Medium similarity
  - 🔴 **Red (<50%)**: Low similarity
- Click any file to see detailed analysis

### 3. Right Panel - Details (Tabbed)

#### Tab 1: Scores
- Combined similarity percentage
- Cosine similarity score
- Euclidean similarity score
- Euclidean distance
- Top keywords from the file

#### Tab 2: Similar Sections
- Shows the top 5 most similar sections
- Each section displays:
  - Heading name
  - Similarity percentage (color-coded)
  - Content preview (first 300 characters)

## How to Use

### Step 1: Select Target File
1. Click **"Select Target File"** button
2. Choose your main markdown file (the one you want to compare against)
3. The file content will appear in the left panel
4. You can now edit the content directly in the GUI

### Step 1.5: Edit and Refresh (Optional)
1. **Edit your target file** directly in the left panel
2. As you type, the system **automatically detects which section** (heading) you're editing
3. The edit detection label will show: `📝 Edited: {Section Name}`
4. When ready, click the **🔄 Refresh** button to:
   - Save your changes to the file
   - Recalculate similarity with the updated content
   - See new results based on your edits

### Step 2: Select Comparison Files

**Option A: Select Individual Files**
1. Click **"Select Files"** button
2. Use Ctrl/Cmd to select multiple markdown files
3. Click "Open"

**Option B: Select Entire Directory**
1. Click **"Select Directory"** button
2. Choose a folder containing markdown files
3. All `.md` files in the directory and subdirectories will be included

### Step 3: Calculate Similarity
1. Click the green **"Calculate Similarity"** button
2. Wait for processing (progress bar will show)
3. Results will appear ranked by similarity

### Step 4: Explore Results
1. Click any file in the middle panel
2. View detailed scores in the "Scores" tab
3. Explore similar sections in the "Similar Sections" tab
4. Read section content previews inline

## Features

### Real-time Processing
- Background thread processing (GUI remains responsive)
- Progress bar shows calculation status
- Status bar updates with current operation

### Edit Detection & Quick Refresh
- **Section-aware editing**: Automatically detects which markdown section you're editing
- **Visual feedback**: Shows `📝 Edited: {Section Name}` when changes are made
- **Smart refresh**: Click 🔄 button to save and recalculate instantly
- **No file switching**: Edit, save, and recalculate all within the GUI

### Visual Feedback
- Color-coded similarity scores
- Easy-to-read HTML formatted details
- Section highlighting by similarity level
- Real-time edit detection labels

### Smart Analysis
- Stop words filtering (English & Korean)
- TF-IDF vectorization
- Multiple similarity metrics
- Section-level granularity

## Tips

1. **Better Results**: Use files with clear markdown structure (headings, bold text)
2. **Faster Processing**: Select specific files instead of large directories if you know what you're looking for
3. **Edit and Iterate**: Make changes to your target file and quickly refresh to see how similarity changes
4. **Section Focus**: When editing, you'll see which section you're in - great for organizing thoughts
5. **Understanding Scores**:
   - Combined similarity is the average of cosine and euclidean metrics
   - Look at section similarities to understand what specifically matches
6. **Multiple Comparisons**: You can run multiple analyses without restarting the GUI

## Keyboard Shortcuts
- **Up/Down arrows**: Navigate through results list
- **Enter**: View details of selected result

## Troubleshooting

### GUI won't start
```bash
# Install dependencies
pip install -r requirements.txt
```

### No results showing
- Ensure comparison files are valid markdown (.md) files
- Check that target file is different from comparison files
- Verify files are not empty

### Slow performance
- Reduce number of comparison files
- Close other applications
- Use specific files instead of entire large directories

## System Requirements

- Python 3.8 or higher
- PyQt6
- scikit-learn
- numpy
- nltk

## Support

For issues or questions, check the main README.md file.
