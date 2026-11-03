// If an image file hasn't been added yet, show a hatched frame with the
// expected file path instead of a broken-image icon.
document.querySelectorAll('.view img').forEach((img) => {
  const frame = img.closest('.view');
  const mark = () => {
    frame.classList.add('is-missing');
    frame.dataset.missing = 'Image not added yet: ' + img.getAttribute('src');
  };
  if (img.complete && img.naturalWidth === 0) mark();
  else img.addEventListener('error', mark);
});

// Keep the footer year current.
document.querySelectorAll('[data-year]').forEach((el) => {
  el.textContent = new Date().getFullYear();
});
