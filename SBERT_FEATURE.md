# SBERT Integration Feature

## Overview

Dragon Brain now supports **Sentence-BERT (SBERT)** for semantic similarity calculation, offering an advanced alternative to the default TF-IDF vectorization method.

## What is SBERT?

Sentence-BERT (SBERT) is a modification of BERT that uses siamese and triplet network structures to derive semantically meaningful sentence embeddings. This allows SBERT to:

- Capture deeper semantic meaning beyond keyword matching
- Better understand context and relationships between concepts
- Provide more nuanced similarity scores for documents with similar meanings but different vocabulary

## How to Use

### 1. Installation

The `sentence-transformers` package is now included in `requirements.txt`. Install it with:

```bash
pip install sentence-transformers
```

Or install all dependencies:

```bash
pip install -r requirements.txt
```

### 2. GUI Usage

1. Launch the Dragon Brain GUI:
   ```bash
   python gui.py
   ```

2. In the File Selection section, you'll see a new checkbox:
   - **☐ Use SBERT (sentence-transformers)**

3. To use SBERT for similarity calculation:
   - Check the "Use SBERT" checkbox
   - Select your target file and comparison files as usual
   - Click "Calculate Similarity" or "🔄 Refresh"

4. The calculation will use the SBERT model instead of TF-IDF

### 3. Command-Line Usage

From Python code, you can now specify `use_sbert=True`:

```python
from main import calculate_similarity

# Use TF-IDF (default)
results = calculate_similarity(target_file, compare_files)

# Use SBERT
results = calculate_similarity(target_file, compare_files, use_sbert=True)
```

## Technical Details

### Model Used

By default, SBERT uses the `paraphrase-MiniLM-L6-v2` model:
- Fast and efficient
- 384-dimensional embeddings
- Good balance between speed and quality
- ~80MB download on first use

### How it Works

1. **File Encoding**: Each markdown file (target and comparison files) is encoded into a dense vector embedding
2. **Section Encoding**: Each section within comparison files is also encoded separately
3. **Similarity Calculation**: 
   - Cosine similarity between embeddings
   - Euclidean distance (normalized)
   - Combined score (average of both metrics)

### Comparison: TF-IDF vs SBERT

| Feature | TF-IDF | SBERT |
|---------|--------|-------|
| **Speed** | Fast | Slower (first run downloads model) |
| **Accuracy** | Keyword-based | Semantic meaning |
| **Dependencies** | scikit-learn | sentence-transformers, PyTorch |
| **Best For** | Exact keyword matching | Conceptual similarity |
| **Memory** | Low | Higher (~80MB model + embeddings) |

### When to Use Each Method

**Use TF-IDF (default) when:**
- You want fast results
- Documents share similar vocabulary
- You're looking for keyword matches
- Memory/storage is limited

**Use SBERT when:**
- Documents express similar ideas with different words
- You need deeper semantic understanding
- Quality is more important than speed
- You have adequate memory and storage

## Example Results

Given a target file about "machine learning basics":

**TF-IDF might rank higher:**
- Files with exact terms like "machine learning", "neural networks", "training"

**SBERT might rank higher:**
- Files about "AI model training" (similar concept, different words)
- Files about "deep learning foundations" (related semantic meaning)
- Files about "supervised algorithms" (contextually related)

## Performance Notes

- **First run**: SBERT will download the model (~80MB) on first use
- **Subsequent runs**: Model is cached locally for faster loading
- **Calculation time**: SBERT is slower than TF-IDF but provides richer semantic analysis
- **Recommendations**: 
  - For quick scans: Use TF-IDF
  - For thorough analysis: Use SBERT
  - For best results: Try both and compare

## Troubleshooting

### "sentence-transformers not installed" error

**Solution**: Install the package
```bash
pip install sentence-transformers
```

### Model download fails

**Possible causes**: Network issues, firewall blocking
**Solution**: 
- Check internet connection
- Try again later
- Manually download model if needed

### Out of memory errors

**Cause**: SBERT uses more memory than TF-IDF
**Solutions**:
- Process fewer files at once
- Use TF-IDF instead
- Increase available system memory

## Future Enhancements

Potential improvements for future versions:
- Model selection dropdown (allow choosing different SBERT models)
- Hybrid mode (combine TF-IDF and SBERT scores)
- Cache embeddings for frequently compared files
- GPU acceleration support
- Progress indicators during model loading

## References

- [Sentence-Transformers Documentation](https://www.sbert.net/)
- [SBERT Paper](https://arxiv.org/abs/1908.10084)
- [Hugging Face Models](https://huggingface.co/sentence-transformers)
