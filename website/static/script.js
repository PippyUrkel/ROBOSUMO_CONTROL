document.addEventListener('DOMContentLoaded', () => {
    const speedControl = document.getElementById('speed');
    let currentSpeed = 50;

    function sendCommand(command) {
        fetch(`/control_motor`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                command: command,
                speed: currentSpeed
            })
        });
    }

    // Handle button clicks for motor control
    document.getElementById('forward').onclick = () => sendCommand('forward');
    document.getElementById('left').onclick = () => sendCommand('left');
    document.getElementById('right').onclick = () => sendCommand('right');
    document.getElementById('stop').onclick = () => sendCommand('stop');

    // Handle speed adjustment
    window.updateSpeed = (speed) => {
        currentSpeed = speed;
        document.getElementById('speedValue').innerText = speed;
        sendCommand('adjust_speed');  // Adjust speed while running
    };
});
