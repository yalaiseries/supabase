// Custom cursor effect - motion.page style
// Optimized for zero latency with GPU acceleration
(function() {
  // Only enable on non-touch devices
  if ('ontouchstart' in window || navigator.maxTouchPoints > 0) {
    return;
  }

  const cursor = document.createElement('div');
  const cursorDot = document.createElement('div');
  cursor.className = 'cursor';
  cursorDot.className = 'cursor-dot';
  document.body.appendChild(cursor);
  document.body.appendChild(cursorDot);
  document.body.classList.add('custom-cursor');

  let mouseX = 0, mouseY = 0;
  let cursorX = 0, cursorY = 0;
  const speed = 0.15; // Smooth trailing effect

  // Update mouse position
  document.addEventListener('mousemove', (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;
    // Dot follows instantly
    cursorDot.style.transform = `translate(${mouseX - 4}px, ${mouseY - 4}px)`;
    
    // Show cursors on first move
    if (!cursor.classList.contains('active')) {
      cursor.classList.add('active');
      cursorDot.classList.add('active');
    }
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
})();
