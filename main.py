import sys
import os
from pathlib import Path
from collections import Counter
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
import numpy as np

# NLTK stop words support
try:
    from nltk.corpus import stopwords
    import nltk
    # Try to load stopwords, download if not available
    try:
        ENGLISH_STOP_WORDS = set(stopwords.words('english'))
    except LookupError:
        print("Downloading NLTK stopwords...")
        nltk.download('stopwords', quiet=True)
        ENGLISH_STOP_WORDS = set(stopwords.words('english'))
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False
    ENGLISH_STOP_WORDS = set()
    print("Warning: nltk not installed. Install with: pip install nltk")
    print("Continuing without NLTK stop words support...")
    print()

def read_markdown_file(file_path):
    """
    Reads a markdown file and returns its text content.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return content
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return ""

def extract_keywords(text, top_n=20):
    """
    Extracts important keywords from text.
    Prioritizes markdown-specific elements:
    - Headings
    - Bullet points
    - Bold text
    - Code blocks
    - Link text
    Uses TF-IDF to select important keywords.
    Filters out common stop words in English (via NLTK) and Korean.
    """
    # English stop words from NLTK (if available)
    english_stop_words = ENGLISH_STOP_WORDS if NLTK_AVAILABLE else set()
    
    # Korean stop words (조사, 접속사, 일반적인 단어)
    korean_stop_words = {
        '의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자',
        '에', '와', '한', '하다', '그', '저', '것', '수', '등', '년', '월', '일',
        '있다', '없다', '되다', '하는', '한다', '있는', '없는', '대한', '위한', '통해',
        '매우', '정말', '너무', '조금', '많이', '같은', '다른', '새로운', '따라',
        '또한', '그리고', '하지만', '그러나', '또는', '및', '때문', '이런', '저런',
        '어떤', '무엇', '누구', '언제', '어디', '왜', '어떻게', '이다', '아니다'
    }
    
    keywords = []
    
    # Extract markdown headings (# Title)
    headings = re.findall(r'#{1,6}\s+(.+)', text)
    keywords.extend(headings)
    
    # Extract bold text (**bold** or __bold__)
    bold_text = re.findall(r'\*\*(.+?)\*\*|__(.+?)__', text)
    keywords.extend([b[0] or b[1] for b in bold_text])
    
    # Extract link text [link text](url)
    link_text = re.findall(r'\[(.+?)\]\(.+?\)', text)
    keywords.extend(link_text)
    
    # Extract plain text, excluding code blocks
    text_without_code = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    text_without_code = re.sub(r'`.*?`', '', text_without_code)
    
    # Remove markdown syntax
    clean_text = re.sub(r'[#*_\[\]\(\)`]', ' ', text_without_code)
    
    # Extract words (Korean, English, numbers)
    words = re.findall(r'[가-힣]+|[a-zA-Z]+', clean_text.lower())
    
    # Filter out short words and stop words
    filtered_words = [
        w for w in words 
        if len(w) >= 2 and w not in english_stop_words and w not in korean_stop_words
    ]
    
    # Combine all keywords
    all_keywords = keywords + filtered_words
    
    # Extract top keywords by frequency
    word_freq = Counter(all_keywords)
    top_keywords = [word for word, freq in word_freq.most_common(top_n * 3)]
    
    return ' '.join(top_keywords), list(word_freq.items())

def extract_sections_by_heading(text):
    """
    Splits markdown text into sections based on headings.
    Returns a list of dictionaries with heading and content.
    """
    sections = []
    
    # Split by headings while preserving the heading markers
    lines = text.split('\n')
    current_heading = "Introduction"
    current_content = []
    
    for line in lines:
        # Check if line is a heading (# Heading)
        heading_match = re.match(r'^(#{1,6})\s+(.+)', line)
        
        if heading_match:
            # Save previous section
            if current_content:
                sections.append({
                    'heading': current_heading,
                    'content': '\n'.join(current_content).strip()
                })
            
            # Start new section
            current_heading = heading_match.group(2).strip()
            current_content = []
        else:
            current_content.append(line)
    
    # Add the last section
    if current_content:
        sections.append({
            'heading': current_heading,
            'content': '\n'.join(current_content).strip()
        })
    
    return sections

def calculate_heading_similarity(target_keywords, compare_sections):
    """
    Calculates similarity between entire target file and each section of comparison files.
    Returns similarity scores for each heading in the comparison file.
    """
    if not target_keywords or not compare_sections:
        return []
    
    results = []
    
    for compare_section in compare_sections:
        compare_heading = compare_section['heading']
        compare_content = compare_section['content']
        
        if not compare_content.strip():
            continue
        
        compare_keywords, _ = extract_keywords(compare_content, top_n=10)
        
        # Calculate similarity between target (whole file) and this section
        try:
            vectorizer = TfidfVectorizer()
            tfidf_matrix = vectorizer.fit_transform([target_keywords, compare_keywords])
            
            cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            # Calculate Euclidean distance
            target_dense = tfidf_matrix[0:1].toarray()
            compare_dense = tfidf_matrix[1:2].toarray()
            euclidean_dist = euclidean_distances(target_dense, compare_dense)[0][0]
            euclidean_sim = 1 / (1 + euclidean_dist)
            
            combined_sim = (cosine_sim + euclidean_sim) / 2
            
            results.append({
                'heading': compare_heading,
                'content': compare_content,
                'cosine_similarity': cosine_sim,
                'euclidean_similarity': euclidean_sim,
                'combined_similarity': combined_sim
            })
        except:
            # Skip if vocabulary is empty
            continue
    
    return results

def calculate_similarity(target_file, compare_files):
    """
    Calculates similarity between target file and comparison files.
    Uses TF-IDF vectorization with both cosine similarity and Euclidean distance.
    
    Metrics:
    - Cosine Similarity: Measures angle between vectors (0-1, higher is better)
    - Euclidean Distance: Measures geometric distance (0-∞, lower is better)
    - Combined Similarity: Average of both normalized metrics
    """
    # Read target file
    print("Reading and processing target file...")
    target_text = read_markdown_file(target_file)
    if not target_text:
        print(f"Error: Could not read target file {target_file}")
        return []
    
    target_keywords, target_freq = extract_keywords(target_text)
    
    print(f"\nProcessing {len(compare_files)} comparison files...")
    
    # Read comparison files
    compare_data = []
    for file_path in compare_files:
        if file_path == target_file:
            continue  # Skip self
        
        text = read_markdown_file(file_path)
        if text:
            keywords, freq = extract_keywords(text)
            sections = extract_sections_by_heading(text)
            compare_data.append({
                'file': file_path,
                'keywords': keywords,
                'freq': freq,
                'sections': sections
            })
    
    if not compare_data:
        print("No valid comparison files found.")
        return []
    
    # TF-IDF vectorization
    all_texts = [target_keywords] + [data['keywords'] for data in compare_data]
    
    try:
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(all_texts)
        
        # Calculate both cosine similarity and Euclidean distance
        target_vector = tfidf_matrix[0:1]
        compare_vectors = tfidf_matrix[1:]
        
        # Cosine similarity (range: -1 to 1, higher is more similar)
        cosine_similarities = cosine_similarity(target_vector, compare_vectors)[0]
        
        # Euclidean distance (range: 0 to infinity, lower is more similar)
        # Convert to dense array for Euclidean distance calculation
        target_dense = target_vector.toarray()
        compare_dense = compare_vectors.toarray()
        euclidean_distances_raw = euclidean_distances(target_dense, compare_dense)[0]
        
        # Normalize Euclidean distance to similarity score (0 to 1)
        # Using formula: similarity = 1 / (1 + distance)
        euclidean_similarities = 1 / (1 + euclidean_distances_raw)
        
        # Calculate combined similarity (average of both metrics)
        combined_similarities = (cosine_similarities + euclidean_similarities) / 2
        
        # Organize results
        results = []
        for i, data in enumerate(compare_data):
            # Calculate heading-based similarity (target vs each section of compare file)
            heading_similarities = calculate_heading_similarity(target_keywords, data['sections'])
            
            results.append({
                'file': data['file'],
                'cosine_similarity': cosine_similarities[i],
                'euclidean_similarity': euclidean_similarities[i],
                'combined_similarity': combined_similarities[i],
                'euclidean_distance': euclidean_distances_raw[i],
                'top_keywords': dict(data['freq'][:10]),
                'heading_similarities': heading_similarities
            })
        
        # Sort by combined similarity (highest first)
        results.sort(key=lambda x: x['combined_similarity'], reverse=True)
        
        return results
    except Exception as e:
        print(f"Error calculating similarity: {e}")
        return []

def print_results(target_file, results):
    """Prints results in a formatted way."""
    print("=" * 80)
    print(f"Target file: {target_file}")
    print("=" * 80)
    
    # Display target file content preview
    try:
        with open(target_file, 'r', encoding='utf-8') as f:
            target_content = f.read()
        
        print("\n📄 Target File Content:")
        print("-" * 80)
        
        # Show first 500 characters or first 10 lines, whichever is shorter
        content_lines = target_content.split('\n')
        preview_lines = content_lines[:10]
        preview_text = '\n'.join(preview_lines)
        
        if len(preview_text) > 500:
            preview_text = preview_text[:500] + "..."
        elif len(content_lines) > 10:
            preview_text += "\n..."
        
        print(preview_text)
        print("-" * 80)
        print(f"Total length: {len(target_content)} characters, {len(content_lines)} lines")
    except Exception as e:
        print(f"\nCould not read target file content: {e}")
    
    print()
    
    if not results:
        print("No similar files found.")
        return
    
    print(f"Comparison results with {len(results)} files (sorted by combined similarity):")
    print()
    
    for rank, result in enumerate(results, 1):
        file_name = os.path.basename(result['file'])
        cosine_percent = result['cosine_similarity'] * 100
        euclidean_percent = result['euclidean_similarity'] * 100
        combined_percent = result['combined_similarity'] * 100
        euclidean_dist = result['euclidean_distance']
        
        print(f"{rank}. {file_name}")
        print(f"   Path: {result['file']}")
        print(f"   Combined Similarity: {combined_percent:.2f}%")
        print(f"   ├─ Cosine Similarity: {cosine_percent:.2f}%")
        print(f"   ├─ Euclidean Similarity: {euclidean_percent:.2f}%")
        print(f"   └─ Euclidean Distance: {euclidean_dist:.4f}")
        print(f"   Top keywords: {', '.join(list(result['top_keywords'].keys())[:5])}")
        
        # Display top heading similarities
        heading_sims = result.get('heading_similarities', [])
        if heading_sims:
            # Sort by combined similarity
            heading_sims_sorted = sorted(heading_sims, key=lambda x: x['combined_similarity'], reverse=True)
            top_heading_matches = heading_sims_sorted[:3]
            
            print(f"   Most similar sections in this file:")
            for i, match in enumerate(top_heading_matches, 1):
                sim_percent = match['combined_similarity'] * 100
                heading = match['heading']
                content = match.get('content', '')
                
                print(f"      {i}. '{heading}': {sim_percent:.1f}%")
                
                # Display content preview (first 200 characters)
                if content:
                    content_preview = content.strip()[:200]
                    # Add ellipsis if content was truncated
                    if len(content.strip()) > 200:
                        content_preview += "..."
                    # Indent the content
                    content_lines = content_preview.split('\n')
                    for line in content_lines[:3]:  # Show first 3 lines max
                        print(f"         {line}")
                    if len(content_lines) > 3:
                        print(f"         ...")
                print()
        
        print()

def main():
    """
    Main function
    Usage:
    python main.py <target_file> <compare_file1> <compare_file2> ...
    or
    python main.py <target_file> <directory>
    """
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python main.py <target_file> <compare_file1> <compare_file2> ...")
        print("  python main.py <target_file> <directory>")
        print()
        print("Examples:")
        print("  python main.py notes/target.md notes/compare1.md notes/compare2.md")
        print("  python main.py notes/target.md notes/")
        sys.exit(1)
    
    target_file = sys.argv[1]
    
    # Check if target file exists
    if not os.path.exists(target_file):
        print(f"Error: Target file '{target_file}' not found.")
        sys.exit(1)
    
    # Collect comparison files
    compare_files = []
    
    for arg in sys.argv[2:]:
        if os.path.isfile(arg):
            # If it's a file
            if arg.endswith('.md'):
                compare_files.append(arg)
        elif os.path.isdir(arg):
            # If it's a directory, collect all markdown files
            for file in Path(arg).rglob('*.md'):
                compare_files.append(str(file))
        else:
            print(f"Warning: '{arg}' is neither a file nor a directory. Skipping.")
    
    if not compare_files:
        print("Error: No valid comparison files found.")
        sys.exit(1)
    
    print(f"Comparing target file with {len(compare_files)} files...")
    print()
    
    # Calculate similarity
    results = calculate_similarity(target_file, compare_files)
    
    # Print results
    print_results(target_file, results)

if __name__ == "__main__":
    main()