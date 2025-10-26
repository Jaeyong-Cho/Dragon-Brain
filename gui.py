import sys
import os
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTextEdit, QFileDialog, QListWidget,
    QSplitter, QGroupBox, QProgressBar, QTabWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QTextCursor

from main import calculate_similarity, read_markdown_file


class SimilarityWorker(QThread):
    """Worker thread for calculating similarity without blocking GUI"""
    finished = pyqtSignal(list)
    progress = pyqtSignal(str)
    error = pyqtSignal(str)
    
    def __init__(self, target_file, compare_files):
        super().__init__()
        self.target_file = target_file
        self.compare_files = compare_files
    
    def run(self):
        try:
            self.progress.emit("Starting similarity calculation...")
            results = calculate_similarity(self.target_file, self.compare_files)
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
        left_layout.addWidget(QLabel("Target File Content:"))
        self.target_content = QTextEdit()
        self.target_content.setReadOnly(True)
        self.target_content.setFont(QFont("Courier", 10))
        left_layout.addWidget(self.target_content)
        splitter.addWidget(left_panel)
        
        # Middle panel - Results list
        middle_panel = QWidget()
        middle_layout = QVBoxLayout(middle_panel)
        middle_layout.addWidget(QLabel("Similar Files (Ranked):"))
        self.results_list = QListWidget()
        self.results_list.itemClicked.connect(self.show_result_details)
        middle_layout.addWidget(self.results_list)
        splitter.addWidget(middle_panel)
        
        # Right panel - Details with tabs
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.addWidget(QLabel("Details:"))
        
        self.details_tabs = QTabWidget()
        
        # Tab 1: Similarity scores
        self.scores_text = QTextEdit()
        self.scores_text.setReadOnly(True)
        self.details_tabs.addTab(self.scores_text, "Scores")
        
        # Tab 2: Similar sections
        self.sections_text = QTextEdit()
        self.sections_text.setReadOnly(True)
        self.details_tabs.addTab(self.sections_text, "Similar Sections")
        
        right_layout.addWidget(self.details_tabs)
        splitter.addWidget(right_panel)
        
        # Set splitter sizes
        splitter.setSizes([400, 300, 500])
        
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
    
    def calculate_similarity(self):
        if not self.target_file or not self.compare_files:
            return
        
        # Disable button and show progress
        self.calculate_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        self.statusBar().showMessage("Calculating similarity...")
        
        # Clear previous results
        self.results_list.clear()
        self.scores_text.clear()
        self.sections_text.clear()
        
        # Start worker thread
        self.worker = SimilarityWorker(self.target_file, self.compare_files)
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
        
        # Populate results list
        for i, result in enumerate(results, 1):
            file_name = os.path.basename(result['file'])
            combined_percent = result['combined_similarity'] * 100
            item_text = f"{i}. {file_name} - {combined_percent:.2f}%"
            
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, result)
            
            # Color code by similarity
            if combined_percent >= 70:
                item.setForeground(Qt.GlobalColor.darkGreen)
            elif combined_percent >= 50:
                item.setForeground(Qt.GlobalColor.darkYellow)
            else:
                item.setForeground(Qt.GlobalColor.darkRed)
            
            self.results_list.addItem(item)
        
        self.statusBar().showMessage(f"Found {len(results)} similar files")
        
        # Auto-select first item
        if results:
            self.results_list.setCurrentRow(0)
            self.show_result_details(self.results_list.item(0))
    
    def on_calculation_error(self, error_msg):
        self.progress_bar.setVisible(False)
        self.calculate_btn.setEnabled(True)
        self.statusBar().showMessage(f"Error: {error_msg}")
    
    def show_result_details(self, item):
        if not item:
            return
        
        result = item.data(Qt.ItemDataRole.UserRole)
        if not result:
            return
        
        # Show similarity scores
        file_name = os.path.basename(result['file'])
        cosine_percent = result['cosine_similarity'] * 100
        euclidean_percent = result['euclidean_similarity'] * 100
        combined_percent = result['combined_similarity'] * 100
        euclidean_dist = result['euclidean_distance']
        
        scores_html = f"""
        <h2>{file_name}</h2>
        <p><b>File Path:</b> {result['file']}</p>
        <hr>
        <h3>Similarity Scores:</h3>
        <table style="width:100%; border-collapse: collapse;">
            <tr style="background-color: #f0f0f0;">
                <td style="padding: 8px; border: 1px solid #ddd;"><b>Combined Similarity</b></td>
                <td style="padding: 8px; border: 1px solid #ddd; color: #4CAF50; font-size: 16px;"><b>{combined_percent:.2f}%</b></td>
            </tr>
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd;">Cosine Similarity</td>
                <td style="padding: 8px; border: 1px solid #ddd;">{cosine_percent:.2f}%</td>
            </tr>
            <tr style="background-color: #f9f9f9;">
                <td style="padding: 8px; border: 1px solid #ddd;">Euclidean Similarity</td>
                <td style="padding: 8px; border: 1px solid #ddd;">{euclidean_percent:.2f}%</td>
            </tr>
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd;">Euclidean Distance</td>
                <td style="padding: 8px; border: 1px solid #ddd;">{euclidean_dist:.4f}</td>
            </tr>
        </table>
        <br>
        <h3>Top Keywords:</h3>
        <p>{', '.join(list(result['top_keywords'].keys())[:10])}</p>
        """
        
        self.scores_text.setHtml(scores_html)
        
        # Show similar sections
        heading_sims = result.get('heading_similarities', [])
        if heading_sims:
            heading_sims_sorted = sorted(heading_sims, key=lambda x: x['combined_similarity'], reverse=True)
            top_headings = heading_sims_sorted[:5]
            
            sections_html = f"<h2>Most Similar Sections</h2><hr>"
            
            for i, match in enumerate(top_headings, 1):
                sim_percent = match['combined_similarity'] * 100
                heading = match['heading']
                content = match.get('content', '')
                
                # Get content preview
                content_preview = content.strip()[:300]
                if len(content.strip()) > 300:
                    content_preview += "..."
                
                # Escape HTML
                content_preview = content_preview.replace('<', '&lt;').replace('>', '&gt;')
                content_preview = content_preview.replace('\n', '<br>')
                
                color = "#4CAF50" if sim_percent >= 70 else "#FF9800" if sim_percent >= 50 else "#F44336"
                
                sections_html += f"""
                <div style="margin-bottom: 20px; padding: 10px; background-color: #f9f9f9; border-left: 4px solid {color};">
                    <h3 style="margin-top: 0;">{i}. {heading}</h3>
                    <p style="color: {color}; font-weight: bold;">Similarity: {sim_percent:.1f}%</p>
                    <div style="background-color: white; padding: 10px; border-radius: 4px; font-family: monospace; font-size: 12px;">
                        {content_preview}
                    </div>
                </div>
                """
            
            self.sections_text.setHtml(sections_html)
        else:
            self.sections_text.setHtml("<p>No section-level similarity data available.</p>")


def main():
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    window = MarkdownSimilarityGUI()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
