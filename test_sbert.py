"""
Test script to verify SBERT functionality
"""
from main import calculate_similarity, SBERT_AVAILABLE
import os

def test_sbert():
    print("=" * 80)
    print("Testing SBERT Functionality")
    print("=" * 80)
    
    # Check if SBERT is available
    print(f"\nSBERT Available: {SBERT_AVAILABLE}")
    
    if not SBERT_AVAILABLE:
        print("❌ sentence-transformers not installed. Install with: pip install sentence-transformers")
        return
    
    # Use sample files
    target_file = "sample_notes/target.md"
    compare_dir = "sample_notes/english"
    
    if not os.path.exists(target_file):
        print(f"❌ Target file not found: {target_file}")
        return
    
    if not os.path.exists(compare_dir):
        print(f"❌ Compare directory not found: {compare_dir}")
        return
    
    # Collect comparison files
    compare_files = []
    for filename in os.listdir(compare_dir):
        if filename.endswith('.md'):
            compare_files.append(os.path.join(compare_dir, filename))
    
    if not compare_files:
        print("❌ No comparison files found")
        return
    
    print(f"\n📁 Target: {target_file}")
    print(f"📁 Comparing with {len(compare_files)} files from {compare_dir}")
    
    # Test with TF-IDF (default)
    print("\n" + "=" * 80)
    print("Test 1: TF-IDF Similarity (use_sbert=False)")
    print("=" * 80)
    
    results_tfidf = calculate_similarity(target_file, compare_files[:3], use_sbert=False)
    
    if results_tfidf:
        print(f"\n✅ TF-IDF calculation successful! Found {len(results_tfidf)} results")
        print("\nTop 3 results:")
        for i, result in enumerate(results_tfidf[:3], 1):
            file_name = os.path.basename(result['file'])
            sim = result['combined_similarity'] * 100
            print(f"  {i}. {file_name}: {sim:.2f}%")
    else:
        print("❌ TF-IDF calculation failed")
    
    # Test with SBERT
    print("\n" + "=" * 80)
    print("Test 2: SBERT Similarity (use_sbert=True)")
    print("=" * 80)
    
    try:
        results_sbert = calculate_similarity(target_file, compare_files[:3], use_sbert=True)
        
        if results_sbert:
            print(f"\n✅ SBERT calculation successful! Found {len(results_sbert)} results")
            print("\nTop 3 results:")
            for i, result in enumerate(results_sbert[:3], 1):
                file_name = os.path.basename(result['file'])
                sim = result['combined_similarity'] * 100
                print(f"  {i}. {file_name}: {sim:.2f}%")
        else:
            print("❌ SBERT calculation returned no results")
    except Exception as e:
        print(f"❌ SBERT calculation failed with error: {e}")
    
    print("\n" + "=" * 80)
    print("✅ All tests completed!")
    print("=" * 80)

if __name__ == "__main__":
    test_sbert()
