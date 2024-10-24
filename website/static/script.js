let speed = 50; // Speed percentage, 0-100
let statusDisplay = document.getElementById('status');
let speedDisplay = document.getElementById('speed-display');
let throttleFill = document.getElementById('throttle-fill');

// Update speed display
function updateSpeedDisplay() {
    speedDisplay.innerText = `${speed}%`;
    throttleFill.style.height = `${speed}%`;
}

// Handle robot movement keys (W, A, S, D)
document.addEventListener('keydown', function(event) {
    let key = event.key.toLowerCase();
    switch (key) {
        case 'w':
            statusDisplay.innerText = 'Moving Forward';
            break;
        case 's':
            statusDisplay.innerText = 'Moving Backward';
            break;
        case 'a':
            statusDisplay.innerText = 'Moving Left';
            break;
        case 'd':
            statusDisplay.innerText = 'Moving Right';
            break;
    }
});

// Handle speed control with arrow keys
document.addEventListener('keydown', function(event) {
    if (event.key === 'ArrowUp') {
        if (speed < 100) {
            speed += 5;
        }
        updateSpeedDisplay();
    } else if (event.key === 'ArrowDown') {
        if (speed > 0) {
            speed -= 5;
        }
        updateSpeedDisplay();
    }
});
