document.addEventListener('DOMContentLoaded', function() {
    var seeMoreLink = document.getElementById('see-more-link');
    if (seeMoreLink) {
        var shortDescription = document.getElementById('short-description');
        var fullDescription = document.getElementById('full-description');

        seeMoreLink.addEventListener('click', function() {
            if (fullDescription.style.display === 'none') {
                fullDescription.style.display = 'block';
                shortDescription.style.display = 'none';
                seeMoreLink.textContent = 'See less product details';
            } else {
                fullDescription.style.display = 'none';
                shortDescription.style.display = 'block';
                seeMoreLink.textContent = 'See more product details';
            }
        });
    }
});
