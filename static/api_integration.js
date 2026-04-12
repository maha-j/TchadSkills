// TchadSkills API Integration
const API_BASE = "/api/";

async function fetchFromAPI(endpoint) {
    try {
        const response = await fetch(`${API_BASE}${endpoint}`);
        if (!response.ok) throw new Error('Network response was not ok');
        return await response.json();
    } catch (error) {
        console.error("API Error:", error);
        return null;
    }
}

async function loadCoursesFromAPI() {
    const data = await fetchFromAPI("courses/");
    if (data && data.results) {
        // Supposons que la variable 'courses' est globale dans index.html
        window.courses = data.results;
        if (typeof renderCourses === 'function') {
            renderCourses(window.courses);
        }
    }
}

async function loadCategoriesFromAPI() {
    const data = await fetchFromAPI("categories/");
    if (data && data.results) {
        const categoryContainer = document.querySelector(".categories");
        if (categoryContainer) {
            categoryContainer.innerHTML = data.results.map(cat => `
                <div class="category-card" onclick="filterCoursesByCategory('${cat.name}')">
                    <i class="fas ${cat.icon || 'fa-laptop-code'} category-icon"></i>
                    <h3>${cat.name}</h3>
                    <p>${cat.description || ''}</p>
                </div>
            `).join("");
        }
    }
}

// Initialize API data on load
window.addEventListener("DOMContentLoaded", () => {
    loadCoursesFromAPI();
    loadCategoriesFromAPI();
});
