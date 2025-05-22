📌 Title

OMNITRACKER Auto Refresh GUI — Cyber Themed Productivity Tool

🧾 Description

A cyberpunk-inspired Python GUI tool that automates periodic refreshing of the OMNITRACKER Client window. It simulates a mouse click and F5 press to refresh the app at user-defined intervals. The interface features glowing neon animations, interactive logging, and a sleek gradient background.
Ideal for users who need to keep OMNITRACKER sessions alive or regularly updated without manual intervention.

🚀 Features

    ⚡ Cyber-themed GUI with animated glow effects

    ⏱ Set custom refresh intervals (in minutes)

    🖱 Auto-detect mouse coordinates for refresh clicks

    🔔 Desktop notifications upon successful refresh

    📜 Live event log in a scrollable text box

    🪟 Auto-activation of OMNITRACKER Client window

    🔒 Graceful start/stop and clean shutdown handling

🛠️ Requirements

Install dependencies:

pip install pyautogui pygetwindow win10toast


🖥️ How to Use

    Launch the App:

    python your_script_name.py

    Set Refresh Interval (in minutes).

    Get Mouse Coordinates:

        Click the 📍 Get Mouse Coordinates button.

        Within 5 seconds, hover your mouse over the spot in OMNITRACKER you want clicked.

        The coordinates will be automatically captured.

    Start Auto Refresh:

        Click ▶ Start Auto Refresh.

        The app will click and refresh OMNITRACKER at your specified interval.

    Stop the Refresh:

        Click ⏹ Stop Auto Refresh to halt the automation.


🧠 Tips

    Ensure OMNITRACKER is open and its window title is exactly "OMNITRACKER Client" (case-sensitive).

    If the app can’t find the window, it will log an error.
