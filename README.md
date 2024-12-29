# Ollama Dashboard

A lightweight, personal dashboard for monitoring your locally running Ollama models. Built with Flask and designed for simplicity.

![Screenshot of Ollama Process Status UI](static/screenshot.png)

## Purpose

Ollama Dashboard provides a clean, minimal web interface to:

 - View all your running Ollama models in one place
 - Monitor model details like family, parameters, and quantization
 - Track model sizes and expiration times
 - View historical model usage
 - Auto-refresh every 30 seconds to keep information current

## Features

- 🎯 Simple, single-purpose design
- 🔄 Auto-refreshing dashboard
- 🎨 Dark mode interface
- 📱 Responsive layout
- 📋 Model history tracking
- 🕒 Real-time status indicators
- 0️⃣ Zero configuration needed

### Dashboard Features

- Real-time model status monitoring
- Detailed model information including:
  - Model family and version
  - Parameter size
  - Quantization level
  - Model size (adaptive units)
  - Expiration time (when applicable)
- Status indicator showing Ollama connection state
- Clear error messages when Ollama is not running

### History Tracking

- Sidebar with historical model usage
- Timestamps for all model runs
- Duration tracking for model sessions
- Preserves model details for reference

## Prerequisites

- Python 3.x
- Ollama running locally

## Quick Start

1. Clone the repository:

```bash
git clone https://github.com/poiley/ollama-dashboard.git
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


## Testing

The dashboard includes test routes to preview different states:

- `/test/no-models` - Preview empty state
- `/test/error` - Preview error state when Ollama isn't running
- `/test/with-models` - Preview dashboard with sample models

## Note

This is a personal utility tool designed for individual use. It's intentionally kept simple and assumes Ollama is running on the same machine. Perfect for developers who want a quick visual overview of their currently running Ollama models.
