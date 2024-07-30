document.addEventListener('DOMContentLoaded', function () {
    const showMoreButton = document.getElementById('show-more-images');
    if (showMoreButton) {
        showMoreButton.addEventListener('click', function () {
            const hiddenImages = document.querySelectorAll('.post-image.hidden');
            hiddenImages.forEach(image => image.classList.remove('hidden'));
            showMoreButton.style.display = 'none';
        });
    }
});
