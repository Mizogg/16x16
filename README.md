# 16x16
🐍16x16 Grid Hunting for Crypto🐍

BitcoinHunter 16x16 is a graphical user interface (GUI) application built in Python using the PyQt framework. The application is designed to provide various tools and features for exploring the Bitcoin blockchain and related activities.

Features
Key Space Scanning: Explore the Bitcoin key space by specifying a range of private key values. Visualize corresponding Bitcoin addresses, WIF formats, and more.

Dark Space Scanning: Perform dark space scanning to identify potential weak points in the Bitcoin key space. Utilize multiple CPU cores for efficient scanning.

Address Visualization: Visualize Bitcoin addresses and related information, including balance, transactions, total received, and total sent.

Matrix Rain Effects: Enjoy the aesthetic appeal of matrix rain effects, adding a unique visual element to the application.

Mnemonic and Brain Wallet: Generate and explore mnemonic words and brain wallets. Specify the number of words, language, and derivations to customize your exploration.

Game of Life Patterns: Discover and interact with Conway's Game of Life patterns, including popular patterns like High Life, Maze, Crystallization, and more.

Random Matrix and Matrix Rain: Experience randomly generated matrix displays and matrix rain effects for a dynamic and captivating visualization.

Forward and Backward Scanning: Scan the Bitcoin key space in both forward and backward directions with customizable step sizes.

The table generates a 256bit visual bitcoin private key represented by square 16×16 (16 bits per each line).Visualizing your private key!! Flip the genuine coin for random bit selection and use your mouse to mark any bit within a square as 1 (filled cell) or 0 (blank cell). Also includes:

    Balance Checker
    Private Key in BIN (256 digits)
    Private Key in HEX (64 digits)
    BTC address (Legacy, uncompressed, p2sh, bc1)
    BTC address (Compressed)

Bitcoin Visual PrivateKey Generator

More Info (https://mizogg.co.uk)

Requirements 

```python
pip install PyQt6
pip install simplebloomfilter
pip install bitarray==1.9.2
pip install webbrowser
pip install request
pip install mnemonic
pip install hdwallet
pip install numpy
```

![image](https://github.com/Mizogg/16x16/assets/88630056/06ff460c-add4-47bb-a4bf-08e67a349a48)

## KnightRiderWidget: Animated "Knight Rider" Lights in PyQt6

The `KnightRiderWidget` is a custom widget designed to replicate the iconic "Knight Rider" scanner animation using PyQt6. This animation showcases a series of moving lights that travel back and forth, creating a visually engaging effect.

### Features

- **Dynamic Animation:** The widget features dynamic animation of lights that glide smoothly across the widget's surface.
- **Auto-Reversal:** The lights automatically reverse their direction when reaching the edges of the widget, simulating the classic bouncing effect.
- **Customizable Color:** The color of the moving lights can be easily customized to match your application's aesthetic.


![image](https://github.com/Mizogg/16x16/assets/88630056/574841c1-626f-4346-9c62-1b58be189622)

## MatrixDrop, Smoke_up, and LavaBubble: Visual Effects for Python Applications

These classes, namely `MatrixDrop`, `Smoke_up`, and `LavaBubble`, encapsulate dynamic visual effects that can enhance the visual appeal of your Python applications. Each class represents a unique visual element with its own characteristics and animations.

### MatrixDrop Class

The `MatrixDrop` class simulates the iconic "Matrix" digital rain effect, where individual drops descend vertically down the screen. Each drop is represented by a column and a row position. The speed and appearance of each drop are randomized, creating a dynamic and engaging visual effect.

### Smoke_up Class

The `Smoke_up` class generates an upward-moving smoke effect. The smoke is characterized by its row and column position, speed, and time-to-live (TTL). The TTL defines how long the smoke particle remains visible as it moves upwards. The result is a visually appealing simulation of rising smoke.

### LavaBubble Class

The `LavaBubble` class creates animated lava bubbles that move horizontally along the screen. Each bubble is defined by its row and column position, direction, speed, size, and TTL. The bubbles have a random chance of changing direction during their movement, adding variability to the animation.

### Common Methods

For all three classes, there are common methods to control their behavior:

## Conway's Game of Life Patterns

This section of the **BitcoinHunter 16x16 Crypto Scanner** program includes an implementation of Conway's Game of Life patterns. Conway's Game of Life is a cellular automaton devised by mathematician John Horton Conway, which demonstrates how simple rules can lead to complex and fascinating behaviors.

### Overview

The program provides several predefined Game of Life patterns, including 'Conway', 'High Life', 'Maze', 'Crystallization', and 'Castle Walls'. These patterns determine the evolution of a grid of cells based on simple rules applied to each cell's neighbors.

### How it Works

1. Each cell in the grid can be in one of two states: alive (1) or dead (0).
2. For each cell, the program calculates the number of living neighbors it has.
3. Depending on the selected pattern, a lambda function is used to determine the cell's next state based on its current state and the number of neighbors.
4. The grid's state is updated according to the next state of each cell.
5. The updated grid is displayed on the screen, showcasing the progression of the chosen Game of Life pattern.

### Patterns Available

- **Conway**: The classic Game of Life pattern. Cells survive with 2 or 3 neighbors and are born with 3 neighbors.
- **High Life**: Similar to Conway's, but cells can also survive with 6 neighbors.
- **Maze**: A pattern where cells live if they have 1 to 5 neighbors.
- **Crystallization**: Cells survive with 3 or 8 neighbors, and birth occurs with 3 neighbors.
- **Castle Walls**: Cells survive with 2 or 3 neighbors, and birth occurs with 4 or 5 neighbors.

### Usage

1. Select a Game of Life pattern from the dropdown menu.
2. Adjust the scanning speed using the speed slider.
3. Watch as the grid evolves based on the selected pattern and rules.

This feature adds a touch of interactivity and visual interest to the **BitcoinHunter 16x16 Crypto Scanner** application, allowing users to explore the captivating world of cellular automata through various patterns.


![image](https://github.com/Mizogg/16x16/assets/88630056/c25ae015-fe47-4f3c-af89-2d2bbef1280b)


