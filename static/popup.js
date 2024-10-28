function showMessage() {
        const message = document.getElementById('success-message');
        message.style.display = 'block'; // Show the message

        // After 10 seconds, fade out the message
        setTimeout(() => {
            message.classList.add('hide'); // Add the hide class to fade out

            // Remove the message from the DOM after fade out
            setTimeout(() => {
                message.style.display = 'none'; // Hide the message completely
                message.classList.remove('hide'); // Reset the class for future use
            }, 500); // Match the duration of the CSS transition
        }, 10000); // 10 seconds
    }

    // Call the function when the page loads
    window.onload = showMessage;

