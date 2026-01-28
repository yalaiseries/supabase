// Custom cursor effect - motion.page style
// Optimized for zero latency with GPU acceleration
(function() {
  // Only enable on non-touch devices
  if ('ontouchstart' in window || navigator.maxTouchPoints > 0) {
    console.log('Touch device detected, custom cursor disabled');
    return;
  }

  // Wait for DOM to be ready
  function initCursor() {
    const cursor = document.createElement('div');
    const cursorDot = document.createElement('div');
    cursor.className = 'cursor active'; // Start visible
    cursorDot.className = 'cursor-dot active'; // Start visible
    document.body.appendChild(cursor);
    document.body.appendChild(cursorDot);
    
    // Only hide default cursor after custom cursor is ready
    setTimeout(() => {
      document.body.classList.add('custom-cursor');
      document.body.classList.add('cursor-ready');
    }, 100);

    let mouseX = 0, mouseY = 0;
    let cursorX = 0, cursorY = 0;
    const speed = 0.15; // Smooth trailing effect

    // Update mouse position
    document.addEventListener('mousemove', (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
      // Dot follows instantly
      cursorDot.style.transform = `translate(${mouseX - 4}px, ${mouseY - 4}px)`;
    });

    // Smooth animation for trailing circle
    function animate() {
      const dx = mouseX - cursorX;
      const dy = mouseY - cursorY;
      
      cursorX += dx * speed;
      cursorY += dy * speed;
      
      cursor.style.transform = `translate(${cursorX - 20}px, ${cursorY - 20}px)`;
      requestAnimationFrame(animate);
    }
    animate();

    // Hover effects on interactive elements
    const interactives = 'a, button, summary, .card, details, input, textarea, select';
    
    document.addEventListener('mouseover', (e) => {
      if (e.target.closest(interactives)) {
        cursor.classList.add('hover');
      }
    }, true);
    
    document.addEventListener('mouseout', (e) => {
      if (e.target.closest(interactives)) {
        cursor.classList.remove('hover');
      }
    }, true);

    // Hide cursor when leaving window
    document.addEventListener('mouseleave', () => {
      cursor.style.opacity = '0';
      cursorDot.style.opacity = '0';
    });

    document.addEventListener('mouseenter', () => {
      cursor.style.opacity = '1';
      cursorDot.style.opacity = '1';
    });
    
    console.log('Custom cursor initialized');
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initCursor);
  } else {
    initCursor();
  }
})();
