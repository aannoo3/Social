document.addEventListener('DOMContentLoaded', function() {
    const leftArrow = document.querySelector('.left-arrow');
    const rightArrow = document.querySelector('.right-arrow');
    const carouselTrack = document.querySelector('.carousel-track');
    let currentIndex = 0;
  
    function getVisibleItems() {
      return window.innerWidth <= 768 ? 2 : 5;
    }
  
    function updateCarousel() {
      const bookWidth = document.querySelector('.book').offsetWidth + 20; // width + margins
      carouselTrack.style.transform = `translateX(-${currentIndex * bookWidth}px)`;
    }
  
    leftArrow.addEventListener('click', () => {
      if (currentIndex > 0) {
        currentIndex--;
        updateCarousel();
      }
    });
  
    rightArrow.addEventListener('click', () => {
      const maxIndex = carouselTrack.children.length - getVisibleItems();
      if (currentIndex < maxIndex) {
        currentIndex++;
        updateCarousel();
      }
    });
  
    // Reset carousel on window resize
    window.addEventListener('resize', () => {
      currentIndex = 0;
      updateCarousel();
    });
  
    // Initial update
    updateCarousel();
  });
  