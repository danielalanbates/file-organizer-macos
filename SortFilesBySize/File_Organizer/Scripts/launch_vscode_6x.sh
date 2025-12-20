#!/bin/bash

# VS Code Multi-Window Launcher Shell Script
# Alternative script-based approach for launching 6 VS Code windows

# Function to get screen dimensions
get_screen_dimensions() {
    local screen_info=$(system_profiler SPDisplaysDataType | grep -A 5 "Resolution")
    local width=$(echo "$screen_info" | grep -o '[0-9]\+ x [0-9]\+' | head -1 | cut -d' ' -f1)
    local height=$(echo "$screen_info" | grep -o '[0-9]\+ x [0-9]\+' | head -1 | cut -d' ' -f3)
    
    # Fallback to default if detection fails
    if [[ -z "$width" || -z "$height" ]]; then
        width=1920
        height=1080
    fi
    
    echo "$width $height"
}

# Function to calculate window positions for 2x3 grid
calculate_positions() {
    local screen_dims=$(get_screen_dimensions)
    local screen_width=$(echo "$screen_dims" | cut -d' ' -f1)
    local screen_height=$(echo "$screen_dims" | cut -d' ' -f2)
    
    local window_width=$((screen_width / 3))
    local window_height=$((screen_height / 2))
    
    # Menu bar height offset (approximate)
    local menu_bar_offset=25
    local usable_height=$((screen_height - menu_bar_offset))
    window_height=$((usable_height / 2))
    
    # Array to store positions: x,y,width,height
    declare -a positions
    
    # Top row
    for col in {0..2}; do
        local x=$((col * window_width))
        local y=$window_height
        positions+=("$x,$y,$window_width,$window_height")
    done
    
    # Bottom row  
    for col in {0..2}; do
        local x=$((col * window_width))
        local y=0
        positions+=("$x,$y,$window_width,$window_height")
    done
    
    printf '%s\n' "${positions[@]}"
}

# Function to launch and position a VS Code window
launch_vscode_window() {
    local position="$1"
    local window_index="$2"
    
    IFS=',' read -r x y width height <<< "$position"
    
    echo "Launching VS Code window $window_index at position ($x,$y) with size ${width}x${height}"
    
    # Launch VS Code in new window
    code --new-window &
    local vscode_pid=$!
    
    # Wait for VS Code to start
    sleep 2
    
    # Use AppleScript to position the window
    osascript <<EOF
tell application "Visual Studio Code"
    activate
    delay 1
end tell

tell application "System Events"
    tell process "Visual Studio Code"
        set frontmost to true
        try
            set position of front window to {$x, $y}
            set size of front window to {$width, $height}
        on error
            display notification "Failed to position window $window_index" with title "VS Code Launcher"
        end try
    end tell
end tell
EOF
    
    return 0
}

# Function to configure VS Code windows with terminal and chat
configure_vscode_windows() {
    echo "Configuring VS Code windows with terminal and chat panels..."
    
    osascript <<'EOF'
tell application "Visual Studio Code"
    activate
    delay 2
end tell

tell application "System Events"
    tell process "Visual Studio Code"
        set frontmost to true
        
        -- Get all VS Code windows
        set windowCount to count of windows
        
        repeat with i from 1 to windowCount
            try
                -- Focus on window
                set front window to window i
                delay 0.5
                
                -- Open terminal (Cmd+Shift+`)
                keystroke "`" using {command down, shift down}
                delay 0.3
                
                -- Open command palette to access chat
                keystroke "p" using {command down, shift down}
                delay 0.5
                type text "GitHub Copilot: Open Chat"
                delay 0.3
                key code 36 -- Enter
                delay 1
                
            on error errMsg
                display notification ("Error configuring window " & i & ": " & errMsg) with title "VS Code Launcher"
            end try
        end repeat
    end tell
end tell
EOF
}

# Main function
main() {
    echo "=== VS Code Multi-Window Launcher ==="
    echo "Preparing to launch 6 VS Code windows in a 2x3 grid..."
    
    # Check if VS Code is installed
    if ! command -v code &> /dev/null; then
        echo "Error: VS Code command 'code' not found. Please install VS Code and ensure it's in your PATH."
        exit 1
    fi
    
    # Calculate window positions
    local positions=($(calculate_positions))
    
    echo "Screen layout calculated. Launching windows..."
    
    # Launch 6 VS Code windows
    for i in {0..5}; do
        launch_vscode_window "${positions[$i]}" $((i + 1))
        sleep 1  # Brief delay between launches
    done
    
    echo "All windows launched. Configuring panels..."
    sleep 3  # Wait for all windows to be ready
    
    # Configure all windows
    configure_vscode_windows
    
    echo "=== Launch completed! ==="
    echo "6 VS Code windows have been launched and arranged in a 2x3 grid."
    echo "Each window should have terminal and chat panels open."
}

# Run main function if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi