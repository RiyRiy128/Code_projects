# US States Guessing Game

An interactive educational game that challenges players to name all 50 US states on a map.

## Description

This project is an educational geography game where players try to name all 50 US states. The game displays a blank map of the United States and prompts users to guess state names, placing them correctly on the map as they're guessed.

## Features

- Interactive US map display
- Real-time state placement as you guess
- Progress tracking (states guessed out of 50)
- Missing states export functionality
- Case-insensitive input handling
- Early exit option with progress saving

## Game Components

- `main.py` - Main game logic and user interface
- `50_states.csv` - State names with coordinates data
- `blank_states_img.gif` - Blank US map image
- `missing_states.csv` - Generated file of unguessed states (created during gameplay)

## How to Play

1. Run main.py
2. A blank US map will appear
3. Enter state names when prompted
4. Correctly guessed states will appear on the map
5. Continue until you've guessed all 50 states or type "exit" to quit
6. If you exit early, a file with missing states will be created

## Game Features

- **Progress Display**: Shows how many states you've guessed (e.g., "25/50 States guessed")
- **Smart Input**: Automatically capitalizes your input
- **Exit Anytime**: Type "exit" to quit and save your progress
- **Study Aid**: Missing states are saved to a CSV file for review

## Installation

```
pip install pandas
```

## Dependencies Used

- Python
- turtle (built-in)
- pandas

## Educational Value

Perfect for:
- Learning US geography
- Testing state knowledge
- Educational classroom activities
- Geography study sessions