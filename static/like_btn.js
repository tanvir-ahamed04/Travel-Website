let liked = false; // Track whether the post is liked

// Function to toggle like
function toggleLike(button) {
    const postId = button.dataset.postId; // Assuming you set a data attribute on the button

    fetch('/toggle_like', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ post_id: postId }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            liked = !liked; // Toggle the liked state
            const likeCountElement = button.querySelector('.like-count');
            const currentLikes = parseInt(likeCountElement.textContent) || 0;

            if (data.action === 'added') {
                likeCountElement.textContent = currentLikes + 1;
            } else {
                likeCountElement.textContent = currentLikes - 1;
            }
        } else {
            alert('Error toggling like');
        }
    });
}

// Load like count on page load
document.addEventListener('DOMContentLoaded', () => {
    const postId = document.querySelector('.like-btn').dataset.postId; // Adjust selector as needed
    fetch(`/get_like_count/${postId}`)
        .then(response => response.json())
        .then(data => {
            const likeCountElement = document.querySelector('.like-count');
            likeCountElement.textContent = data.count || 0; // Initialize like count
        });
});

// Function to submit a comment
function submitComment(postId) {
    const commentInput = document.querySelector(`#comment-input-${postId}`);
    const commentText = commentInput.value;

    fetch('/submit_comment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ post_id: postId, comment: commentText }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Add new comment to the comment section
            const commentList = document.querySelector(`#comment-list-${postId}`);
            const newComment = document.createElement('li');
            newComment.textContent = commentText; // Optionally include user info
            commentList.appendChild(newComment);
            commentInput.value = ''; // Clear the input field
        } else {
            alert('Error submitting comment');
        }
    });
}
