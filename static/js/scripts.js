document.addEventListener('DOMContentLoaded', async () => {
  const genderSelect = document.getElementById('gender');
  const countrySelect = document.getElementById('country');
  const courseSelect = document.getElementById('course');

  if (!genderSelect || !countrySelect || !courseSelect) {
    return;
  }

  const options = await fetch('/api/options').then((response) => response.json());

  const populateSelect = (select, values) => {
    values.forEach((value) => {
      const option = document.createElement('option');
      option.value = value;
      option.textContent = value;
      select.appendChild(option);
    });
  };

  populateSelect(genderSelect, ['Male', 'Female', 'Other']);
  populateSelect(countrySelect, options.countries);
  populateSelect(courseSelect, options.courses);
});
