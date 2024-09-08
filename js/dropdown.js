// Basic JavaScript to update the selected items display (you'll likely need to enhance this)
const checkboxes = document.querySelectorAll('.dropdown-content input[type="checkbox"]');
const selectedItemsDisplay = document.querySelector('.selected-items');

checkboxes.forEach(checkbox => {
  checkbox.addEventListener('change', () => {
    updateSelectedItemsDisplay();
  });
});

function updateSelectedItemsDisplay() {
  const selectedItems = Array.from(checkboxes)
    .filter(checkbox => checkbox.checked)
    .map(checkbox => checkbox.parentNode.textContent.trim());

  if (selectedItems.length === 0) {
    selectedItemsDisplay.textContent = "None";
  } else if (selectedItems.length <= 2) {
    selectedItemsDisplay.textContent = selectedItems.join(", ");
  } else {
    selectedItemsDisplay.textContent = `${selectedItems.slice(0, 2).join(", ")}, +${selectedItems.length - 2}`;
  }
}

// Initial update on page load
updateSelectedItemsDisplay();