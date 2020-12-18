from . import blueprint
from flask import render_template
from flask_login import login_required

from flask import (current_app as app, request, render_template, abort,
                   url_for, session, redirect)
from app.models import (
    CNFFoodName, CNFConversionFactor, CNFNutrientAmount,
    CNFYieldAmount, CNFRefuseAmount)

@blueprint.route('/food_search', methods=['GET', 'POST'])
@login_required
def cnf_food_search():
    q = request.args.get('q')
    foods = CNFFoodName.objects.filter(description__icontains=q) if q else []
    return render_template('main/food_search.html', foods=foods, q=q)


@blueprint.route('/<int:food_id>', methods=['GET'])
@login_required
def cnf_show(food_id):
    food = CNFFoodName.objects.get(id=str(food_id))
    conversions = CNFConversionFactor.objects.filter(food=food)
    nutrients = CNFNutrientAmount.objects.filter(food=food, nutrient_value__gt=-1)
    yields = CNFYieldAmount.objects.filter(food=food)
    refuses = CNFRefuseAmount.objects.filter(food=food)
    return render_template(
        'main/show.html',
        food=food,
        conversions=conversions,
        nutrients=nutrients,
        yields=yields,
        refuses=refuses,
    )
