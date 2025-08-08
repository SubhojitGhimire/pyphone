# PyPhone: A Mobile OS Simulator in Python

![Python](https://img.shields.io/badge/Python-3.10-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

Welcome to PyPhone, a fully-featured mobile operating system simulator built from the ground up using Python and the PySide6 framework. This project serves as a comprehensive portfolio piece demonstrating advanced GUI development, modular application architecture, and the integration of various programming concepts into a single, cohesive, and visually appealing application.

<p align="center">
<img src="https://github.com/user-attachments/assets/c0228828-e18e-40c9-a379-9291bd9e48c7" />
</p>

---

## Features
1. Core System Features
   - Modern UI: A sleek, dark/light theme-able user interface inspired by modern mobile operating systems.
   - Homescreen & App Dock: A functional homescreen with a live clock, date, and a dock for essential apps.
   - App Drawer: A dynamic app drawer that automatically discovers and displays all installed applications.
   - Persistent Settings: A powerful settings app that allows for global customization of the theme (Light/Dark), font, clock format, and homescreen wallpaper (image or solid color). All settings are saved and loaded on startup.

2. Included Apps
   - Utilities:
       - Planner: A robust planner with a daily to-do list and a separate, full-featured event planner integrated with a calendar view.
       - Clock: A multi-function clock with a World Clock (handling multiple timezones), a precise Stopwatch, and a countdown Timer.
       - Weather: A live weather app that fetches data (temperature, humidity, wind, AQI, etc.) for any city in the world using the OpenWeatherMap API.
       - Calculator: A standard calculator for basic arithmetic.
       - Calendar: A simple, beautifully styled full-screen calendar viewer.
       - Notes: A persistent notes application for saving and editing text.
   - Media & Tools:
       - Web Browser: A functional web browser powered by the Chromium engine, complete with navigation controls and a progress bar.
       - Photos Gallery: A gallery that displays all images from a designated folder in a thumbnail grid, with a full-size image viewer.
   - Games:
       - Chess: A professional-grade chess application powered by **Stockfish Engine** featuring multiple board themes, PGN import/export, move history, and gameplay against another player or a powerful AI.
       - Paper Plane Pilot: A "Flappy Bird" style arcade game with custom graphics and scoring.
       - Brick Breaker: The classic arcade game with mouse controls, a scoring system, and game states.
       - Snake: The timeless classic, built with a custom game loop and keyboard controls.

## Requirements
```
PySide6==6.9.1
PyQtWebEngine==5.15.7
python-chess==1.999
requests==2.32.4
psutil==7.0.0
pytz==2025.2
PyQt6-WebEngine==6.9.0
PyQt6==6.9.1
PyQt5==5.15.11
PyAutoGUI==0.9.54
```

### Setup the Chess AI (Optional): 
The Stockfish chess engine is not included in this repository due to its large file size (exceeding GitHub's upload limit of 25MB). If you want to play chess against the AI, you must install the engine manually.
```
Go to the Stockfish official download page. https://stockfishchess.org/download/
Download the appropriate version for your system (e.g., "Windows (64-bit AVX2)").
Unzip the downloaded file.
Find the executable file inside (e.g., stockfish-windows-x86-64-avx2.exe).
Copy this executable file into the root directory of this project.
Rename the executable to stockfish.exe
```
The app will work without this step, but only in "Player vs. Player" mode.

### Compile Qt Resources
This project uses a Qt Resource file (.qrc) to bundle assets like icons and wallpapers. After adding any new assets, you must compile it by running:
```bash
pyside6-rcc resources.qrc -o resources_rc.py
```

## Run the Application
```bash
python main.py
```

## Screenshots

<img src="https://github.com/user-attachments/assets/72008175-30c9-407d-a35f-2871154bf0b1" />
<br>
<img src="https://github.com/user-attachments/assets/c2a3e6ab-cce5-4723-8faa-fc33b39e2047" />

<h1></h1>

**This README.md file has been improved for overall readability (grammar, sentence structure, and organization) using AI tools.*
