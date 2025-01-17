# Calendar Puzzle

A simple web-based puzzle solver. Choose a puzzle variant (“dvoj” or “troj”), optionally disable a few cells, and let the solver place the pieces.

## Features
- **Two puzzle variants**:  
  - **dvoj**: user can disable up to 2 cells  
  - **troj**: user can disable up to 3 cells  
- **Animated** or **blocking** solver.  
- **Dynamic grid** based on puzzle definition (with predefined disabled cells and auto-disabled “today” cells).

## Usage
1. **Open `index.html`** in your browser.
2. Under **"Druh puzzle"** choose **dvoj** or **troj**.
3. **Click** on allowable cells to toggle disable (limited by the puzzle).
4. **Check** the "Zobrazovat průběh skládání" box for an *animated* solver.
5. **Click "Hledej řešení"**. If a solution is found, pieces color the grid.

## Customization
- **Puzzle definitions** (tiles, shapes, disabled cells) live in the `puzzleDefinitions` object.
- Adjust styling in the `<style>` block (e.g., colors, cell size).

## License
[MIT](LICENSE)
