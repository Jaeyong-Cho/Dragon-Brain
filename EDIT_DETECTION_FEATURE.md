# Edit Detection Feature

## Overview

The Dragon Brain GUI now includes **automatic edit detection** that tracks where users make changes in the target markdown file and allows quick recalculation of similarity scores.

## Key Features

### 1. **Real-time Edit Detection**
   - The target file content editor now allows editing directly in the GUI
   - As you type, the system detects which section (markdown header) you're editing
   - Edit location is displayed with visual feedback

### 2. **Section-based Tracking**
   - Automatically identifies the nearest markdown heading (`#`, `##`, `###`, etc.) above your cursor
   - Shows the section name in the interface: `📝 Edited: {Section Name}`
   - Tracks the most recently edited section

### 3. **Refresh Button (🔄)**
   - New refresh button appears next to the target file selector
   - Enabled automatically when edits are detected
   - Clicking it:
     - Saves the edited content to the target file
     - Recalculates similarity with all comparison files
     - Shows which section was edited in the status bar
     - Resets the edit detection state

## How It Works

### Architecture

1. **Edit Tracking**
   ```python
   self.last_edit_section = None      # Stores the section name being edited
   self.last_target_content = ""      # Stores previous content for change detection
   ```

2. **Section Detection Algorithm**
   - When text changes, gets the cursor position
   - Searches backwards from cursor position to find the nearest markdown heading
   - Extracts the heading text (without `#` symbols)
   - Updates the UI with the section name

3. **Refresh Flow**
   ```
   User edits → Section detected → Refresh enabled → 
   User clicks refresh → Content saved → Similarity recalculated → 
   Results updated → Refresh disabled
   ```

## Usage Example

### Scenario: Editing a Machine Learning Note

1. **Load Target File**
   - Click "Select Target File" 
   - Choose your markdown note (e.g., `machine_learning.md`)

2. **Select Comparison Files**
   - Click "Select Directory" or "Select Files"
   - Choose files to compare against

3. **Initial Calculation**
   - Click "Calculate Similarity"
   - Review the results

4. **Edit Content**
   - Make changes in the target file editor
   - For example, add content under "# Neural Networks" section
   - The label updates: `📝 Edited: Neural Networks`

5. **Refresh and Recalculate**
   - Click the "🔄 Refresh" button
   - The system saves your changes and recalculates
   - Status bar shows: `Recalculating similarity (edited section: Neural Networks)...`
   - New results appear, potentially highlighting files with similar "Neural Networks" content

## Technical Implementation

### New Properties

```python
class MarkdownSimilarityGUI(QMainWindow):
    def __init__(self):
        # ... existing code ...
        self.last_edit_section = None      # Track edited section
        self.last_target_content = ""       # Track content changes
```

### New UI Components

1. **Refresh Button**
   ```python
   self.refresh_btn = QPushButton("🔄 Refresh")
   self.refresh_btn.setEnabled(False)
   self.refresh_btn.setToolTip("Recalculate similarity (detects recent edits)")
   ```

2. **Edit Detection Label**
   ```python
   self.edit_detection_label = QLabel("")
   self.edit_detection_label.setStyleSheet("color: #FF9800; font-style: italic;")
   ```

### Key Functions

1. **`on_target_content_changed()`**
   - Triggered when text in the editor changes
   - Detects cursor position and finds the section
   - Updates UI with edit information
   - Enables the refresh button

2. **`find_section_at_position(content, position)`**
   - Takes content string and cursor position
   - Searches backwards for markdown headings
   - Returns the heading text or None

3. **`refresh_calculation()`**
   - Saves edited content to file
   - Shows appropriate status messages
   - Calls the standard similarity calculation
   - Resets edit detection state

## Benefits

### For Users
- **Quick Iterations**: Edit and recalculate without leaving the GUI
- **Context Awareness**: Know exactly which section you edited
- **Efficient Workflow**: No need to manually save files or reload
- **Visual Feedback**: Clear indicators of edit state and location

### For Development
- **Modular Design**: New functionality doesn't break existing features
- **Reusable Logic**: Section detection can be extended for other features
- **Clear State Management**: Edit state is tracked and reset appropriately

## Future Enhancements

### Potential Improvements

1. **Section-Focused Comparison**
   - Only recalculate similarity for the edited section
   - Show section-specific similarity scores
   - Highlight changes in the edited section

2. **Multi-Section Tracking**
   - Track all edited sections in a session
   - Show a list of modified sections
   - Allow selective recalculation

3. **Undo/Redo Support**
   - Integrate with editor undo/redo
   - Track edit history per section
   - Allow reverting to previous states

4. **Auto-Save**
   - Periodically save changes automatically
   - Show save status indicator
   - Prevent data loss

5. **Diff Visualization**
   - Show what changed between versions
   - Highlight differences in the editor
   - Compare before/after similarity scores

## Testing

### Manual Testing Steps

1. **Test Edit Detection**
   - Load a markdown file with multiple sections
   - Edit text under different headings
   - Verify the correct section name appears

2. **Test Refresh**
   - Make edits
   - Click refresh button
   - Verify file is saved and similarity recalculated
   - Check status messages

3. **Test Edge Cases**
   - Edit before any heading (should show generic message)
   - Edit with nested headings (`##`, `###`)
   - Make multiple edits in different sections
   - Test with empty files

## Code Changes Summary

### Modified Files
- `gui.py`: Added edit detection and refresh functionality

### New Methods
- `on_target_content_changed()`: Detects and tracks edits
- `find_section_at_position()`: Identifies the current section
- `refresh_calculation()`: Handles refresh button click

### Modified Methods
- `__init__()`: Added new state variables
- `init_ui()`: Added refresh button and edit label
- `load_target_content()`: Initializes edit tracking
- `on_calculation_finished()`: Shows edit context in status

### UI Changes
- Target content editor is now editable (`setReadOnly(False)`)
- Added refresh button next to target file selector
- Added edit detection label in content panel
- Enhanced status messages with edit context

## Compatibility

- **Backward Compatible**: All existing features work as before
- **No Breaking Changes**: Existing workflows are unaffected
- **Optional Feature**: Users can ignore edit detection and use as before

## Performance

- **Minimal Overhead**: Edit detection is lightweight
- **No Performance Impact**: Section detection is O(n) where n is cursor line
- **Efficient Updates**: Only tracks changes when content actually modified
