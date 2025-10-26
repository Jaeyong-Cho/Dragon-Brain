#!/bin/bash
# Quick setup script for translation feature

echo "🚀 Dragon Brain - Translation Feature Setup"
echo "==========================================="
echo ""

# Check Python version
echo "📋 Checking Python version..."
python3 --version

echo ""
echo "📦 Installing dependencies..."
echo ""

# Install core dependencies
echo "Installing core dependencies (scikit-learn, numpy)..."
pip install scikit-learn numpy

echo ""
echo "Installing translation library (googletrans)..."
pip install googletrans==4.0.0-rc1

echo ""
echo "✅ Installation complete!"
echo ""
echo "🧪 Running a quick test..."
echo ""

# Run a simple test
python3 -c "
import sklearn
import numpy
print('✓ scikit-learn version:', sklearn.__version__)
print('✓ numpy version:', numpy.__version__)

try:
    from googletrans import Translator
    print('✓ googletrans: installed')
    print('')
    print('🎉 All dependencies are ready!')
    print('')
    print('Next steps:')
    print('  1. Run demo: python demo.py')
    print('  2. Try translation: python main.py sample_notes/target.md sample_notes/ --translate')
except ImportError:
    print('⚠ googletrans: not installed')
    print('  Translation features will not be available')
"
