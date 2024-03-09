import pytest
from pydantic import ValidationError

from core.models.foods import FoodModel


def test_valid_food_model():
    data = {
        "name": "Basmati Rice",
        "description": "Long grain foreign rice from Asia",
        "amount_per_scoop": 1550.21,
    }

    # This should not raise any validation errors
    food = FoodModel(**data)

    # Assert that the values match the expected values
    assert food.name == "Basmati Rice"
    assert food.description == "Long grain foreign rice from Asia"
    assert food.amount_per_scoop == 1550.21


def test_invalid_food_model():
    # Test with missing 'amount_per_scoop'
    data = {
        "name": "Basmati Rice",
        "description": "Long grain foreign rice from Asia",
    }

    # This should raise a ValidationError
    with pytest.raises(ValidationError):
        FoodModel(**data)


def test_food_model_example():
    # Test the example data provided in the model's JSON schema
    example_data = {
        "name": "Basmati Rice",
        "description": "Long grain foreign rice from Asia",
        "amount_per_scoop": 1550.21,
    }

    # This should not raise any validation errors
    food = FoodModel(**example_data)

    # Assert that the values match the expected values
    assert food.name == "Basmati Rice"
    assert food.description == "Long grain foreign rice from Asia"
    assert food.amount_per_scoop == 1550.21

    # Optional: Add more assertions as needed for your specific use case
