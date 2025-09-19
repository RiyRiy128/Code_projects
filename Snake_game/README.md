# Snake Game

A classic Snake game implementation with high score tracking and modern features.

## Description

This is a recreation of the classic Snake game where the player controls a snake to eat food and grow longer while avoiding collisions with walls and the snake's own body. Features include high score persistence and smooth gameplay.

## Features

- Classic Snake gameplay mechanics
- Food generation and consumption
- Collision detection (walls and self)
- High score tracking with file persistence
- Snake growth mechanics
- Smooth controls and movement

## Controls

- **Arrow Keys**: Control snake direction
  - Up Arrow: Move up
  - Down Arrow: Move down
  - Left Arrow: Move left
  - Right Arrow: Move right

## Game Components

- `main.py` - Main game loop and setup
- `snake.py` - Snake class with movement and growth logic
- `Food.py` - Food generation and positioning
- `scoreboard.py` - Score tracking and high score management
- `data.txt` - High score persistence file

## How to Play

1. Run main.py
2. Use arrow keys to control the snake
3. Eat the food to grow and increase your score
4. Avoid hitting walls or the snake's body
5. Try to beat your high score!

## Game Mechanics

- Snake grows longer each time it eats food
- Game resets (not ends) when collision occurs
- High score is saved and persists between sessions
- Speed remains constant for consistent gameplay

## Dependencies Used

- Python
- Turtle Graphics Module
- File I/O for high score persistence
- Object-Oriented Programming