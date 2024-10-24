document.addEventListener('DOMContentLoaded', () => {
    let speed = 0; // Speed percentage, ranges from -80 (reverse) to 100 (boost)
    const statusDisplay = document.getElementById('status');
    const speedDisplay = document.getElementById('speed-display');
    const throttleFill = document.getElementById('throttle-fill');

    // Function to send command to the server
    function sendCommand(command) {
        const url = `/control_motor?command=${command}&speed=${Math.abs(speed)}`;
        fetch(url, { method: 'GET' })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'error') {
                    console.error('Error:', data.message);
                }
            })
            .catch(error => console.error('Error:', error));
    }

    // Function to trigger LED blinking
    function triggerLedBlink(duration = 1, blinkCount = 5) {
        const url = `/blink_led?duration=${duration}&blink_count=${blinkCount}`;
        fetch(url, { method: 'GET' })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'error') {
                    console.error('Error:', data.message);
                } else {
                    console.log('LED blinking initiated');
                }
            })
            .catch(error => console.error('Error:', error));
    }

    // Update speed display
    function updateSpeedDisplay() {
        if (speed > 0 && speed <= 80) {
            speedDisplay.innerText = `${speed}% (Normal)`;
            throttleFill.style.backgroundColor = "#00cc66"; // Green for normal forward
        } else if (speed > 80) {
            speedDisplay.innerText = `${speed}% (Boost)`;
            throttleFill.style.backgroundColor = "#ffcc00"; // Yellow for boost
        } else if (speed < 0) {
            speedDisplay.innerText = `${Math.abs(speed)}% (Reverse)`;
            throttleFill.style.backgroundColor = "#cc3333"; // Red for reverse
        } else {
            speedDisplay.innerText = `0% (Neutral)`;
            throttleFill.style.backgroundColor = "#00cc66"; // Neutral state
        }

        // Adjust the throttle fill position and height
        if (speed >= 0) {
            throttleFill.style.height = `${speed}%`;
            throttleFill.style.bottom = `50%`;
        } else {
            throttleFill.style.height = `${Math.abs(speed)}%`;
            throttleFill.style.bottom = `calc(50% - ${Math.abs(speed)}%)`;
        }

        // Send the updated speed to the server
        sendCommand('adjust_speed');
    }

    // Handle robot movement keys (W, A, S, D)
    document.addEventListener('keydown', function(event) {
        let key = event.key.toLowerCase();
        switch (key) {
            case 'w':
                statusDisplay.innerText = 'Moving Forward';
                sendCommand('forward');
                triggerLedBlink();
                break;
            case 's':
                statusDisplay.innerText = 'Moving Backward';
                sendCommand('reverse');
                triggerLedBlink();
                break;
            case 'a':
                statusDisplay.innerText = 'Moving Left';
                sendCommand('left');
                triggerLedBlink();
                break;
            case 'd':
                statusDisplay.innerText = 'Moving Right';
                sendCommand('right');
                triggerLedBlink();
                break;
            case ' ': // Space key for stop
                statusDisplay.innerText = 'Stopped';
                sendCommand('stop');
                triggerLedBlink(2, 10); // Longer blink for stop
                break;
        }
    });

    // Handle speed control with arrow keys
    document.addEventListener('keydown', function(event) {
        if (event.key === 'ArrowUp') {
            if (speed < 100) {
                speed += (speed >= 80) ? 10 : 5; // Boost mode after 80%
                if (speed > 100) speed = 100; // Cap at 100% boost
            }
            updateSpeedDisplay();
            triggerLedBlink(0.5, 3); // Short blink for speed increase
        } else if (event.key === 'ArrowDown') {
            if (speed > -80) {
                speed -= (speed > 80) ? 10 : 5; // Slower reduction when in boost mode
            }
            updateSpeedDisplay();
            triggerLedBlink(0.5, 3); // Short blink for speed decrease
        }
    });

    // Handle button clicks for motor control (if buttons are present in HTML)
    const forwardBtn = document.getElementById('forward');
    const leftBtn = document.getElementById('left');
    const rightBtn = document.getElementById('right');
    const stopBtn = document.getElementById('stop');

    if (forwardBtn) forwardBtn.onclick = () => { sendCommand('forward'); statusDisplay.innerText = 'Moving Forward'; triggerLedBlink(); };
    if (leftBtn) leftBtn.onclick = () => { sendCommand('left'); statusDisplay.innerText = 'Moving Left'; triggerLedBlink(); };
    if (rightBtn) rightBtn.onclick = () => { sendCommand('right'); statusDisplay.innerText = 'Moving Right'; triggerLedBlink(); };
    if (stopBtn) stopBtn.onclick = () => { sendCommand('stop'); statusDisplay.innerText = 'Stopped'; triggerLedBlink(2, 10); };

    // Initialize speed display
    updateSpeedDisplay();
});