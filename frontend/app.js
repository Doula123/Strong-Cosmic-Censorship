// ===============================
// 1. Feature Keys
// ===============================
const CORE_FEATURE_KEYS = [
    'orb_period',
    'duration',
    'depth',
    'planet_rad',
    'stellar_rad',
    'model_snr',
    'impact'
  ];
  
  const OPTIONAL_FEATURE_KEYS = [
    'stellar_teff',
    'stellar_g_log',
    'planet_eq_temp',
    'planet_insol'
  ];
  
  // keep planet_name separate for display / CSV first column
  const ALL_FEATURE_KEYS = [
    'planet_name',
    ...CORE_FEATURE_KEYS,
    ...OPTIONAL_FEATURE_KEYS
  ];
  
  const API_URL = 'http://127.0.0.1:5000/predict';          // For CSV upload
  const API_SINGLE_URL = 'http://127.0.0.1:5000/predict_single'; // For manual JSON input
  
  
  // ===============================
  // 2. Utility Functions
  // ===============================
  function displayError(message) {
    const errorContainer = document.getElementById('error-message-container');
    if (!errorContainer) return;
  
    errorContainer.innerHTML = `
      <div class="alert alert-danger alert-dismissible fade show" role="alert">
        <strong>Error:</strong> ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
      </div>
    `;
  
    setTimeout(() => {
      const alertElement = errorContainer.querySelector('.alert');
      if (alertElement) alertElement.remove();
    }, 5000);
  }
  
  function setLoading(isLoading) {
    const predictBtn = document.getElementById('predictBtn');
    const inputPredictBtn = document.getElementById('inputPredictBtn');
    const loadingDiv = document.getElementById('loading');
  
    [predictBtn, inputPredictBtn].forEach(btn => {
      if (btn) {
        btn.disabled = isLoading;
        btn.textContent = isLoading
          ? 'Predicting...'
          : (btn.id === 'predictBtn' ? 'Predict' : 'Predict Inputs');
      }
    });
  
    if (loadingDiv) {
      loadingDiv.classList.toggle('d-none', !isLoading);
    }
  }
  
  
  // ===============================
  // 3. Prediction for CSV Upload
  // ===============================
  async function predictData(file, fileName) {
    setLoading(true);
    document.getElementById('results-section').classList.add('d-none');
  
    try {
      const formData = new FormData();
      formData.append('file', file, fileName);
  
      const response = await fetch(API_URL, {
        method: 'POST',
        body: formData
      });
  
    const text = await response.text();         // get raw response as text
    console.log("RAW RESPONSE:", text);         // log it so we can see it
    const result = JSON.parse(text); 
      if (response.ok) {
        updateUI(result);
      } else {
        displayError(result.error || `Prediction failed: Server returned ${response.status}`);
      }
    } catch (error) {
      console.error('Fetch error:', error);
      displayError('A network error occurred or the server is unavailable.');
    } finally {
      setLoading(false);
    }
  }
  
  
  // ===============================
  // 4. Prediction for Manual Input (JSON)
  // ===============================
  function handleManualPredict() {
    // Collect input values
    const inputValues = {};
    ALL_FEATURE_KEYS.forEach(key => {
      const el = document.getElementById(key);
      if (el) inputValues[key] = el.value === '' ? null : parseFloat(el.value) || el.value;
    });
  
    if (!inputValues.planet_name) {
      displayError("Planet Name is required for manual input.");
      return;
    }
  
    // Ensure at least 3 core numeric fields are provided
    const filledCoreCount = CORE_FEATURE_KEYS.reduce(
      (count, key) => count + (!isNaN(parseFloat(inputValues[key])) ? 1 : 0),
      0
    );
  
    if (filledCoreCount < 3) {
      displayError(`You must fill in at least 3 core numerical columns (currently ${filledCoreCount} filled).`);
      return;
    }
  
    setLoading(true);
    document.getElementById('results-section').classList.add('d-none');
  
    fetch(API_SINGLE_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(inputValues)
    })
      .then(res => res.json())
      .then(result => {
        if (result.error) {
          displayError(result.error);
        } else {
          updateSingleUI(result);
        }
      })
      .catch(err => {
        console.error('Network error:', err);
        displayError('A network error occurred or the server is unavailable.');
      })
      .finally(() => setLoading(false));
  }
  
  
  // ===============================
  // 5. CSV Upload Handler
  // ===============================
  function handleCsvUpload() {
    const fileInput = document.getElementById('csvFile');
    const file = fileInput.files[0];
  
    if (!file) {
      displayError("Please select a CSV file to upload.");
      return;
    }
  
    predictData(file, file.name);
  }
  
  
  // ===============================
  // 6. UI Update for Bulk CSV Predictions
  // ===============================
  function updateUI(result) {
    console.log('Prediction Result:', result);
    const uploadDiv = document.getElementById('upload-section');
    const manualDiv = document.getElementById('manual-input-section');
    if (uploadDiv) uploadDiv.style.display = 'none';
    if (manualDiv) manualDiv.style.display = 'none';
  
    const table = document.getElementById('resultsTable');
    const thead = table.querySelector('thead');
    const tbody = table.querySelector('tbody');
  
    thead.innerHTML = '';
    tbody.innerHTML = '';
  
    // Add header
    const headerRow = document.createElement('tr');
    result.columns.forEach(col => {
      const th = document.createElement('th');
      th.textContent = col;
      headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);
  
    // Add rows
    result.rows.forEach(rowData => {
      const row = document.createElement('tr');
      rowData.forEach(cellData => {
        const td = document.createElement('td');
        td.textContent = cellData;
        row.appendChild(td);
      });
      tbody.appendChild(row);
    });
  
    document.getElementById('summary').innerHTML = `<p>Predictions generated for ${result.rows.length} objects.</p>`;
    document.getElementById('results-section').classList.remove('d-none');
  }
  
  
  // ===============================
  // 7. UI Update for Single Prediction
  // ===============================
  function updateSingleUI(result) {
    console.log('Single Prediction Result:', result);
  
    const summaryDiv = document.getElementById('summary');
    summaryDiv.innerHTML = `
      <p><strong>Planet:</strong> ${result.planet_name}</p>
      <p><strong>Predicted Disposition:</strong> ${result.prediction}</p>
    `;
  
    // Hide table when doing single input
    const table = document.getElementById('resultsTable');
    table.querySelector('thead').innerHTML = '';
    table.querySelector('tbody').innerHTML = '';
  
    document.getElementById('results-section').classList.remove('d-none');
  }
  
  
  // ===============================
  // 8. Attach Event Listeners
  // ===============================
  document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('predictBtn')?.addEventListener('click', handleCsvUpload);
    document.getElementById('inputPredictBtn')?.addEventListener('click', handleManualPredict);
  
  });
  