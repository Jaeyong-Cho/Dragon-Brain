# Markdown File Similarity Evaluator

A program that evaluates similarity between markdown note files and provides a ranking based on content similarity.

## Features

- 📄 Automatic keyword extraction from markdown files
- 🔍 Similarity calculation using TF-IDF and cosine similarity
- 🤖 **SBERT Support** - Optional Sentence-BERT for semantic similarity (new!)
- 📊 File ranking based on similarity scores
- 🎯 Markdown-specific keyword extraction (headings, bold text, links, etc.)
- 🛑 Smart stop words filtering (NLTK for English, custom for Korean)
- 📑 Section-level similarity analysis (compares by headings)
- 🖥️ **GUI Application** - Easy-to-use graphical interface
- 💻 **CLI Tool** - Command-line interface for automation
- ✏️ **Edit Detection** - Automatically detects edited sections and enables quick refresh
- 🔄 **Smart Refresh** - Recalculate similarity after making edits without restarting

## Installation

```bash
# Install required packages
pip install -r requirements.txt

# Or install individually
pip install scikit-learn numpy nltk PyQt6

# Optional: Install sentence-transformers for SBERT support
pip install sentence-transformers
```

## Usage

### GUI Application (Recommended)

Launch the graphical interface for easy file selection and visualization:

```bash
python gui.py
```

