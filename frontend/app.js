const FEATURE_MAP = {
    'planet_name': 'planet_name',
    'model_snr': 'koi_model_snr',
    'planet_rad': 'koi_prad',
    'depth': 'koi_depth',
    'impact': 'koi_impact',
    'orb_period': 'koi_period',
    'duration': 'koi_duration',
    'planet_eq_temp': 'koi_teq',
    'stellar_teff': 'koi_steff',
    'planet_insol': 'koi_insol',
    'stellar_rad': 'koi_srad',
    'stellar_g_log': 'koi_slogg'
};
const CORE_FEATURE_KEYS = [
    'model_snr', 'planet_rad', 'depth', 'impact', 'orb_period', 'duration'
];
const API_URL = '/predict'; //? change to backend url



// . . .utilities . . .
function displayError(message) {
    const errorContainer = document.getElementById('error-message-container');
    if (!errorContainer) return;

    errorContainer.innerHTML = `
        <div class="alert alert-danger alert-dismissible fade show" role="alert">
            <strong>Error:</strong> ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
    //  close the error after 5 seconds
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
            btn.textContent = isLoading ? 'Predicting...' : (btn.id === 'predictBtn' ? 'Predict' : 'Predict Inputs');
        }
    });
    
    if (loadingDiv) {
        loadingDiv.classList.toggle('d-none', !isLoading);
    }
}

//convert form input into csv 'blob'
function createCsvBlobFromInput() {
    const inputValues = {};
    for (const feKey in FEATURE_MAP) {
        const inputElement = document.getElementById(feKey);
        if (inputElement) {
            inputValues[feKey] = inputElement.value;
        }
    }

    //planet name validation
    if (!inputValues.planet_name) {
        displayError("Planet Name is required for manual input.");
        return null;
    }

    //>=3 must be filled validation
    let filledCoreCount = 0;
    CORE_FEATURE_KEYS.forEach(key => {
        const value = inputValues[key];
        if (value && !isNaN(parseFloat(value))) {
            filledCoreCount++;
        }
    });

    if (filledCoreCount < 3) {
        displayError(`You must fill in at least three core numerical columns (currently ${filledCoreCount} filled).`);
        return null;
    }

    //csv content
    const headers = [];
    const rowValues = [];
    const allFeKeys = Object.keys(FEATURE_MAP);

    // header row using from backend expected keys
    allFeKeys.forEach(feKey => {
        headers.push(FEATURE_MAP[feKey]);
        // input value or empty string for missing data 
        rowValues.push(inputValues[feKey] || ''); 
    });

    const csvContent = headers.join(',') + '\n' + rowValues.join(',');
    
    // new blobl representing csv
    return new Blob([csvContent], { type: 'text/csv' });
}


// . . .prediction logic . . .

//send to backend for prediction
async function predictData(file, fileName) {
    setLoading(true);
    document.getElementById('results-section').classList.add('d-none');
    document.getElementById('explanation-section').classList.add('d-none');

    try {
        const formData = new FormData();
        formData.append('file', file, fileName);

        const response = await fetch(API_URL, {
            method: 'POST',
            body: formData,
        });

        const result = await response.json();

        if (response.ok) {
            updateUI(result);
        } else {
            displayError(result.error || `Prediction failed: Server returned ${response.status}`);
        }

    } catch (error) {
        console.error('Fetch error:', error);
        displayError('A network error occurred or the server unavailable.');
    } finally {
        setLoading(false);
    }
}

//handle csv uplaod
function handleCsvUpload() {
    const fileInput = document.getElementById('csvFile');
    const file = fileInput.files[0];

    if (!file) {
        displayError("Please select a CSV file to upload.");
        return;
    }

    predictData(file, file.name);
}

//handle manual input
function handleManualPredict() {
    const csvBlob = createCsvBlobFromInput();

    if (csvBlob) {
        predictData(csvBlob, 'manual_input.csv');
    }
} 




/**
 * function generateCharts(){
 * clear previous
 *  if (confusionChartInstance) confusionChartInstance.destroy();
    if (featureChartInstance) featureChartInstance.destroy();
    
    make graphs......-->
    
    }
 */




//updates UI with backend predictions
function updateUI(results) {
    const tableBody = document.getElementById('resultsTable').querySelector('tbody');
    const tableHead = document.getElementById('resultsTable').querySelector('thead');
    const summaryDiv = document.getElementById('summary');
    
    // clear previous results.
    tableHead.innerHTML = '';
    tableBody.innerHTML = '';

    if (!results.columns || !results.rows || results.rows.length === 0) {
        displayError("Received no data or rows from the predictor.");
        return;
    }

    //table header
    const headerRow = document.createElement('tr');
    results.columns.forEach(col => {
        const th = document.createElement('th');
        th.textContent = col;
        headerRow.appendChild(th);
    });
    tableHead.appendChild(headerRow);

    // table body and summary
    let confirmedCount = 0;
    let candidateCount = 0;
    let falsePositiveCount = 0;
    
    results.rows.forEach(row => {
        const tr = document.createElement('tr');
        row.forEach((cell, index) => {
            const td = document.createElement('td');
            // If the cell is a number, round it (readability)
            if (typeof cell === 'number' && index < row.length - 1) { 
                td.textContent = cell.toFixed(4);
            } else {
                td.textContent = cell;
            }
            tr.appendChild(td);
        });
        tableBody.appendChild(tr);

        // count predictions (last element in the row is the prediction string)
        const prediction = row[row.length - 1];
        if (prediction === 'CONFIRMED') confirmedCount++;
        else if (prediction === 'CANDIDATE') candidateCount++;
        else if (prediction === 'FALSE POSITIVE') falsePositiveCount++;
    });

    const totalCount = results.rows.length;

    // update summary 
    summaryDiv.innerHTML = `
        <p class="mb-2">Total Objects Analyzed: <strong>${totalCount}</strong></p>
        <p class="mb-1 text-success">Confirmed Planets: <strong>${confirmedCount}</strong> (${((confirmedCount / totalCount) * 100).toFixed(1)}%)</p>
        <p class="mb-1 text-warning">Candidate Planets: <strong>${candidateCount}</strong> (${((candidateCount / totalCount) * 100).toFixed(1)}%)</p>
        <p class="mb-1 text-danger">False Positives: <strong>${falsePositiveCount}</strong> (${((falsePositiveCount / totalCount) * 100).toFixed(1)}%)</p>
        <p class="mt-3 text-info border-top pt-2">Model Run successfully using **${results.columns.length - 1}** features.</p>
    `;
    
    // generate charts and show results
    // generateCharts();
    document.getElementById('results-section').classList.remove('d-none');
    
    // scroll to results
    document.getElementById('results-section').scrollIntoView({ behavior: 'smooth' });
}