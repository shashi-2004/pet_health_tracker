// Walking Tracker
let walkingInterval;
let steps = 0;

function startWalking() {
    if (!walkingInterval) {
        walkingInterval = setInterval(() => {
            steps += 10;
            document.getElementById('stepCount').innerText = steps;
        }, 1000);
    }
}

function stopWalking() {
    clearInterval(walkingInterval);
    walkingInterval = null;
}

async function saveSteps() {
    const petId = document.getElementById('walkingPetId').value;
    if (!petId) { alert('Please enter a Pet ID!'); return; }
    const formData = new FormData();
    formData.append('pet_id', petId);
    formData.append('steps', steps);
    const response = await fetch('http://127.0.0.1:5000/save_steps', { method: 'POST', body: formData });
    const result = await response.json();
    alert(result.message);
}

// Food Tracker
function calculateCalories() {
    const foodType = document.getElementById('foodType').value.toLowerCase();
    const quantity = parseInt(document.getElementById('foodQuantity').value) || 0;
    let caloriesPerGram = foodType.includes('chicken') ? 2 : foodType.includes('rice') ? 1.5 : 1;
    const totalCalories = quantity * caloriesPerGram;
    document.getElementById('calorieCount').innerText = totalCalories;
}

async function saveFood() {
    const petId = document.getElementById('foodPetId').value;
    const food = document.getElementById('foodType').value;
    const calories = document.getElementById('calorieCount').innerText;
    if (!petId || !food) { alert('Please enter Pet ID and Food Type!'); return; }
    const formData = new FormData();
    formData.append('pet_id', petId);
    formData.append('food', food);
    formData.append('calories', calories);
    const response = await fetch('http://127.0.0.1:5000/save_food', { method: 'POST', body: formData });
    const result = await response.json();
    alert(result.message);
}

// Medical Tracker
function getSuggestion() {
    const problem = document.getElementById('problem').value.toLowerCase();
    let suggestion = "Consult a vet.";
    if (problem.includes('vomiting')) suggestion = "Keep pet hydrated.";
    else if (problem.includes('lethargy')) suggestion = "Check for fever.";
    document.getElementById('suggestion').innerText = suggestion;
}

async function saveMedical() {
    const petId = document.getElementById('medicalPetId').value;
    const problem = document.getElementById('problem').value;
    const suggestion = document.getElementById('suggestion').innerText;
    if (!petId || !problem) { alert('Please enter Pet ID and Problem!'); return; }
    const formData = new FormData();
    formData.append('pet_id', petId);
    formData.append('problem', problem);
    formData.append('suggestion', suggestion);
    const response = await fetch('http://127.0.0.1:5000/save_medical', { method: 'POST', body: formData });
    const result = await response.json();
    alert(result.message);
}

// Vaccination Updates
async function saveVaccination() {
    const petId = document.getElementById('vaccinationPetId').value;
    const vaccinationType = document.getElementById('vaccinationType').value;
    const vaccinationDate = document.getElementById('vaccinationDate').value;
    if (!petId || !vaccinationType || !vaccinationDate) { alert('Please fill all fields!'); return; }
    const formData = new FormData();
    formData.append('pet_id', petId);
    formData.append('vaccination_type', vaccinationType);
    formData.append('vaccination_date', vaccinationDate);
    const response = await fetch('http://127.0.0.1:5000/save_vaccination', { method: 'POST', body: formData });
    const result = await response.json();
    alert(result.message);
}