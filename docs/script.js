const url = 'timeline_en.pdf'; // Replace with your PDF path
const canvas = document.getElementById('pdf-canvas');
const ctx = canvas.getContext('2d');

pdfjsLib.getDocument(url).promise.then(pdf => {
  pdf.getPage(1).then(page => {
    // Fit to height
    const containerHeight = window.innerHeight;
    const viewport = page.getViewport({ scale: 1 });
    const scale = containerHeight / viewport.height;

    const fitViewport = page.getViewport({ scale: scale });
    canvas.width = fitViewport.width;
    canvas.height = fitViewport.height;

    page.render({
      canvasContext: ctx,
      viewport: fitViewport
    }).promise.then(() => {
      // Enable pan & zoom after rendering
      const panzoom = Panzoom(canvas, {
        maxScale: 1000, // allow huge zoom
        minScale: 0.1,
        contain: 'outside'
      });

      // Allow pinch zoom
      canvas.parentElement.addEventListener('wheel', panzoom.zoomWithWheel);
    });
  });
});
