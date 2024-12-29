# Ollama Dashboard

A lightweight, personal dashboard for monitoring your locally running Ollama models. Built with Flask and designed for simplicity.

## Purpose

Ollama Watch provides a clean, minimal web interface to:
- View all your running Ollama models in one place
- Monitor model details like family, parameters, and quantization
- Track model sizes and expiration times
- Auto-refresh every 30 seconds to keep information current

## Features

- 🎯 Simple, single-purpose design
- 🔄 Auto-refreshing dashboard
- 🎨 Dark mode interface
- 📱 Responsive layout
- 0️⃣ Zero configuration needed

## Prerequisites

- Python 3.x
- Ollama running locally

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/poiley/ollama-watch.git
cd ollama-dashboard
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the dashboard:
```bash
python main.py
```

4. Open your browser and visit `http://localhost:5000`

## Note

This is a personal utility tool designed for individual use. It's intentionally kept simple and assumes Ollama is running on the same machine. Perfect for developers who want a quick visual overview of their currently running Ollama models. 