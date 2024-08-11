document.addEventListener('DOMContentLoaded', function() {
  const prevButton = document.querySelector('.prev-button');
  const nextButton = document.querySelector('.next-button');

  document.addEventListener('mousemove', function(e) {
    const x = e.clientX;
    const width = window.innerWidth;

    if (x < width * 0.25) {
      prevButton.style.opacity = '1';
      nextButton.style.opacity = '0';
    } else if (x > width * 0.75) {
      prevButton.style.opacity = '0';
      nextButton.style.opacity = '1';
    } else {
      prevButton.style.opacity = '0';
      nextButton.style.opacity = '0';
    }
  });

  document.addEventListener('mouseleave', function() {
    prevButton.style.opacity = '0';
    nextButton.style.opacity = '0';
  });
});
