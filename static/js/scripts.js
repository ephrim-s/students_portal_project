document.addEventListener('DOMContentLoaded', async () => {
  const genderSelect = document.getElementById('gender');
  const countrySelect = document.getElementById('country');
  const courseSelect = document.getElementById('course');

  if (genderSelect && countrySelect && courseSelect) {
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
  }

  const searchName = document.getElementById('search-name');
  const statusFilter = document.getElementById('status-filter');
  const genderFilter = document.getElementById('gender-filter');
  const scoreFilter = document.getElementById('score-filter');
  const filterButton = document.getElementById('filter-search');
  const tableBody = document.querySelector('.student-table tbody');

  if (!searchName || !statusFilter || !genderFilter || !scoreFilter || !filterButton || !tableBody) {
    return;
  }

  filterButton.addEventListener('click', () => {
    const nameValue = searchName.value.trim().toLowerCase();
    const statusValue = statusFilter.value;
    const genderValue = genderFilter.value;
    const scoreValue = scoreFilter.value.trim();

    const rows = Array.from(tableBody.querySelectorAll('tr'));
    let matchedRows = 0;

    rows.forEach((row) => {
      const cells = row.querySelectorAll('td');
      if (cells.length === 0) return;

      const name = cells[1]?.textContent.trim().toLowerCase() || '';
      const gender = cells[2]?.textContent.trim() || '';
      const jambScore = cells[3]?.textContent.trim() || '';
      const admissionStatus = cells[4]?.textContent.trim() || '';

      const matchName = !nameValue || name.includes(nameValue);
      const matchStatus = !statusValue || admissionStatus === statusValue;
      const matchGender = !genderValue || gender === genderValue;
      const matchScore = !scoreValue || jambScore === scoreValue;

      const shouldShow = matchName && matchStatus && matchGender && matchScore;
      row.style.display = shouldShow ? '' : 'none';
      if (shouldShow) matchedRows += 1;
    });

    const noDataRow = document.querySelector('.no-data-row');
    if (noDataRow) {
      noDataRow.style.display = matchedRows === 0 ? '' : 'none';
    }
  });
});
