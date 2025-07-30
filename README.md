# AI Traffic Light Simulation

## Project Description

This project is a traffic light simulation built using **Pygame**, designed to explore and demonstrate concepts of **Artificial Intelligence (AI)** in managing traffic flow at an intersection. It features two distinct simulation modes: a standard timer-based approach and a more advanced queue-based, dynamic timing system. The goal is to compare and optimize traffic light timings to reduce congestion and improve vehicle throughput.

## Features

* **Pygame-based Visualization:** Interactive graphical representation of a traffic intersection.
* **Traffic Flow Simulation:** Vehicles moving through the intersection based on traffic light states.
* **Two Simulation Modes:**
    * **Standard Timer-Based (`main.py`):** Traffic lights operate on fixed, predefined timings.
    * **Queue-Based Dynamic Timing (`simu2.py`):** Traffic light durations adjust dynamically based on real-time vehicle queues at each lane, demonstrating an AI approach to traffic optimization.

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Before you begin, ensure you have the following installed:

* **Python 3.x:** Download and install from [python.org](https://www.python.org/downloads/).
* **Pygame:** Install via pip.
    ```bash
    pip install pygame
    ```

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/ibexdev-01/AI-traffic-light-simulation.git](https://github.com/ibexdev-01/AI-traffic-light-simulation.git)
    ```
2.  **Navigate into the project directory:**
    ```bash
    cd AI-traffic-light-simulation
    ```
3.  **(Optional) Create a virtual environment:**
    It's good practice to use a virtual environment to manage project dependencies.
    ```bash
    python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```
4.  **Install project dependencies:**
    *(If you have a `requirements.txt` file, use that. Otherwise, just `pygame` for now.)*
    ```bash
    pip install -r requirements.txt # If you create one later
    # OR
    pip install pygame # If pygame is the only dependency
    ```

## Running the Simulation

You can run either the standard timer-based simulation or the queue-based dynamic simulation.

### 1. Standard Timer-Based Simulation

To run the simulation with fixed traffic light timings:

```bash
python main.py