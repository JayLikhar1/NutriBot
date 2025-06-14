from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from chatbot_logic import calculate_bmr, calculate_tdee, calculate_macros, generate_meal_plan
import os
import json

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.debug = True

# Meal database with nutritional information
MEAL_DATABASE = {
    'breakfast': {
        'vegetarian': [
            {
                'name': 'Oatmeal with Fruits and Nuts',
                'calories': 350,
                'protein': 12,
                'carbs': 45,
                'fat': 15,
                'ingredients': ['Oatmeal', 'Mixed berries', 'Almonds', 'Honey', 'Cinnamon']
            },
            {
                'name': 'Greek Yogurt Parfait',
                'calories': 300,
                'protein': 20,
                'carbs': 35,
                'fat': 10,
                'ingredients': ['Greek yogurt', 'Granola', 'Mixed fruits', 'Honey']
            },
            {
                'name': 'Avocado Toast',
                'calories': 400,
                'protein': 15,
                'carbs': 40,
                'fat': 20,
                'ingredients': ['Whole grain bread', 'Avocado', 'Eggs', 'Cherry tomatoes', 'Microgreens']
            }
        ],
        'non_vegetarian': [
            {
                'name': 'Protein-Packed Breakfast Bowl',
                'calories': 450,
                'protein': 30,
                'carbs': 40,
                'fat': 20,
                'ingredients': ['Eggs', 'Turkey bacon', 'Sweet potato', 'Spinach', 'Avocado']
            },
            {
                'name': 'Chicken and Vegetable Omelette',
                'calories': 400,
                'protein': 35,
                'carbs': 15,
                'fat': 25,
                'ingredients': ['Eggs', 'Chicken breast', 'Bell peppers', 'Onions', 'Cheese']
            }
        ],
        'indian_vegetarian': [
            {
                'name': 'Poha (Flattened Rice)',
                'calories': 280,
                'protein': 8,
                'carbs': 45,
                'fat': 10,
                'ingredients': ['Flattened rice', 'Peas', 'Potatoes', 'Onion', 'Turmeric', 'Curry leaves']
            },
            {
                'name': 'Moong Dal Cheela (Lentil Pancake)',
                'calories': 320,
                'protein': 15,
                'carbs': 40,
                'fat': 12,
                'ingredients': ['Moong dal flour', 'Ginger', 'Green chilies', 'Coriander', 'Spices']
            }
        ],
        'indian_non_vegetarian': [
            {
                'name': 'Anda Bhurji (Scrambled Eggs) with Pav',
                'calories': 400,
                'protein': 20,
                'carbs': 40,
                'fat': 18,
                'ingredients': ['Eggs', 'Onion', 'Tomatoes', 'Spices', 'Pav (bread rolls)']
            }
        ]
    },
    'lunch': {
        'vegetarian': [
            {
                'name': 'Mediterranean Quinoa Bowl',
                'calories': 550,
                'protein': 20,
                'carbs': 65,
                'fat': 25,
                'ingredients': ['Quinoa', 'Chickpeas', 'Cucumber', 'Tomatoes', 'Feta cheese', 'Olive oil']
            },
            {
                'name': 'Lentil and Vegetable Soup',
                'calories': 400,
                'protein': 18,
                'carbs': 45,
                'fat': 15,
                'ingredients': ['Lentils', 'Carrots', 'Celery', 'Onions', 'Vegetable broth']
            }
        ],
        'non_vegetarian': [
            {
                'name': 'Grilled Chicken Salad',
                'calories': 500,
                'protein': 40,
                'carbs': 30,
                'fat': 25,
                'ingredients': ['Chicken breast', 'Mixed greens', 'Cherry tomatoes', 'Cucumber', 'Olive oil']
            },
            {
                'name': 'Salmon and Brown Rice Bowl',
                'calories': 600,
                'protein': 35,
                'carbs': 50,
                'fat': 30,
                'ingredients': ['Salmon', 'Brown rice', 'Broccoli', 'Carrots', 'Soy sauce']
            }
        ],
        'indian_vegetarian': [
            {
                'name': 'Dal Makhani with Brown Rice',
                'calories': 600,
                'protein': 25,
                'carbs': 80,
                'fat': 20,
                'ingredients': ['Black lentils', 'Kidney beans', 'Cream', 'Spices', 'Brown rice']
            },
            {
                'name': 'Paneer Butter Masala with Whole Wheat Roti',
                'calories': 650,
                'protein': 30,
                'carbs': 70,
                'fat': 30,
                'ingredients': ['Paneer', 'Tomatoes', 'Butter', 'Cream', 'Spices', 'Whole wheat flour']
            }
        ],
        'indian_non_vegetarian': [
            {
                'name': 'Chicken Curry with Brown Rice',
                'calories': 650,
                'protein': 40,
                'carbs': 60,
                'fat': 25,
                'ingredients': ['Chicken', 'Onion', 'Tomatoes', 'Ginger', 'Garlic', 'Spices', 'Brown rice']
            },
            {
                'name': 'Fish Fry with Vegetable Pulao',
                'calories': 700,
                'protein': 35,
                'carbs': 70,
                'fat': 30,
                'ingredients': ['Fish fillet', 'Spices', 'Basmati rice', 'Mixed vegetables']
            }
        ]
    },
    'dinner': {
        'vegetarian': [
            {
                'name': 'Stuffed Bell Peppers',
                'calories': 450,
                'protein': 15,
                'carbs': 55,
                'fat': 20,
                'ingredients': ['Bell peppers', 'Quinoa', 'Black beans', 'Corn', 'Cheese']
            },
            {
                'name': 'Vegetable Stir-Fry with Tofu',
                'calories': 400,
                'protein': 20,
                'carbs': 45,
                'fat': 18,
                'ingredients': ['Tofu', 'Broccoli', 'Carrots', 'Snap peas', 'Soy sauce']
            }
        ],
        'non_vegetarian': [
            {
                'name': 'Grilled Chicken with Roasted Vegetables',
                'calories': 550,
                'protein': 45,
                'carbs': 40,
                'fat': 25,
                'ingredients': ['Chicken breast', 'Sweet potatoes', 'Broccoli', 'Carrots', 'Olive oil']
            },
            {
                'name': 'Baked Salmon with Asparagus',
                'calories': 500,
                'protein': 35,
                'carbs': 30,
                'fat': 30,
                'ingredients': ['Salmon fillet', 'Asparagus', 'Lemon', 'Herbs', 'Olive oil']
            }
        ],
        'indian_vegetarian': [
            {
                'name': 'Palak Paneer with Jeera Rice',
                'calories': 580,
                'protein': 28,
                'carbs': 60,
                'fat': 25,
                'ingredients': ['Spinach', 'Paneer', 'Tomatoes', 'Spices', 'Basmati rice', 'Cumin seeds']
            },
            {
                'name': 'Vegetable Korma with Naan',
                'calories': 620,
                'protein': 20,
                'carbs': 70,
                'fat': 28,
                'ingredients': ['Mixed vegetables', 'Cream', 'Nuts', 'Spices', 'All-purpose flour']
            }
        ],
        'indian_non_vegetarian': [
            {
                'name': 'Mutton Rogan Josh with Whole Wheat Roti',
                'calories': 700,
                'protein': 45,
                'carbs': 50,
                'fat': 35,
                'ingredients': ['Mutton', 'Yogurt', 'Spices', 'Whole wheat flour']
            },
            {
                'name': 'Tandoori Chicken with Salad',
                'calories': 550,
                'protein': 40,
                'carbs': 20,
                'fat': 30,
                'ingredients': ['Chicken', 'Yogurt', 'Tandoori masala', 'Lemon', 'Mixed greens']
            }
        ]
    },
    'snacks': {
        'vegetarian': [
            {
                'name': 'Greek Yogurt with Berries',
                'calories': 200,
                'protein': 15,
                'carbs': 20,
                'fat': 8,
                'ingredients': ['Greek yogurt', 'Mixed berries', 'Honey']
            },
            {
                'name': 'Hummus with Vegetables',
                'calories': 250,
                'protein': 8,
                'carbs': 25,
                'fat': 15,
                'ingredients': ['Hummus', 'Carrot sticks', 'Cucumber', 'Bell peppers']
            }
        ],
        'non_vegetarian': [
            {
                'name': 'Hard-Boiled Eggs with Avocado',
                'calories': 300,
                'protein': 20,
                'carbs': 10,
                'fat': 22,
                'ingredients': ['Eggs', 'Avocado', 'Salt', 'Pepper']
            },
            {
                'name': 'Turkey and Cheese Roll-Ups',
                'calories': 250,
                'protein': 25,
                'carbs': 5,
                'fat': 15,
                'ingredients': ['Turkey slices', 'Cheese', 'Lettuce', 'Mustard']
            }
        ],
        'indian_vegetarian': [
            {
                'name': 'Fruit Chaat',
                'calories': 180,
                'protein': 3,
                'carbs': 40,
                'fat': 2,
                'ingredients': ['Mixed fruits', 'Chaat masala', 'Lemon juice']
            },
            {
                'name': 'Roasted Chana (Chickpeas)',
                'calories': 220,
                'protein': 10,
                'carbs': 30,
                'fat': 7,
                'ingredients': ['Roasted chickpeas', 'Spices']
            }
        ],
        'indian_non_vegetarian': [
            {
                'name': 'Chicken Tikka Skewers',
                'calories': 280,
                'protein': 30,
                'carbs': 5,
                'fat': 15,
                'ingredients': ['Chicken breast', 'Yogurt', 'Spices']
            }
        ]
    }
}

