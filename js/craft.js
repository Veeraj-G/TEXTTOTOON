// Grid and picture type selection
let selectedGridType = 0;
let selectedPictureType = 0;
const pictureTypeLabels = ['Japanese', 'American', 'Egyptian'];

// Toggle grid type dropdown
function toggleDropdown() {
    const list = document.getElementById('dropdown-list');
    list.style.display = list.style.display === 'block' ? 'none' : 'block';
}

// Select grid type
function selectGrid(idx) {
    const labels = ['TYPE-1', 'TYPE-2', 'TYPE-3'];
    const icons = [
        '<svg width="24" height="24" viewBox="0 0 24 24"><rect x="2" y="2" width="9" height="9" fill="#444"/><rect x="13" y="2" width="9" height="9" fill="#444"/><rect x="2" y="13" width="9" height="9" fill="#444"/><rect x="13" y="13" width="9" height="9" fill="#444"/></svg>',
        '<svg width="24" height="24" viewBox="0 0 24 24"><rect x="2" y="2" width="20" height="9" fill="#444"/><rect x="2" y="13" width="9" height="9" fill="#888"/><rect x="13" y="13" width="9" height="9" fill="#444"/></svg>',
        '<svg width="24" height="24" viewBox="0 0 24 24"><rect x="2" y="2" width="9" height="20" fill="#444"/><rect x="13" y="2" width="9" height="9" fill="#888"/><rect x="13" y="13" width="9" height="9" fill="#888"/></svg>'
    ];
    
    // Update selected grid icon and label
    document.getElementById('selected-grid-icon').innerHTML = icons[idx];
    document.getElementById('selected-grid-label').innerText = labels[idx];
    
    // Hide dropdown
    document.getElementById('dropdown-list').style.display = 'none';
    
    // Update checkmark and selected class
    const items = document.querySelectorAll('.dropdown-item');
    items.forEach((item, i) => {
        if (i === idx) {
            item.classList.add('selected');
            if (!item.querySelector('.checkmark')) {
                const check = document.createElement('span');
                check.className = 'checkmark';
                check.innerHTML = '&#10003;';
                item.appendChild(check);
            }
        } else {
            item.classList.remove('selected');
            const check = item.querySelector('.checkmark');
            if (check) check.remove();
        }
    });
    
    selectedGridType = idx;
    updateOutputDemo();
}

// Toggle picture style dropdown
function togglePictureDropdown() {
    const list = document.getElementById('picture-dropdown-list');
    list.style.display = list.style.display === 'block' ? 'none' : 'block';
}

// Select picture style
function selectPictureType(idx) {
    const labels = ['Japanese', 'American', 'Egyptian'];
    document.getElementById('selected-picture-label').innerText = labels[idx];
    document.getElementById('picture-dropdown-list').style.display = 'none';
    
    // Update checkmark
    const items = document.querySelectorAll('#picture-dropdown-list .dropdown-item');
    items.forEach((item, i) => {
        if (i === idx) {
            item.classList.add('selected');
            if (!item.querySelector('.checkmark')) {
                const check = document.createElement('span');
                check.className = 'checkmark';
                check.innerHTML = '&#10003;';
                item.appendChild(check);
            }
        } else {
            item.classList.remove('selected');
            const check = item.querySelector('.checkmark');
            if (check) check.remove();
        }
    });
    selectedPictureType = idx;
    updateOutputDemo();
}

// Update output demo
function updateOutputDemo() {
    // Update style label
    document.getElementById('output-picture-style').innerText = 'Style: ' + pictureTypeLabels[selectedPictureType];
    
    // Update grid class
    const output = document.getElementById('output-images');
    output.className = 'output-images grid-' + selectedGridType;
    
    // Insert comic panel divs
    output.innerHTML = '';
    let numPanels = 4;
    for (let i = 0; i < numPanels; i++) {
        const panel = document.createElement('div');
        panel.className = 'comic-panel panel-' + (i+1) + ' empty-outline';
        output.appendChild(panel);
    }
}

// Show generating state
function showGeneratingState() {
    const output = document.getElementById('output-images');
    output.innerHTML = '';
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'loading-state';
    loadingDiv.innerHTML = '<div class="spinner"></div><p>Generating your comic...</p>';
    output.appendChild(loadingDiv);
}

// Generate comic
async function generateComic() {
    const prompt = document.querySelector('.search_container input').value;
    if (!prompt) {
        alert('Please enter a prompt first!');
        return;
    }

    showGeneratingState();

    try {
        const response = await fetch('http://localhost:8000/generate-comic', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                prompt: prompt,
                style: pictureTypeLabels[selectedPictureType],
                grid_type: selectedGridType,
                num_panels: 4
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        if (data.images && data.images.length > 0) {
            const output = document.getElementById('output-images');
            output.innerHTML = '';
            data.images.forEach((imageData, index) => {
                const panel = document.createElement('div');
                panel.className = `comic-panel panel-${index + 1}`;
                const img = document.createElement('img');
                img.src = imageData;
                img.alt = `Comic panel ${index + 1}`;
                panel.appendChild(img);
                output.appendChild(panel);
            });
        } else {
            throw new Error('No images received from the server');
        }
    } catch (error) {
        console.error('Error:', error);
        alert(`Failed to generate comic: ${error.message}`);
        updateOutputDemo();
    }
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    // Close dropdowns on outside click
    document.addEventListener('click', (event) => {
        const gridDropdown = document.querySelector('.grid-type-dropdown');
        const pictureDropdown = document.querySelector('.picture-style-dropdown');
        
        if (gridDropdown && !gridDropdown.contains(event.target)) {
            document.getElementById('dropdown-list').style.display = 'none';
        }
        
        if (pictureDropdown && !pictureDropdown.contains(event.target)) {
            document.getElementById('picture-dropdown-list').style.display = 'none';
        }
    });

    // Generate button click handler
    const generateBtn = document.getElementById('generate-btn');
    if (generateBtn) {
        generateBtn.addEventListener('click', generateComic);
    }

    // Initialize the demo
    updateOutputDemo();
}); 