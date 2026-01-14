// API Base URL
const API_URL = '/api/recipes';

// DOM Elements
const recipeForm = document.getElementById('recipe-form');
const recipesContainer = document.getElementById('recipes-container');

// Sample Food Images (Modest food images)
const sampleImages = [
    'https://images.unsplash.com/photo-1565958011703-44f9829ba187?ixlib=rb-4.0.3&auto=format&fit=crop&w=1365&q=80',
    'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?ixlib=rb-4.0.3&auto=format&fit=crop&w=1365&q=80',
    'https://images.unsplash.com/photo-1565958011703-44f9829ba187?ixlib=rb-4.0.3&auto=format&fit=crop&w=1365&q=80',
    'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?ixlib=rb-4.0.3&auto=format&fit=crop&w=1365&q=80',
    'https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?ixlib=rb-4.0.3&auto=format&fit=crop&w=1365&q=80'
];

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadRecipes();
    setupEventListeners();
    addSampleRecipesIfEmpty();
});

// Setup Event Listeners
function setupEventListeners() {
    recipeForm.addEventListener('submit', handleAddRecipe);
}

// Load Recipes
async function loadRecipes() {
    try {
        const response = await fetch(API_URL);
        const recipes = await response.json();
        displayRecipes(recipes);
    } catch (error) {
        console.error('Error loading recipes:', error);
        showDefaultRecipes();
    }
}

// Display Recipes
function displayRecipes(recipes) {
    recipesContainer.innerHTML = '';
    
    recipes.forEach(recipe => {
        const recipeCard = createRecipeCard(recipe);
        recipesContainer.innerHTML += recipeCard;
    });
}

// Create Recipe Card HTML
function createRecipeCard(recipe) {
    return `
        <div class="recipe-card" data-id="${recipe._id}">
            <div class="recipe-img" style="background-image: url('${recipe.image || sampleImages[Math.floor(Math.random() * sampleImages.length)]}')"></div>
            <div class="recipe-content">
                <h4>${recipe.name}</h4>
                <p>${recipe.description}</p>
                <div class="recipe-meta">
                    <span><i class="fas fa-tag"></i> ${recipe.category}</span>
                    <span><i class="fas fa-clock"></i> ${recipe.time} min</span>
                </div>
                <p><strong>Ingredients:</strong> ${recipe.ingredients ? recipe.ingredients.join(', ') : 'No ingredients listed'}</p>
                <div class="recipe-actions">
                    <button class="btn-edit" onclick="editRecipe('${recipe._id}')">
                        <i class="fas fa-edit"></i> Edit
                    </button>
                    <button class="btn-delete" onclick="deleteRecipe('${recipe._id}')">
                        <i class="fas fa-trash"></i> Delete
                    </button>
                </div>
            </div>
        </div>
    `;
}

// Handle Add Recipe
async function handleAddRecipe(e) {
    e.preventDefault();
    
    const recipeData = {
        name: document.getElementById('name').value,
        description: document.getElementById('description').value,
        image: document.getElementById('image').value,
        category: document.getElementById('category').value,
        time: parseInt(document.getElementById('time').value),
        ingredients: document.getElementById('ingredients').value.split(',').map(item => item.trim())
    };
    
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(recipeData)
        });
        
        if (response.ok) {
            alert('✅ Recipe added successfully!');
            recipeForm.reset();
            loadRecipes();
        }
    } catch (error) {
        console.error('Error adding recipe:', error);
        alert('❌ Error adding recipe');
    }
}

// Delete Recipe
async function deleteRecipe(id) {
    if (confirm('Are you sure you want to delete this recipe?')) {
        try {
            const response = await fetch(`${API_URL}/${id}`, {
                method: 'DELETE'
            });
            
            if (response.ok) {
                alert('✅ Recipe deleted successfully!');
                loadRecipes();
            }
        } catch (error) {
            console.error('Error deleting recipe:', error);
            alert('❌ Error deleting recipe');
        }
    }
}

