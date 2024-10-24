let speed = 0; // Speed percentage, ranges from -80 (reverse) to 100 (boost)
let statusDisplay = document.getElementById('status');
let speedDisplay = document.getElementById('speed-display');
let throttleFill = document.getElementById('throttle-fill');

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
}

// Send movement commands to the Flask backend
function sendMovementCommand(direction) {
    fetch('/move', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ direction: direction, speed: speed })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

// Handle robot movement keys (W, A, S, D)
document.addEventListener('keydown', function(event) {
    let key = event.key.toLowerCase();
    switch (key) {
        case 'w':
            statusDisplay.innerText = 'Moving Forward';
            sendMovementCommand('forward');
            break;
        case 's':
            statusDisplay.innerText = 'Moving Backward';
            sendMovementCommand('reverse');
            break;
        case 'a':
            statusDisplay.innerText = 'Moving Left';
            sendMovementCommand('left');
            break;
        case 'd':
            statusDisplay.innerText = 'Moving Right';
            sendMovementCommand('right');
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
    } else if (event.key === 'ArrowDown') {
        if (speed > -80) {
            speed -= (speed > 80) ? 10 : 5; // Slower reduction when in boost mode
        }
        updateSpeedDisplay();
    }
});