**GUI Features:**
- 🎯 Visual file selection for target and comparison files
- 📁 Directory browsing to select multiple files at once
- 🤖 **SBERT toggle** - Switch between TF-IDF and Sentence-BERT similarity
- 📊 Real-time similarity scores with color coding
- 📝 In-app markdown editor with edit detection
- ✏️ Section-aware edit tracking (detects which heading you're editing)
- 🔄 Quick refresh button to recalculate after edits
- 🔍 Detailed section-level similarity analysis
- 📈 Beautiful visualization of results with tabs
- 🎨 Modern, user-friendly interface

### CLI Tool

For command-line usage or automation:

### Method 1: Specify Individual Files

```bash
python main.py <target_file> <compare_file1> <compare_file2> ...
```

Example:
```bash
python main.py notes/my_note.md notes/note1.md notes/note2.md notes/note3.md
```

### Method 2: Specify Directory (Recommended)

```bash
python main.py <target_file> <directory>
```

Example:
```bash
python main.py sample_notes/target.md sample_notes/
```

When you specify a directory, the program compares with all `.md` files in that directory.

## Sample Output

```
Comparing target file with 4 files...

================================================================================
Target file: sample_notes/target.md
================================================================================

📄 Target File Content:
--------------------------------------------------------------------------------
# Machine Learning Overview

This document covers the fundamentals of machine learning...
--------------------------------------------------------------------------------
Total length: 3456 characters, 87 lines

Comparison results with 4 files (sorted by combined similarity):

1. compare1.md
   Path: sample_notes/compare1.md
   Combined Similarity: 75.40%
   ├─ Cosine Similarity: 78.40%
   ├─ Euclidean Similarity: 72.40%
   └─ Euclidean Distance: 0.3812
   Top keywords: data, science, machine, learning, analysis
   Most similar sections in this file:
      1. 'Machine Learning Basics': 89.3%
         Machine learning is a method of data analysis that automates
         analytical model building. It is a branch of artificial intelligence
         based on the idea that systems can learn from data...

      2. 'Deep Learning': 82.1%
         Deep learning is part of a broader family of machine learning methods
         based on artificial neural networks with representation learning...
```

## How It Works

1. **Keyword Extraction**
   - Markdown headings (`# Title`)
   - Bold text (`**bold**`)
   - Link text (`[text](url)`)
   - Important words in body text (based on frequency)
   - Stop words filtering (English via NLTK, Korean custom list)

2. **Similarity Calculation**
   - TF-IDF (Term Frequency-Inverse Document Frequency) vectorization
   - Cosine Similarity: Measures angle between vectors (0-1, higher is better)
   - Euclidean Distance: Measures geometric distance (lower is better)
   - Combined Similarity: Average of both normalized metrics

3. **Section-Level Analysis**
   - Splits comparison files by headings
   - Compares entire target file against each section
   - Shows which sections are most relevant
   - Measure document similarity using cosine similarity
   - Similarity scores between 0-100%

3. **Ranking Generation**
   - Sort by similarity (highest first)
   - Display top keywords for each file

## Use Cases

- 📝 Find notes on similar topics
- 🔗 Link related documents
- 📚 Organize and categorize notes
- 🎓 Group learning materials

## Testing

### Quick Demo

Test various scenarios with the interactive demo script:

```bash
python demo.py
```

The demo showcases:
1. English-to-English comparison (no translation needed)
2. Mixed language comparison (without translation)
3. Mixed language comparison (with translation) - **Recommended**
4. Korean target file translation comparison

### Test with Sample Files

You can test with the provided sample files:

#### Korean Dataset

```bash
python main.py sample_notes/korean/target.md sample_notes/korean/
```

Files in `sample_notes/korean/` directory:
- `target.md`: Python Programming Basics (target file)
- `data_science.md`: Introduction to Data Science (high similarity)
- `numpy.md`: NumPy and Array Operations (high similarity)
- `mobile_dev.md`: Mobile App Development
- `blockchain.md`: Blockchain and Cryptocurrency
- `cloud.md`: Cloud Computing
- `design_patterns.md`: Design Patterns
- `cybersecurity.md`: Cybersecurity
- `game_dev.md`: Game Development
- `devops.md`: DevOps and CI/CD
- `ai_ethics.md`: AI Ethics
- `web_dev.md`: Web Development Guide
- `algorithms.md`: Algorithms and Data Structures

#### English Dataset

```bash
python main.py sample_notes/english/machine_learning.md sample_notes/english/
```

Files in `sample_notes/english/` directory:
- `machine_learning.md`: Machine Learning Fundamentals
- `deep_learning.md`: Deep Learning
- `databases.md`: Database Systems
- `computer_graphics.md`: Computer Graphics
- `augmented_reality.md`: Augmented Reality
- `quantum_computing.md`: Quantum Computing
- `functional_programming.md`: Functional Programming
- `iot.md`: Internet of Things
- `neuroscience.md`: Neuroscience
- `renewable_energy.md`: Renewable Energy
- `psychology.md`: Psychology
- `materials_science.md`: Materials Science
- `urban_planning.md`: Urban Planning
- `linguistics.md`: Linguistics
- `anthropology.md`: Anthropology

#### Mixed Language Dataset (with Translation)

```bash
python main.py sample_notes/target.md sample_notes/ --translate
```

This compares across both Korean and English files with automatic translation for accurate cross-language similarity.

## Technical Details

### Algorithm

1. **Text Processing**
   - Read markdown files
   - Optional: Translate Korean to English
   - Extract keywords using markdown-specific patterns

2. **Vectorization**
   - Convert text to TF-IDF vectors
   - Each word gets a weight based on importance

3. **Similarity Measurement**
   - Calculate cosine similarity between vectors
   - Value ranges from 0 (completely different) to 1 (identical)
   - Convert to percentage for display

### Translation Process

1. Detect language of each file (Korean detection: >20% Korean characters)
2. If Korean detected and `--translate` flag is set:
   - Split text into chunks (~4500 characters each)
   - Translate each chunk via Google Translate API
   - Reassemble translated text
3. Extract keywords from (possibly translated) text
4. Calculate TF-IDF and cosine similarity

### Keyword Extraction Priority

1. **High priority**: Headings, bold text, links (explicit emphasis)
2. **Medium priority**: Frequently occurring words
3. **Low priority**: Short words (filtered out), code blocks (excluded)

## Requirements

### Core Dependencies
- Python 3.7+
- scikit-learn >= 1.0.0
- numpy >= 1.21.0

### Optional Dependencies
- googletrans == 4.0.0-rc1 (for translation features)

Install all at once:
```bash
pip install -r requirements.txt
```

## Project Structure

```
dragon-brain/
├── main.py                 # Main program
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── README_EN.md           # English README
├── setup.sh               # Quick setup script
├── TRANSLATION_FEATURE.md # Translation feature documentation
└── sample_notes/          # Sample markdown files
    ├── target.md
    ├── english/           # English sample files
    │   ├── machine_learning.md
    │   ├── deep_learning.md
    │   └── ...
    └── korean/            # Korean sample files
        ├── ai_ethics.md
        ├── data_science.md
        └── ...
```

## Troubleshooting

### Translation not working

**Problem**: "googletrans not installed" error

**Solution**:
```bash
pip install googletrans==4.0.0-rc1
```

### No similar files found

**Problem**: All similarity scores are 0%

**Possible causes**:
1. Different languages without `--translate` flag
2. Completely different topics
3. Very short files (insufficient content)

**Solutions**:
- Use `--translate` for mixed language files
- Ensure files contain substantial content
- Check if files are actually related in topic

### Import errors

**Problem**: `ModuleNotFoundError` for scikit-learn or numpy

**Solution**:
```bash
pip install scikit-learn numpy
```

## Advanced Usage

### Custom Keyword Extraction

Modify the `extract_keywords()` function in `main.py` to adjust:
- Number of keywords extracted (`top_n` parameter)
- Minimum word length
- Stop words filtering

### Batch Processing

Process multiple target files:
```bash
for file in sample_notes/korean/*.md; do
    python main.py "$file" sample_notes/ --translate
done
```

### Output to File

Save results to a file:
```bash
python main.py sample_notes/target.md sample_notes/ --translate > results.txt
```

## Contributing

Contributions are welcome! Areas for improvement:
- Support for more languages (Japanese, Chinese, etc.)
- Caching mechanism for translations
- Performance optimization for large datasets
- Additional similarity algorithms
- GUI interface
- Export results to JSON/CSV

## License

This project is open source and available for educational and personal use.

## Acknowledgments

- Uses scikit-learn for TF-IDF vectorization and cosine similarity
- Uses googletrans for translation features
- Inspired by the need for better note organization and discovery

## Future Enhancements

- 🚀 Local translation models (offline support)
- 📊 Visualization of similarity networks
- 🔍 Semantic similarity using embeddings
- 💾 Database backend for large collections
- 🌐 Web interface
- 📱 Mobile app integration
- 🤖 AI-powered suggestions for linking notes

## Support

For issues, questions, or suggestions:
- Check existing documentation
- Review sample files for examples
- Ensure all dependencies are installed
- Verify file paths and formats

---

**Made with ❤️ for better note organization and discovery**
