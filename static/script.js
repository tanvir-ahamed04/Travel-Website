// navagetion menu
const hamburger = document.querySelector('.hamburger');
const navLinks = document.querySelector('.nav-links');

hamburger.addEventListener('click', () => {
    navLinks.classList.toggle('active');
});


// Ensure that the DOM is fully loaded before executing the script
document.addEventListener("DOMContentLoaded", function() {
    // Initialize Typed.js for the typing effect
    // Initialize Typed.js for the typing effect
var typed = new Typed(".typing", {
    strings: ["Where will your next adventure take you?", "Embark on a journey to uncover the world's hidden gems! "], // Add multiple strings if needed
    typeSpeed: 100,       // Speed of typing
    backSpeed: 60,        // Speed of erasing
//    backDelay: 1000,      // Delay before starting to erase
//    smartBackspace: true,  // Backspace smarter, skips already typed characters
    loop: true,           // Loop the typing effect
});

});


// scrooling bg

window.addEventListener("scroll", function() {
    const header = document.querySelector("header");
    if (window.scrollY > 50) {  // If the scroll position is greater than 50px
        header.classList.add("scrolled"); // Add the 'scrolled' class
        header.style.color = "white"; // Change text color to white
    } else {
        header.classList.remove("scrolled"); // Remove the 'scrolled' class
        header.style.color = ""; // Reset text color
    }
});



//   click to show 
document.getElementById("howItWorksToggle").addEventListener("click", function() {
    toggleContent("howItWorksContent");
});

document.getElementById("localExpertsToggle").addEventListener("click", function() {
    toggleContent("localExpertsContent");
});

document.getElementById("whatsIncludedToggle").addEventListener("click", function() {
    toggleContent("whatsIncludedContent");
});

function toggleContent(contentId) {
    // Get all content elements
    const contents = document.querySelectorAll('.content');

    // Hide all contents
    contents.forEach(content => {
        if (content.id !== contentId) {
            content.style.display = 'none';
        }
    });

    // Toggle the clicked content
    const contentToToggle = document.getElementById(contentId);
    contentToToggle.style.display = contentToToggle.style.display === 'block' ? 'none' : 'block';
}











