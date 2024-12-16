// Register ScrollTrigger plugin
gsap.registerPlugin(ScrollTrigger);

// Smooth unified animation for "coming from top to down"
gsap.fromTo(
  '.card-group', 
  {
    opacity:0, 
    // scale: 0.6, 
    y: -100 // Starting position and scale
  }, 
  {
    opacity: 1,
    // scale: 1, 
    // x: 30, 
    y: 30, // End position
    duration: 3,
    ease: 'power2.out', // Use a smooth easing function
    scrollTrigger: {
      trigger: '.cardtitles',
      start: 'top 80%', // When it enters viewport
      end: 'bottom 50%', // When the animation should finish
      scrub: 1, // Smoother scrolling
      markers: true // Debugging markers
    }
  }
);
