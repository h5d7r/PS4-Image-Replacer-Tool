# PS4 AppMeta Manager

An advanced, GUI-driven Python utility designed to seamlessly customize PlayStation 4 game graphics directly via FTP. Automates the resizing and formatting of images to ensure perfect compatibility with the PS4's AppMeta structure.

**Developer:** Mr. Velox  
**Telegram Support:** [@C2_9H](https://t.me/C2_9H)

## Core Features

* **Intuitive Graphic Interface**: Built with Tkinter, featuring a clean, tabbed workflow and dynamic status tracking.
* **Live Image Preview**: Visual feedback of the selected asset before deployment.
* **Automated Image Rendering**: 
  * External logic automatically conforms assets to `512x512` mapping for `icon0.png`.
  * Internal logic automatically conforms assets to `1920x1080` mapping for both `pic0.png` and `pic1.png`.
* **Direct Memory Injection**: Bypasses local file saving. Images are processed in RAM and directly streamed to the console.
* **Persistent Configuration**: Save your console IP and FTP Port locally to streamline future sessions.

## Prerequisites

1. A computer with Python 3.8 or higher installed.
2. A jailbroken PS4 running an active FTP payload (e.g., GoldHEN).
3. Both the PC and PS4 must be operating on the same local network subnet.

## Deployment Instructions

1. Extract the tool files to a dedicated directory.
2. Open your command line interface within that directory.
3. Install the required dependencies:
   ```cmd
   pip install -r requirements.txt# PS4-Image-Replacer-Tool
