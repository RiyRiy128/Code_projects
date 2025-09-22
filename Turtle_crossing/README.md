# Turtle Crossing Game

A Frogger-inspired game where a turtle must safely cross a busy road filled with moving cars.

## Description

This is an arcade-style game where the player controls a turtle trying to cross a road filled with randomly generated cars. The game features multiple levels with increasing difficulty as the player progresses.

## Features

- Player-controlled turtle character
- Randomly generated car obstacles
- Multiple difficulty levels
- Collision detection system
- Score and level tracking
- Increasing game speed with each level

## Controls

- **W Key**: Move turtle up (forward)

## Game Components

- `main.py` - Main game loop and collision detection
- `player.py` - Turtle player class and movement
- `car_manager.py` - Car generation and movement logic
- `scoreboard.py` - Level tracking and game over display

## How to Play

1. Run main.py
2. Press 'W' to move your turtle forward
3. Avoid the moving cars
4. Reach the top of the screen to advance to the next level
5. Try to achieve the highest level possible!

## Game Mechanics

- Cars move from right to left at varying speeds
- New cars are randomly generated
- Each level increases car speed
- Collision with any car ends the game
- Player resets to bottom after completing each level

## Dependencies Used

- Python
- Turtle Graphics Module
- Random module for car generation
- Object-Oriented Programming
- Game loop and event handling