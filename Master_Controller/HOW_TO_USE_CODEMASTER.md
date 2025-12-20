# 🤖 How to Use CodeMaster

**Status:** ✅ Running (PID: 99618)
**Location:** Menu bar (top-right of your screen)

---

## 👀 WHERE TO LOOK

CodeMaster is a **menu bar application**. Look for the **🤖 robot emoji** at the **TOP-RIGHT** of your screen, near:
- WiFi icon
- Battery icon
- Clock/time
- Spotlight icon

### It looks like this: 🤖

**Not in the Dock!** CodeMaster doesn't appear in the Dock - it lives in the menu bar.

---

## 🚀 LAUNCHING CODEMASTER

### Method 1: Double-Click Launcher (EASIEST)
In Finder, go to:
```
/Users/daniel/Documents/aicode/Master/
```

Double-click: **LAUNCH_CODEMASTER.command**

This will:
- Stop any old instances
- Start CodeMaster fresh
- Show you the status
- Tell you to look for 🤖 in menu bar

### Method 2: Open the App
1. Press `Cmd+Space` (Spotlight)
2. Type: `CodeMaster`
3. Press Enter
4. Look for 🤖 in menu bar

### Method 3: From Applications
1. Open Finder
2. Go to Applications folder
3. Double-click CodeMaster.app
4. Look for 🤖 in menu bar

---

## ✅ VERIFYING IT'S RUNNING

### Check if Process is Running:
Open Terminal and run:
```bash
ps aux | grep "codemaster" | grep -v grep
```

You should see:
```
daniel  99618  ... Python codemaster.py
```

### Check Menu Bar:
Run this in Terminal:
```bash
osascript -e 'tell application "System Events" to tell process "Python" to get name of menu bar 1'
```

Should return: `Menu bar found`

---

## 🎯 USING CODEMASTER

Once you see the 🤖 icon:

### 1. Click the 🤖 Icon
You'll see a dropdown menu with options:

```
🤖 CodeMaster
├── ✨ Quick Code Generation
├── 💼 Work Projects
├── 🏗️ New Project
├── 🤖 Automation Bots
├── 📋 Templates
├── 🛠️ Utilities
├── ⚙️ Settings
├── 📖 Help
├── ℹ️ About CodeMaster
└── 🚪 Quit CodeMaster
```

### 2. Try Your First Action

**Generate a Function:**
1. Click 🤖
2. Select: `✨ Quick Code Generation > 🎯 Generate Function`
3. A dialog will appear asking for a description
4. Type: "Calculate factorial of a number"
5. Click OK
6. Wait 5-10 seconds (Ollama is thinking)
7. Code appears in TextEdit or VSCode!
8. File saved to: `/Users/daniel/Documents/aicode/Master/output_[timestamp].py`

---

## 🔧 TROUBLESHOOTING

### I Don't See the 🤖 Icon!

**Solution 1: Check if it's hidden**
- Your menu bar might be too full
- Try closing other menu bar apps
- The icon might be hidden - click the `>>` symbol in menu bar to see hidden items

**Solution 2: Check permissions**
1. Open System Settings
2. Go to: Privacy & Security > Accessibility
3. Make sure Python has permission
4. If not, click `+` and add: `/Library/Frameworks/Python.framework/Versions/3.14/Resources/Python.app`

**Solution 3: Restart CodeMaster**
```bash
# In Terminal:
pkill -f codemaster
sleep 2
open /Applications/CodeMaster.app
```

Or double-click: `LAUNCH_CODEMASTER.command` in Master folder

### CodeMaster Won't Launch

**Check Dependencies:**
```bash
python3 -c "import rumps; print('✅ rumps OK')"
python3 -c "import ollama; print('✅ ollama OK')"
```

**Reinstall if needed:**
```bash
pip3 install --upgrade rumps ollama
```

### Menu Bar Icon Appears but Clicking Does Nothing

This usually means a permission issue.

1. Open System Settings
2. Privacy & Security > Automation
3. Allow Terminal/Python to control System Events
4. Restart CodeMaster

---

## 📊 CURRENT STATUS

```
✅ CodeMaster Process: Running (PID 99618)
✅ Menu Bar: Active
✅ Data Directory: /Users/daniel/Documents/aicode/Master/
✅ Work Reference: /Users/daniel/Documents/aicode/Work/
✅ Ollama Model: llama3.1
✅ Dependencies: Installed
```

---

## 🎨 WHAT THE ICON LOOKS LIKE

The CodeMaster app has a cute robot icon:
- In Applications folder: Full icon (purple robot with antenna)
- In menu bar: 🤖 emoji

**Remember:** It's at the **TOP-RIGHT** of your screen, not in the Dock!

---

## 🆘 QUICK COMMANDS

### Start CodeMaster:
```bash
open /Applications/CodeMaster.app
```

### Stop CodeMaster:
```bash
pkill -f codemaster
```

### Check if Running:
```bash
ps aux | grep codemaster | grep -v grep
```

### View Logs:
```bash
cat /tmp/codemaster.log
```

### Restart CodeMaster:
```bash
pkill -f codemaster && sleep 2 && open /Applications/CodeMaster.app
```

---

## 💡 TIPS

1. **Look in the right place:** Menu bar TOP-RIGHT, not Dock
2. **Check hidden icons:** Click `>>` in menu bar if you don't see 🤖
3. **Use the launcher:** Double-click LAUNCH_CODEMASTER.command for easy start
4. **Check permissions:** System Settings > Privacy if it's not working
5. **Generated files:** All saved to Master folder automatically

---

## 📁 FILES SAVED TO

All generated code goes here:
```
/Users/daniel/Documents/aicode/Master/
├── output_[timestamp].py      (Generated code)
├── temp_input_[timestamp].txt  (Temporary files)
└── [other generated files]
```

---

## ✨ NEXT STEPS

1. Find the 🤖 icon in your menu bar
2. Click it to see the menu
3. Try generating a function
4. Explore the Work Projects menu
5. Use automation bots

---

**CodeMaster is running RIGHT NOW!**

Look at the top-right of your screen for 🤖 and click it!

If you still can't find it, run this and send me the output:
```bash
osascript -e 'tell application "System Events" to get name of every process' | grep -i python
ps aux | grep codemaster
```

---

*Last Updated: October 20, 2025 at 2:36 PM*
*Process ID: 99618*
*Status: Running ✅*
