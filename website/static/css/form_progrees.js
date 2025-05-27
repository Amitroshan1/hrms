document.addEventListener('DOMContentLoaded', function () {
  const form = document.querySelector('form');
  if (!form) {
    console.log("No form found");
    return;
  }

  const inputs = form.querySelectorAll('input, select, textarea');
  const progressBar = document.getElementById('formProgressBar');

  console.log("Total inputs found:", inputs.length); // ✅ debug

  function updateProgress() {
    let filledCount = 0;
    let totalCount = 0;

    inputs.forEach(input => {
      if (input.type === 'hidden' || input.type === 'submit' || input.disabled) return;
      totalCount++;

      if (input.type === 'file') {
        if (input.files.length > 0) filledCount++;
      } else if (input.value.trim() !== "") {
        filledCount++;
      }
    });

    console.log(`Filled: ${filledCount}, Total: ${totalCount}`); // ✅ debug

    const percentage = Math.round((filledCount / totalCount) * 100);
    progressBar.style.width = percentage + "%";
    progressBar.textContent = percentage + "%";
  }

  inputs.forEach(input => {
    input.addEventListener('input', updateProgress);
    input.addEventListener('change', updateProgress);
  });

  updateProgress(); // Initial call
});