def calculate_bmr(weight, height, age, gender):
    """Calculate Basal Metabolic Rate using Mifflin-St Jeor Equation"""
    if gender == 'male':
        return 10 * weight + 6.25 * height - 5 * age + 5
    return 10 * weight + 6.25 * height - 5 * age - 161

def calculate_tdee(bmr, activity_level):
    """Calculate Total Daily Energy Expenditure"""
    activity_multipliers = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'very': 1.725
    }
    return bmr * activity_multipliers[activity_level]

def calculate_macros(calories, goal):
    """Calculate macronutrient distribution based on goal"""
    if goal == 'lose':
        return {
            'protein': 0.4,  # 40% of calories
            'carbs': 0.3,    # 30% of calories
            'fat': 0.3       # 30% of calories
        }
    elif goal == 'gain':
        return {
            'protein': 0.3,  # 30% of calories
            'carbs': 0.5,    # 50% of calories
            'fat': 0.2       # 20% of calories
        }
    else:  # maintain
        return {
            'protein': 0.3,  # 30% of calories
            'carbs': 0.45,   # 45% of calories
            'fat': 0.25      # 25% of calories
        }

def generate_meal_plan(user_data, target_calories, macros):
    """Generate a personalized meal plan based on user data and goals"""
    is_vegetarian = 'vegetarian' in user_data['diet_type']
    is_indian = 'indian' in user_data['diet_type']

    if is_indian:
        diet_key = 'indian_vegetarian' if is_vegetarian else 'indian_non_vegetarian'
    else:
        diet_key = 'vegetarian' if is_vegetarian else 'non_vegetarian'
    
    # Calculate calories per meal
    meal_calories = {
        'breakfast': target_calories * 0.25,  # 25% of daily calories
        'lunch': target_calories * 0.35,      # 35% of daily calories
        'dinner': target_calories * 0.30,     # 30% of daily calories
        'snacks': target_calories * 0.10      # 10% of daily calories
    }
    
    meal_plan = {}
    for meal_type in ['breakfast', 'lunch', 'dinner', 'snacks']:
        # Filter meals based on dietary restrictions and selected diet_key
        available_meals = MEAL_DATABASE[meal_type][diet_key]
        
        # Filter out meals that don't match dietary restrictions
        if 'gluten' in user_data['restrictions']:
            available_meals = [meal for meal in available_meals if 'gluten' not in ' '.join(meal['ingredients']).lower()]
        if 'dairy' in user_data['restrictions']:
            available_meals = [meal for meal in available_meals if 'dairy' not in ' '.join(meal['ingredients']).lower()]
        if 'nuts' in user_data['restrictions']:
            available_meals = [meal for meal in available_meals if 'nut' not in ' '.join(meal['ingredients']).lower()]
        
        # Select meals that best match the calorie target
        selected_meals = []
        remaining_calories = meal_calories[meal_type]
        
        # Try to find meals that fit the calorie budget
        for meal in available_meals:
            if meal['calories'] <= remaining_calories:
                selected_meals.append(meal)
                remaining_calories -= meal['calories']
                if len(selected_meals) >= 2:  # Limit to 2 options per meal for variety
                    break
        
        # If no meals fit, or not enough, just add what's available (or a fallback)
        if not selected_meals and available_meals:
            selected_meals.append(available_meals[0]) # Fallback to first available
        elif not selected_meals:
            selected_meals.append({'name': 'Custom Meal', 'calories': int(meal_calories[meal_type]), 'protein': 0, 'carbs': 0, 'fat': 0, 'ingredients': ['Please consult a nutritionist for a custom plan.']}) # Generic fallback

        meal_plan[meal_type] = selected_meals
    
    return meal_plan

