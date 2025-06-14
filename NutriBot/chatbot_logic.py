def calculate_bmr(age, weight, height, gender):
    """Calculate Basal Metabolic Rate using Mifflin-St Jeor Equation"""
    if gender.lower() == "male":
        return 10 * weight + 6.25 * height - 5 * age + 5
    else:
        return 10 * weight + 6.25 * height - 5 * age - 161

def calculate_tdee(bmr, activity_level):
    """Calculate Total Daily Energy Expenditure based on activity level"""
    activity_multipliers = {
        'sedentary': 1.2,        # Little to no exercise
        'lightly_active': 1.375,  # Light exercise 1-3 days/week
        'moderately_active': 1.55, # Moderate exercise 3-5 days/week
        'very_active': 1.725,     # Hard exercise 6-7 days/week
        'extra_active': 1.9       # Very hard exercise & physical job
    }
    return bmr * activity_multipliers.get(activity_level, 1.2)

def calculate_macros(calories, weight, goal):
    """Calculate macronutrient distribution based on goals"""
    if goal == 'muscle_gain':
        protein = weight * 1.8  # Higher protein for muscle gain
        fat = weight * 0.8
    elif goal == 'weight_loss':
        protein = weight * 1.6  # Higher protein for weight loss
        fat = weight * 0.6
    else:  # maintenance
        protein = weight * 1.4
        fat = weight * 0.7
    
    # Calculate remaining calories for carbs
    protein_calories = protein * 4
    fat_calories = fat * 9
    carb_calories = calories - (protein_calories + fat_calories)
    carbs = carb_calories / 4
    
    return {
        'protein': round(protein, 1),
        'carbs': round(carbs, 1),
        'fats': round(fat, 1)
    }

# Meal database with calorie ranges
meal_db = {
    'veg': {
        'breakfast': [
            {'name': 'Oatmeal with fruits and nuts', 'calories': 350, 'protein': 12, 'carbs': 45, 'fats': 15},
            {'name': 'Poha with vegetables', 'calories': 300, 'protein': 8, 'carbs': 55, 'fats': 8},
            {'name': 'Idli with sambar', 'calories': 250, 'protein': 10, 'carbs': 40, 'fats': 5}
        ],
        'lunch': [
            {'name': 'Brown rice with dal and vegetables', 'calories': 450, 'protein': 15, 'carbs': 70, 'fats': 12},
            {'name': 'Roti with paneer curry', 'calories': 400, 'protein': 18, 'carbs': 45, 'fats': 15},
            {'name': 'Quinoa bowl with vegetables', 'calories': 380, 'protein': 14, 'carbs': 55, 'fats': 12}
        ],
        'dinner': [
            {'name': 'Khichdi with vegetables', 'calories': 350, 'protein': 12, 'carbs': 50, 'fats': 10},
            {'name': 'Vegetable curry with brown rice', 'calories': 400, 'protein': 10, 'carbs': 60, 'fats': 12},
            {'name': 'Lentil soup with whole wheat bread', 'calories': 300, 'protein': 15, 'carbs': 40, 'fats': 8}
        ],
        'snacks': [
            {'name': 'Mixed nuts and seeds', 'calories': 200, 'protein': 8, 'carbs': 10, 'fats': 15},
            {'name': 'Greek yogurt with fruits', 'calories': 150, 'protein': 12, 'carbs': 15, 'fats': 5},
            {'name': 'Protein smoothie', 'calories': 250, 'protein': 20, 'carbs': 25, 'fats': 8}
        ]
    },
    'nonveg': {
        'breakfast': [
            {'name': 'Egg omelette with whole grain toast', 'calories': 400, 'protein': 25, 'carbs': 30, 'fats': 20},
            {'name': 'Chicken sandwich', 'calories': 450, 'protein': 30, 'carbs': 35, 'fats': 22},
            {'name': 'Protein pancakes', 'calories': 350, 'protein': 20, 'carbs': 40, 'fats': 15}
        ],
        'lunch': [
            {'name': 'Grilled chicken with brown rice', 'calories': 500, 'protein': 35, 'carbs': 45, 'fats': 20},
            {'name': 'Fish curry with roti', 'calories': 450, 'protein': 30, 'carbs': 40, 'fats': 18},
            {'name': 'Chicken salad wrap', 'calories': 400, 'protein': 25, 'carbs': 35, 'fats': 15}
        ],
        'dinner': [
            {'name': 'Grilled fish with vegetables', 'calories': 400, 'protein': 35, 'carbs': 20, 'fats': 18},
            {'name': 'Chicken stir-fry with rice', 'calories': 450, 'protein': 30, 'carbs': 40, 'fats': 20},
            {'name': 'Lean meat curry with roti', 'calories': 400, 'protein': 28, 'carbs': 35, 'fats': 15}
        ],
        'snacks': [
            {'name': 'Hard-boiled eggs', 'calories': 150, 'protein': 12, 'carbs': 1, 'fats': 10},
            {'name': 'Protein shake', 'calories': 200, 'protein': 25, 'carbs': 15, 'fats': 5},
            {'name': 'Tuna salad', 'calories': 180, 'protein': 20, 'carbs': 5, 'fats': 8}
        ]
    }
}

def generate_meal_plan(calories, macros, dietary_preference, goal):
    """Generate a meal plan based on calorie needs and dietary preferences"""
    if dietary_preference == 'vegan':
        # Use vegetarian options but exclude dairy
        meal_options = meal_db['veg']
    elif dietary_preference == 'nonveg':
        meal_options = meal_db['nonveg']
    else:
        meal_options = meal_db['veg']  # Default to vegetarian
    
    # Calculate calories per meal
    calories_per_meal = {
        'breakfast': calories * 0.25,  # 25% of daily calories
        'lunch': calories * 0.35,      # 35% of daily calories
        'dinner': calories * 0.30,     # 30% of daily calories
        'snacks': calories * 0.10      # 10% of daily calories
    }
    
    meal_plan = {}
    for meal_type, target_calories in calories_per_meal.items():
        # Find the closest matching meal
        best_meal = min(meal_options[meal_type], 
                       key=lambda x: abs(x['calories'] - target_calories))
        meal_plan[meal_type] = best_meal
    
    # Add health tips based on goal
    health_tips = []
    if goal == 'weight_loss':
        health_tips.extend([
            "Drink 2-3 liters of water daily",
            "Aim for 7-8 hours of sleep",
            "Include 30 minutes of cardio 3-4 times per week"
        ])
    elif goal == 'muscle_gain':
        health_tips.extend([
            "Consume protein within 30 minutes after workout",
            "Stay hydrated with 3-4 liters of water daily",
            "Get 8-9 hours of sleep for optimal recovery"
        ])
    else:
        health_tips.extend([
            "Maintain consistent meal timing",
            "Stay hydrated with 2-3 liters of water daily",
            "Balance cardio and strength training"
        ])
    
    return {
        'meals': meal_plan,
        'health_tips': health_tips,
        'daily_summary': {
            'total_calories': sum(meal['calories'] for meal in meal_plan.values()),
            'total_protein': sum(meal['protein'] for meal in meal_plan.values()),
            'total_carbs': sum(meal['carbs'] for meal in meal_plan.values()),
            'total_fats': sum(meal['fats'] for meal in meal_plan.values())
        }
    } 