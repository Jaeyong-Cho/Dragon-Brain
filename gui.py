import sys
import os
import re
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTextEdit, QFileDialog, QListWidget,
    QSplitter, QGroupBox, QProgressBar, QTabWidget, QListWidgetItem,
    QScrollArea
)
from PyQt6.QtWidgets import QCheckBox
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QTextCursor

# Try to import markdown library
try:
    import markdown
    MARKDOWN_AVAILABLE = True
except ImportError:
    MARKDOWN_AVAILABLE = False

from main import calculate_similarity, read_markdown_file


class SimilarityWorker(QThread):
    """Worker thread for calculating similarity without blocking GUI"""
    finished = pyqtSignal(list)
    progress = pyqtSignal(str)
    error = pyqtSignal(str)
    
    def __init__(self, target_file, compare_files, use_sbert=False):
        super().__init__()
        self.target_file = target_file
        self.compare_files = compare_files
        self.use_sbert = use_sbert
    
    def run(self):
        try:
            self.progress.emit("Starting similarity calculation...")
            results = calculate_similarity(self.target_file, self.compare_files, use_sbert=self.use_sbert)
            self.finished.emit(results)
        except Exception as e:
            self.error.emit(str(e))


class MarkdownSimilarityGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.target_file = None
        self.compare_files = []
        self.results = []
        self.worker = None
        self.last_edit_section = None
        self.last_target_content = ""
        
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Dragon Brain - Markdown Similarity Analyzer")
        self.setGeometry(100, 100, 1400, 900)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Top section - File selection
        file_selection_group = QGroupBox("File Selection")
        file_layout = QVBoxLayout()
        
        # Target file selection
        target_layout = QHBoxLayout()
        target_layout.addWidget(QLabel("Target File:"))
        self.target_label = QLabel("No file selected")
        self.target_label.setStyleSheet("color: gray; font-style: italic;")
        target_layout.addWidget(self.target_label, 1)
        self.target_btn = QPushButton("Select Target File")
        self.target_btn.clicked.connect(self.select_target_file)
        target_layout.addWidget(self.target_btn)
        
        # Refresh button for recalculating with edit detection
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.setEnabled(False)
        self.refresh_btn.setToolTip("Recalculate similarity (detects recent edits)")
        self.refresh_btn.clicked.connect(self.refresh_calculation)
        target_layout.addWidget(self.refresh_btn)
        
        file_layout.addLayout(target_layout)
        
        # Comparison files selection
        compare_layout = QHBoxLayout()
        compare_layout.addWidget(QLabel("Compare Files:"))
        self.compare_label = QLabel("No files selected")
        self.compare_label.setStyleSheet("color: gray; font-style: italic;")
        compare_layout.addWidget(self.compare_label, 1)
        self.compare_files_btn = QPushButton("Select Files")
        self.compare_files_btn.clicked.connect(self.select_compare_files)
        compare_layout.addWidget(self.compare_files_btn)
        self.compare_dir_btn = QPushButton("Select Directory")
        self.compare_dir_btn.clicked.connect(self.select_compare_directory)
        compare_layout.addWidget(self.compare_dir_btn)
        file_layout.addLayout(compare_layout)
        
        # Option: Use SBERT
        self.sbert_checkbox = QCheckBox("Use SBERT (sentence-transformers)")
        self.sbert_checkbox.setToolTip("If checked, similarity will be calculated using a Sentence-BERT model (requires sentence-transformers package).")
        file_layout.addWidget(self.sbert_checkbox)
        
        # Calculate button
        self.calculate_btn = QPushButton("Calculate Similarity")
        self.calculate_btn.setEnabled(False)
        self.calculate_btn.clicked.connect(self.calculate_similarity)
        self.calculate_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-weight: bold; padding: 10px; }")
        file_layout.addWidget(self.calculate_btn)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        file_layout.addWidget(self.progress_bar)
        
        file_selection_group.setLayout(file_layout)
        main_layout.addWidget(file_selection_group)
        
        # Main content area with splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel - Target file content
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # Header with edit detection info
        target_header_layout = QHBoxLayout()
        target_header_layout.addWidget(QLabel("Target File Content:"))
        self.edit_detection_label = QLabel("")
        self.edit_detection_label.setStyleSheet("color: #FF9800; font-style: italic;")
        target_header_layout.addWidget(self.edit_detection_label, 1)
        left_layout.addLayout(target_header_layout)
        
        self.target_content = QTextEdit()
        self.target_content.setReadOnly(False)  # Allow editing
        self.target_content.setFont(QFont("Courier", 10))
        self.target_content.textChanged.connect(self.on_target_content_changed)
        left_layout.addWidget(self.target_content)
        splitter.addWidget(left_panel)
        
        # Right panel - News Feed Style Display
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        # Header for news feed
        feed_header = QLabel("Related Sections Feed")
        feed_header.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px; background-color: #f0f0f0;")
        right_layout.addWidget(feed_header)
        
        # Scrollable news feed area
        self.news_feed = QTextEdit()
        self.news_feed.setReadOnly(True)
        self.news_feed.setStyleSheet("""
            QTextEdit {
                background-color: #fafafa;
                border: none;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            }
        """)
        right_layout.addWidget(self.news_feed)
        
        splitter.addWidget(right_panel)
        
        # Set splitter sizes (40% target, 60% feed)
        splitter.setSizes([500, 800])
        
        main_layout.addWidget(splitter, 1)
        
        # Status bar
        self.statusBar().showMessage("Ready")
    
    def select_target_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Target Markdown File", "", "Markdown Files (*.md)"
        )
        if file_path:
            self.target_file = file_path
            self.target_label.setText(os.path.basename(file_path))
            self.target_label.setStyleSheet("color: black;")
            self.load_target_content()
            self.check_ready_to_calculate()
            self.statusBar().showMessage(f"Target file selected: {file_path}")
    
    def select_compare_files(self):
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, "Select Comparison Markdown Files", "", "Markdown Files (*.md)"
        )
        if file_paths:
            self.compare_files = file_paths
            self.compare_label.setText(f"{len(file_paths)} files selected")
            self.compare_label.setStyleSheet("color: black;")
            self.check_ready_to_calculate()
            self.statusBar().showMessage(f"{len(file_paths)} comparison files selected")
    
    def select_compare_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Directory")
        if dir_path:
            md_files = list(Path(dir_path).rglob('*.md'))
            self.compare_files = [str(f) for f in md_files]
            self.compare_label.setText(f"{len(self.compare_files)} files from directory")
            self.compare_label.setStyleSheet("color: black;")
            self.check_ready_to_calculate()
            self.statusBar().showMessage(f"{len(self.compare_files)} files found in directory")
    
    def check_ready_to_calculate(self):
        if self.target_file and self.compare_files:
            self.calculate_btn.setEnabled(True)
        else:
            self.calculate_btn.setEnabled(False)
    
    def load_target_content(self):
        if self.target_file:
            content = read_markdown_file(self.target_file)
            self.target_content.setText(content)
            self.last_target_content = content
            self.last_edit_section = None
            self.edit_detection_label.setText("")
    
    def on_target_content_changed(self):
        """Detect when target content is edited and identify the section"""
        if not self.target_file:
            return
        
        current_content = self.target_content.toPlainText()
        
        # Check if content actually changed
        if current_content == self.last_target_content:
            return
        
        # Detect the edited section
        cursor = self.target_content.textCursor()
        cursor_position = cursor.position()
        
        # Find the section (by header) where the cursor is
        section = self.find_section_at_position(current_content, cursor_position)
        
        if section:
            self.last_edit_section = section
            self.edit_detection_label.setText(f"Edited: {section}")
            self.refresh_btn.setEnabled(True)
            self.statusBar().showMessage(f"Edit detected in section: {section}")
        else:
            self.edit_detection_label.setText("Content edited")
            self.refresh_btn.setEnabled(True)
            self.statusBar().showMessage("Edit detected in target file")
        
        self.last_target_content = current_content
    
    def find_section_at_position(self, content, position):
        """Find the markdown section (heading) at the given cursor position"""
        # Split content into lines and find which line the position is at
        lines = content[:position].split('\n')
        current_line = len(lines) - 1
        
        # Search backwards for the nearest heading
        all_lines = content.split('\n')
        for i in range(current_line, -1, -1):
            line = all_lines[i].strip()
            # Check if line is a markdown heading (starts with #)
            if line.startswith('#'):
                # Extract heading text
                heading_text = line.lstrip('#').strip()
                return heading_text
        
        return None
    
    def refresh_calculation(self):
        """Refresh similarity calculation with edit detection"""
        if not self.target_file or not self.compare_files:
            return
        
        # Save the current edited content back to the file
        current_content = self.target_content.toPlainText()
        
        # Optionally save to file (or work with in-memory content)
        try:
            with open(self.target_file, 'w', encoding='utf-8') as f:
                f.write(current_content)
            self.statusBar().showMessage("Target file saved. Recalculating...")
        except Exception as e:
            self.statusBar().showMessage(f"Error saving file: {e}")
            return
        
        # Show which section was edited
        if self.last_edit_section:
            self.statusBar().showMessage(f"Recalculating similarity (edited section: {self.last_edit_section})...")
        else:
            self.statusBar().showMessage("Recalculating similarity...")
        
        # Call the normal calculate function
        self.calculate_similarity()
        
        # Clear edit detection after recalculation
        self.edit_detection_label.setText("")
        self.refresh_btn.setEnabled(False)
    
    
    def calculate_similarity(self):
        if not self.target_file or not self.compare_files:
            return
        
        # Disable button and show progress
        self.calculate_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        self.statusBar().showMessage("Calculating similarity...")
        
        # Clear previous results
        self.news_feed.clear()
        
        # Start worker thread (pass SBERT option)
        use_sbert_opt = self.sbert_checkbox.isChecked() if hasattr(self, 'sbert_checkbox') else False
        self.worker = SimilarityWorker(self.target_file, self.compare_files, use_sbert=use_sbert_opt)
        self.worker.finished.connect(self.on_calculation_finished)
        self.worker.progress.connect(self.on_progress_update)
        self.worker.error.connect(self.on_calculation_error)
        self.worker.start()
    
    def on_progress_update(self, message):
        self.statusBar().showMessage(message)
    
    def on_calculation_finished(self, results):
        self.results = results
        self.progress_bar.setVisible(False)
        self.calculate_btn.setEnabled(True)
        
        # Build news feed HTML
        self.build_news_feed(results)
        
        # Show status with edit section info if available
        status_msg = f"Found {len(results)} similar files"
        if self.last_edit_section:
            status_msg += f" (focused on edited section: '{self.last_edit_section}')"
        self.statusBar().showMessage(status_msg)
    
    def on_calculation_error(self, error_msg):
        self.progress_bar.setVisible(False)
        self.calculate_btn.setEnabled(True)
        self.statusBar().showMessage(f"Error: {error_msg}")
    
    def markdown_to_html(self, md_text):
        """Convert markdown text to HTML with proper styling"""
        if MARKDOWN_AVAILABLE:
            try:
                # Use markdown library if available
                html = markdown.markdown(md_text, extensions=['fenced_code', 'tables', 'nl2br'])
                return html
            except:
                pass
        
        # Fallback: basic markdown rendering
        html = md_text
        # Headers
        html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
        # Bold
        html = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', html)
        # Italic
        html = re.sub(r'\*(.*?)\*', r'<i>\1</i>', html)
        # Code blocks
        html = re.sub(r'```(.*?)```', r'<pre>\1</pre>', html, flags=re.DOTALL)
        # Inline code
        html = re.sub(r'`(.*?)`', r'<code>\1</code>', html)
        # Line breaks
        html = html.replace('\n', '<br>')
        return html
    
    def build_news_feed(self, results):
        """Build a scrollable news feed of all related sections"""
        if not results:
            self.news_feed.setHtml("<p style='padding: 20px; text-align: center; color: #999;'>No results yet. Select files and calculate similarity.</p>")
            return
        
        feed_html = """
        <html>
        <head>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Helvetica Neue', Arial, sans-serif;
                line-height: 1.47059;
                font-size: 17px;
                letter-spacing: -0.022em;
                color: #1d1d1f;
                margin: 0;
                padding: 16px;
                background-color: #f5f5f7;
            }
            .feed-item {
                background: #ffffff;
                border-radius: 18px;
                padding: 24px;
                margin-bottom: 16px;
                box-shadow: 0 4px 16px rgba(0,0,0,0.08);
                border: 0.5px solid rgba(0,0,0,0.04);
                transition: all 0.3s ease;
            }
            .feed-item:hover {
                box-shadow: 0 8px 24px rgba(0,0,0,0.12);
            }
            .feed-item.high {
                border-left: 4px solid #30d158;
            }
            .feed-item.medium {
                border-left: 4px solid #ff9f0a;
            }
            .feed-item.low {
                border-left: 4px solid #ff453a;
            }
            .file-header {
                margin-bottom: 16px;
                padding-bottom: 12px;
                border-bottom: 1px solid rgba(0,0,0,0.06);
            }
            .file-name {
                font-size: 20px;
                font-weight: 600;
                letter-spacing: -0.015em;
                color: #1d1d1f;
                margin: 0 0 8px 0;
            }
            .similarity-badge {
                display: inline-block;
                padding: 4px 14px;
                border-radius: 16px;
                font-size: 13px;
                font-weight: 600;
                letter-spacing: -0.01em;
                color: white;
            }
            .similarity-badge.high {
                background: linear-gradient(135deg, #30d158 0%, #28a745 100%);
            }
            .similarity-badge.medium {
                background: linear-gradient(135deg, #ff9f0a 0%, #ff8c00 100%);
            }
            .similarity-badge.low {
                background: linear-gradient(135deg, #ff453a 0%, #e63946 100%);
            }
            .section {
                margin: 20px 0;
                padding: 20px;
                background-color: #f9f9f9;
                border-radius: 12px;
                border: 1px solid rgba(0,0,0,0.06);
            }
            .section-header {
                font-size: 19px;
                font-weight: 600;
                letter-spacing: -0.015em;
                color: #1d1d1f;
                margin: 0 0 12px 0;
            }
            .section-similarity {
                font-size: 13px;
                color: #86868b;
                margin-bottom: 12px;
            }
            .section-content {
                color: #1d1d1f;
                line-height: 1.52947;
                font-size: 17px;
                letter-spacing: -0.022em;
            }
            .section-content h1 {
                font-size: 32px;
                font-weight: 700;
                letter-spacing: -0.005em;
                line-height: 1.125;
                margin: 24px 0 16px 0;
                color: #1d1d1f;
            }
            .section-content h2 {
                font-size: 28px;
                font-weight: 700;
                letter-spacing: -0.003em;
                line-height: 1.14286;
                margin: 20px 0 14px 0;
                color: #1d1d1f;
            }
            .section-content h3 {
                font-size: 24px;
                font-weight: 600;
                letter-spacing: -0.002em;
                line-height: 1.16667;
                margin: 18px 0 12px 0;
                color: #1d1d1f;
            }
            .section-content h4 {
                font-size: 20px;
                font-weight: 600;
                letter-spacing: -0.015em;
                line-height: 1.2;
                margin: 16px 0 10px 0;
                color: #1d1d1f;
            }
            .section-content p {
                margin: 0 0 16px 0;
                line-height: 1.52947;
            }
            .section-content strong {
                font-weight: 600;
                color: #1d1d1f;
            }
            .section-content em {
                font-style: italic;
            }
            .section-content code {
                background-color: rgba(175,184,193,0.2);
                padding: 3px 7px;
                border-radius: 6px;
                font-family: 'SF Mono', 'Monaco', 'Menlo', 'Courier New', monospace;
                font-size: 15px;
                color: #1d1d1f;
                font-weight: 400;
            }
            .section-content pre {
                background-color: #1d1d1f;
                color: #f5f5f7;
                padding: 20px;
                border-radius: 12px;
                overflow-x: auto;
                font-family: 'SF Mono', 'Monaco', 'Menlo', 'Courier New', monospace;
                font-size: 14px;
                line-height: 1.5;
                margin: 20px 0;
            }
            .section-content pre code {
                background-color: transparent;
                padding: 0;
                border-radius: 0;
                color: #f5f5f7;
                font-size: 14px;
            }
            .section-content blockquote {
                border-left: 4px solid #d2d2d7;
                padding-left: 20px;
                margin: 20px 0;
                color: #6e6e73;
                font-style: italic;
                font-size: 17px;
            }
            .section-content ul, .section-content ol {
                margin: 16px 0;
                padding-left: 32px;
            }
            .section-content li {
                margin: 8px 0;
                line-height: 1.52947;
            }
            .section-content a {
                color: #0066cc;
                text-decoration: none;
                transition: color 0.2s ease;
            }
            .section-content a:hover {
                color: #0077ed;
                text-decoration: underline;
            }
            .section-content table {
                border-collapse: collapse;
                width: 100%;
                margin: 20px 0;
                font-size: 15px;
            }
            .section-content th, .section-content td {
                border: 1px solid #d2d2d7;
                padding: 12px 16px;
                text-align: left;
            }
            .section-content th {
                background-color: #f5f5f7;
                font-weight: 600;
                color: #1d1d1f;
            }
            .section-content tr:nth-child(even) {
                background-color: #fafafa;
            }
            .keywords {
                margin-top: 20px;
                padding: 16px;
                background: linear-gradient(135deg, #f5f5f7 0%, #e8e8ed 100%);
                border-radius: 12px;
                font-size: 14px;
            }
            .keyword-tag {
                display: inline-block;
                background: linear-gradient(135deg, #007aff 0%, #0051d5 100%);
                color: white;
                padding: 5px 12px;
                margin: 4px;
                border-radius: 14px;
                font-size: 13px;
                font-weight: 500;
                letter-spacing: -0.01em;
                box-shadow: 0 2px 8px rgba(0,122,255,0.25);
            }
            .keywords strong {
                font-weight: 600;
                color: #1d1d1f;
                font-size: 14px;
            }
        </style>
        </head>
        <body>
        """
        
        # Collect all sections from all files
        all_sections = []
        
        for result in results:
            file_name = os.path.basename(result['file'])
            file_path = result['file']
            combined_percent = result['combined_similarity'] * 100
            
            # Determine similarity class
            if combined_percent >= 70:
                sim_class = "high"
                item_class = "high"
            elif combined_percent >= 50:
                sim_class = "medium"
                item_class = "medium"
            else:
                sim_class = "low"
                item_class = "low"
            
            # Get heading similarities
            heading_sims = result.get('heading_similarities', [])
            
            # If we have section-level data, add each section
            if heading_sims:
                heading_sims_sorted = sorted(heading_sims, key=lambda x: x['combined_similarity'], reverse=True)
                
                for heading_match in heading_sims_sorted:
                    section_sim = heading_match['combined_similarity'] * 100
                    heading = heading_match['heading']
                    content = heading_match.get('content', '')
                    
                    all_sections.append({
                        'file_name': file_name,
                        'file_path': file_path,
                        'file_similarity': combined_percent,
                        'sim_class': sim_class,
                        'item_class': item_class,
                        'section_similarity': section_sim,
                        'heading': heading,
                        'content': content,
                        'keywords': result.get('top_keywords', {})
                    })
            else:
                # No section data, show full file
                try:
                    content = read_markdown_file(file_path)
                except:
                    content = "Could not read file content."
                
                all_sections.append({
                    'file_name': file_name,
                    'file_path': file_path,
                    'file_similarity': combined_percent,
                    'sim_class': sim_class,
                    'item_class': item_class,
                    'section_similarity': combined_percent,
                    'heading': file_name,
                    'content': content,
                    'keywords': result.get('top_keywords', {})
                })
        
        # Sort all sections by similarity
        all_sections_sorted = sorted(all_sections, key=lambda x: x['section_similarity'], reverse=True)
        
        # Build HTML for each section
        for idx, section in enumerate(all_sections_sorted):
            # Render markdown content to HTML
            content_html = self.markdown_to_html(section['content'])
            
            # Get top keywords
            keywords = list(section['keywords'].keys())[:8]
            keywords_html = ''.join([f'<span class="keyword-tag">{kw}</span>' for kw in keywords])
            
            feed_html += f"""
            <div class="feed-item {section['item_class']}">
                <div class="file-header">
                    <div class="file-name">{section['file_name']}</div>
                    <span class="similarity-badge {section['sim_class']}">
                        {section['section_similarity']:.1f}% match
                    </span>
                </div>
                
                <div class="section">
                    <div class="section-header">{section['heading']}</div>
                    <div class="section-content">
                        {content_html}
                    </div>
                </div>
                
                <div class="keywords">
                    <strong>Keywords:</strong><br>
                    {keywords_html}
                </div>
            </div>
            """
        
        feed_html += """
        </body>
        </html>
        """
        
        self.news_feed.setHtml(feed_html)


def main():
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    window = MarkdownSimilarityGUI()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
