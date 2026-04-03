# Emergency Network Routing and Optimization Simulator

A modern Python GUI application built with Tkinter for simulating emergency network routing operations.

## Features

- 🎨 Modern, clean UI with color-coded operations
- 📊 Real-time network graph visualization using NetworkX and Matplotlib
- 🔄 Multiple routing operations (Generate, Find Best, Simulate Failure, Sort, etc.)
- 📈 Interactive graph display with path highlighting
- 💡 Status bar for operation feedback
- ✨ Input validation and error handling

## Installation

1. Install Python 3.7 or higher

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python ui.py
```

## Usage

### Input Fields
- **Source Node**: Starting point for routing (default: A)
- **Destination Node**: End point for routing (default: F)
- **Node Failure**: Optional node to simulate failure
- **Edge Failure**: Optional edge to simulate failure (format: A-B)
- **Route Search**: Search for specific routes

### Operations
1. **Generate Routes**: Find all possible routes between source and destination
2. **Find Best Route**: Calculate shortest path using Dijkstra's algorithm
3. **Simulate Failure**: Test network resilience with node/edge failures
4. **Sort Routes**: Sort all routes by distance
5. **Find Safest Route**: Find route with maximum minimum capacity
6. **Search Route**: Search for specific route patterns
7. **Reset/Clear**: Clear all inputs and reset the display

## Future Integration

The UI is designed to integrate with:
- `network.py` - Network graph management and route generation
- `algorithm.py` - Sorting, max-min, and binary search algorithms

## Project Structure

```
.
├── ui.py              # Main GUI application
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## Technical Details

- **Framework**: Tkinter (Python standard library)
- **Visualization**: Matplotlib + NetworkX
- **Layout**: Frame-based responsive design
- **Window Size**: 1200x700 (adjustable)

## Notes

- Current implementation uses placeholder functions with dummy data
- Graph visualization shows a sample network topology
- All operations display formatted output in the output panel
- Ready for backend integration with actual routing algorithms
