# 📺 Plex Playlist Automation Scripts

This repository contains automation scripts for **managing dynamic playlists in Plex** using the Plex API.

## 🚀 Features
- 📂 **Automatically generates decade-based playlists** for unwatched movies & TV episodes.
- 🔄 **Updates existing playlists** dynamically (adds/removes content).
- ⚡ **Sorts content chronologically** for an optimal viewing order.
- 🛠️ **Fully configurable via `config.json`** (no need to modify the script).

---

## 📦 Installation & Setup

### 1️⃣ Install Dependencies
Make sure you have:
- **Python 3** → [Download Here](https://www.python.org/)
- **PlexAPI**:
- **pip install plexapi**
 
---

### 2️⃣ Clone the Repository
Run: 

    git clone https://github.com/raymcgirk/plex-scripts.git cd plex-scripts

---

### 3️⃣ Configure Your Plex Server
1. Copy the example config:

        cp config.json.example config.json

2. Edit `config.json` with your **Plex server URL & token**:
```json
{
    "plex_url": "http://YOUR_PLEX_SERVER:32400",
    "plex_token": "YOUR_PLEX_TOKEN"
}
```

### ✅ Your Plex token can be found [here.](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/)

---

### 4️⃣ Run the Script
To generate or update playlists, run:
      
      python combine_playlists.py

---

### ⚠️ Important Notes
- Only unwatched content is added to playlists.
- Watched items will be removed from the playlist, but not deleted.
- Can be automated with docker/container manager or task scheduler.

---

### 🎉 Credits
- Built by Shawn McCarthy
- Uses PlexAPI

---

### 📜 License
- Licensed under the MIT License. See LICENSE for details.
