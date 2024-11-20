# Minesweeper AI

An AI that plays Minesweeper using propositional logic to make safe moves whenever possible. Part of the CS50's Introduction to Artificial Intelligence with Python course.

## Description

This project implements an AI to play Minesweeper using knowledge-based agents and propositional logic. The AI keeps track of safe moves, known mines, and makes inferences about the game board based on the information it receives.

## Features

- Logical sentence-based knowledge representation
- Safe move identification
- Mine inference
- Random move capability when no safe moves are available
- Interactive GUI using Pygame

## Requirements

- Python 3.12
- Pygame library

## Installation

1. Clone the repository:
```bash
git clone [your-repository-url]
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

Run the game with:
```bash
python runner.py
```

Controls:
- Left-click: Reveal a cell
- Right-click: Flag a potential mine
- "AI Move" button: Let the AI make the next move
- "Reset" button: Start a new game

## How It Works

The AI uses the following strategies:

1. **Knowledge Representation**
   - Maintains sets of safe cells and mines
   - Uses logical sentences about groups of cells and mine counts

2. **Inference Methods**
   - Marks cells as safe or mines when conclusively proven
   - Infers new information by comparing overlapping sentences
   - Updates knowledge base after each move

3. **Move Selection**
   - Prioritizes known safe moves
   - Makes random moves only when no safe moves are available
   - Avoids known mines and previously selected cells

## File Structure

- `runner.py`: Main game interface and visualization
- `minesweeper.py`: AI implementation and game logic
- `requirements.txt`: Required Python packages
- `assets/`: Game images and fonts

## Testing

Run the test suite with:
```bash
python test_minesweeper.py
```

Tests include:
- Safe move selection
- Random move generation
- Knowledge inference
- Sentence handling

## Contributing

Feel free to submit issues and enhancement requests!

## Credits

This project was created as part of CS50's Introduction to Artificial Intelligence with Python course.