@app.route('/')
def index():
    return render_template('landing.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/plan')
def plan():
    return render_template('plan.html')

@app.route('/generate_plan', methods=['POST'])
def generate_plan():
    # Get form data
    data = {
        'age': int(request.form.get('age')),
        'gender': request.form.get('gender'),
        'weight': float(request.form.get('weight')),
        'height': float(request.form.get('height')),
        'activity_level': request.form.get('activity_level'),
        'goal': request.form.get('goal'),
        'diet_type': request.form.getlist('diet_type'),
        'restrictions': request.form.getlist('restrictions')
    }
    
    # Calculate BMR and TDEE
    bmr = calculate_bmr(data['weight'], data['height'], data['age'], data['gender'])
    tdee = calculate_tdee(bmr, data['activity_level'])
    
    # Adjust calories based on goal
    if data['goal'] == 'lose':
        target_calories = tdee - 500  # 500 calorie deficit
    elif data['goal'] == 'gain':
        target_calories = tdee + 500  # 500 calorie surplus
    else:  # maintain
        target_calories = tdee
    
    # Calculate macronutrient distribution
    macros = calculate_macros(target_calories, data['goal'])
    
    # Calculate macro amounts in grams
    protein_calories = target_calories * macros['protein']
    carbs_calories = target_calories * macros['carbs']
    fat_calories = target_calories * macros['fat']
    
    macro_grams = {
        'protein': round(protein_calories / 4),  # 4 calories per gram
        'carbs': round(carbs_calories / 4),      # 4 calories per gram
        'fat': round(fat_calories / 9)           # 9 calories per gram
    }
    
    # Generate meal plan
    meal_plan = generate_meal_plan(data, target_calories, macros)
    
    # Store the plan in session
    session['diet_plan'] = {
        'target_calories': round(target_calories),
        'macros': macro_grams,
        'meal_plan': meal_plan,
        'user_data': data
    }
    
    return redirect(url_for('result'))

@app.route('/result')
def result():
    if 'diet_plan' not in session:
        return redirect(url_for('plan'))
    
    return render_template('result.html', plan=session['diet_plan'])

if __name__ == '__main__':
    app.run(debug=True) 