// Edit Recipe (Simple implementation)
async function editRecipe(id) {
    const newName = prompt('Enter new recipe name:');
    if (newName) {
        try {
            const response = await fetch(`${API_URL}/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ name: newName })
            });
            
            if (response.ok) {
                alert('✅ Recipe updated successfully!');
                loadRecipes();
            }
        } catch (error) {
            console.error('Error updating recipe:', error);
            alert('❌ Error updating recipe');
        }
    }
}

// Add Sample Recipes if Empty
async function addSampleRecipesIfEmpty() {
    try {
        const response = await fetch(API_URL);
        const recipes = await response.json();
        
        if (recipes.length === 0) {
            const sampleRecipes = [
                {
                    name: "Classic Spaghetti Carbonara",
                    description: "A classic Italian pasta dish with eggs, cheese, pancetta, and pepper.",
                    image: sampleImages[0],
                    category: "Italian",
                    time: 30,
                    ingredients: ["Spaghetti", "Eggs", "Parmesan cheese", "Pancetta", "Black pepper"]
                },
                {
                    name: "Vegetable Stir Fry",
                    description: "Quick and healthy vegetable stir fry with soy sauce and ginger.",
                    image: sampleImages[1],
                    category: "Asian",
                    time: 20,
                    ingredients: ["Mixed vegetables", "Soy sauce", "Ginger", "Garlic", "Sesame oil"]
                },
                {
                    name: "Chocolate Chip Cookies",
                    description: "Soft and chewy chocolate chip cookies perfect for any occasion.",
                    image: sampleImages[2],
                    category: "Dessert",
                    time: 25,
                    ingredients: ["Flour", "Butter", "Sugar", "Chocolate chips", "Egg", "Vanilla extract"]
                },
                {
                    name: "Greek Salad",
                    description: "Fresh and healthy Greek salad with feta cheese and olives.",
                    image: sampleImages[3],
                    category: "Salad",
                    time: 15,
                    ingredients: ["Tomatoes", "Cucumber", "Red onion", "Feta cheese", "Olives", "Olive oil"]
                }
            ];
            
            for (const recipe of sampleRecipes) {
                await fetch(API_URL, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(recipe)
                });
            }
            
            console.log('✅ Sample recipes added');
            loadRecipes();
        }
    } catch (error) {
        console.error('Error adding sample recipes:', error);
    }
}

// Show Default Recipes if API fails
function showDefaultRecipes() {
    const defaultRecipes = `
        <div class="recipe-card">
            <div class="recipe-img" style="background-image: url('${sampleImages[0]}')"></div>
            <div class="recipe-content">
                <h4>Classic Spaghetti Carbonara</h4>
                <p>A classic Italian pasta dish with eggs, cheese, pancetta, and pepper.</p>
                <div class="recipe-meta">
                    <span><i class="fas fa-tag"></i> Italian</span>
                    <span><i class="fas fa-clock"></i> 30 min</span>
                </div>
                <p><strong>Ingredients:</strong> Spaghetti, Eggs, Parmesan cheese, Pancetta, Black pepper</p>
            </div>
        </div>
        
        <div class="recipe-card">
            <div class="recipe-img" style="background-image: url('${sampleImages[1]}')"></div>
            <div class="recipe-content">
                <h4>Vegetable Stir Fry</h4>
                <p>Quick and healthy vegetable stir fry with soy sauce and ginger.</p>
                <div class="recipe-meta">
                    <span><i class="fas fa-tag"></i> Asian</span>
                    <span><i class="fas fa-clock"></i> 20 min</span>
                </div>
                <p><strong>Ingredients:</strong> Mixed vegetables, Soy sauce, Ginger, Garlic, Sesame oil</p>
            </div>
        </div>
        
        <div class="recipe-card">
            <div class="recipe-img" style="background-image: url('${sampleImages[2]}')"></div>
            <div class="recipe-content">
                <h4>Chocolate Chip Cookies</h4>
                <p>Soft and chewy chocolate chip cookies perfect for any occasion.</p>
                <div class="recipe-meta">
                    <span><i class="fas fa-tag"></i> Dessert</span>
                    <span><i class="fas fa-clock"></i> 25 min</span>
                </div>
                <p><strong>Ingredients:</strong> Flour, Butter, Sugar, Chocolate chips, Egg, Vanilla extract</p>
            </div>
        </div>
    `;
    
    recipesContainer.innerHTML = defaultRecipes;
}