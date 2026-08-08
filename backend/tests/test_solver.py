from backend.src.solver import calculate
import pytest
from backend.src.database import get_recipe

def test_iron_ingot():
    errors = []
    recipe_vars = calculate('Iron Ingot', 'Iron Ingot')

    if recipe_vars['Desc_IronIngot_C'] != 120:
        errors.append(f'Incorrect value for Desc_IronIngot_C: expected 120, received {recipe_vars['Desc_IronIngot_C']}')

    assert not errors, "Errors occured:\n{}".format("\n".join(errors))

def test_plastic():
    errors = []
    recipe_vars = calculate('Plastic', 'Plastic')

    if recipe_vars['Desc_Plastic_C'] != 160:
        errors.append(f'Incorrect value for Desc_Plastic_C: expected 160, received {recipe_vars['Desc_Plastic_C']}')

    assert not errors, "Errors occured:\n{}".format("\n".join(errors))

def test_reinforced_plate():
    errors = []
    recipe_vars = calculate('Reinforced Iron Plate', 'Reinforced Iron Plate')

    if recipe_vars['Desc_IronPlateReinforced_C'] != 10:
        errors.append(f'Incorrect value for Desc_IronPlateReinforced_C: expected 10, received {recipe_vars['Desc_IronPlateReinforced_C']}')
    if recipe_vars['Desc_IronPlate_C'] != 60:
        errors.append(f'Incorrect value for Desc_IronPlate_C: expected 60, received {recipe_vars['Desc_IronPlate_C']}')
    if recipe_vars['Desc_IronScrew_C'] != 120:
        errors.append(f'Incorrect value for Desc_IronScrew_C: expected 120, received {recipe_vars['Desc_IronScrew_C']}')
    if recipe_vars['Desc_IronIngot_C'] != 120:
        errors.append(f'Incorrect value for Desc_IronIngot_C: expected 120, received {recipe_vars['Desc_IronIngot_C']}')
    if recipe_vars['Desc_IronRod_C'] != 30:
        errors.append(f'Incorrect value for Desc_IronRod_C: expected 30, received {recipe_vars['Desc_IronRod_C']}')

    assert not errors, "Errors occured:\n{}".format("\n".join(errors))

def test_ai_limiter():
    errors = []
    recipe_vars = calculate('AI Limiter', 'AI Limiter')

    if recipe_vars['Desc_CircuitBoardHighSpeed_C'] != 10:
        errors.append(f'Incorrect value for Desc_CircuitBoardHighSpeed_C: expected 10, received {recipe_vars['Desc_CircuitBoardHighSpeed_C']}')
    if recipe_vars['Desc_CopperSheet_C'] != 60:
        errors.append(f'Incorrect value for Desc_CopperSheet_C: expected 60, received {recipe_vars['Desc_CopperSheet_C']}')
    if recipe_vars['Desc_HighSpeedWire_C'] != 200:
        errors.append(f'Incorrect value for Desc_HighSpeedWire_C: expected 200, received {recipe_vars['Desc_HighSpeedWire_C']}')
    if recipe_vars['Desc_CopperIngot_C'] != 120:
        errors.append(f'Incorrect value for Desc_CopperIngot_C: expected 120, received {recipe_vars['Desc_CopperIngot_C']}')
    if recipe_vars['Desc_GoldIngot_C'] != 40:
        errors.append(f'Incorrect value for Desc_GoldIngot_C: expected 40, received {recipe_vars['Desc_GoldIngot_C']}')

    assert not errors, "Errors occured:\n{}".format("\n".join(errors))

def test_stator():
    errors = []
    recipe_vars = calculate('Stator', 'Stator')

    if recipe_vars['Desc_Stator_C'] != pytest.approx(26.6667, abs=1e-3):
        errors.append(f'Incorrect value for Desc_Stator_C: expected 26.6667, received {recipe_vars['Desc_Stator_C']}')
    if recipe_vars['Desc_SteelPipe_C'] != 80:
        errors.append(f'Incorrect value for Desc_SteelPipe_C: expected 80, received {recipe_vars['Desc_SteelPipe_C']}')
    if recipe_vars['Desc_Wire_C'] != pytest.approx(240):
            errors.append(f'Incorrect value for Desc_Wire_C: expected 240, received {recipe_vars['Desc_Wire_C']}')
    # if recipe_vars['Desc_Wire_C'] != pytest.approx(213.3333, abs=1e-3):
    #     errors.append(f'Incorrect value for Desc_Wire_C: expected 213.3333, received {recipe_vars['Desc_Wire_C']}')
    if recipe_vars['Desc_SteelIngot_C'] != 120:
        errors.append(f'Incorrect value for Desc_SteelIngot_C: expected 120, received {recipe_vars['Desc_SteelIngot_C']}')
    if recipe_vars['Desc_CopperIngot_C'] != pytest.approx(120):
        errors.append(f'Incorrect value for Desc_CopperIngot_C: expected 120, received {recipe_vars['Desc_CopperIngot_C']}')
    # if recipe_vars['Desc_CopperIngot_C'] != pytest.approx(106.6667, abs=1e-3):
    #     errors.append(f'Incorrect value for Desc_CopperIngot_C: expected 106.6667, received {recipe_vars['Desc_CopperIngot_C']}')

    assert not errors, "Errors occured:\n{}".format("\n".join(errors))

def test_computer():
    errors = []
    recipe_vars = calculate('Computer', 'Computer')

    if recipe_vars['Desc_Computer_C'] != 5:
        errors.append(f'Incorrect value for Desc_Computer_C: expected 5, received {recipe_vars['Desc_Computer_C']}')
    if recipe_vars['Desc_CircuitBoard_C'] != 20:
        errors.append(f'Incorrect value for Desc_CircuitBoard_C: expected 20, received {recipe_vars['Desc_CircuitBoard_C']}')
    if recipe_vars['Desc_Cable_C'] != 40:
        errors.append(f'Incorrect value for Desc_Cable_C: expected 40, received {recipe_vars['Desc_Cable_C']}')
    if recipe_vars['Desc_Plastic_C'] != 160:
        errors.append(f'Incorrect value for Desc_Plastic_C: expected 160, received {recipe_vars['Desc_Plastic_C']}')
    if recipe_vars['Desc_CopperSheet_C'] != 40:
        errors.append(f'Incorrect value for Desc_CopperSheet_C: expected 40, received {recipe_vars['Desc_CopperSheet_C']}')
    if recipe_vars['Desc_Wire_C'] != 80:
        errors.append(f'Incorrect value for Desc_Wire_C: expected 80, received {recipe_vars['Desc_Wire_C']}')
    if recipe_vars['Desc_CopperIngot_C'] != 120:
        errors.append(f'Incorrect value for Desc_CopperIngot_C: expected 120, received {recipe_vars['Desc_CopperIngot_C']}')

    assert not errors, "Errors occured:\n{}".format("\n".join(errors))

def test_iron_ingot_list():
    errors = []
    recipes = [get_recipe('Iron Ingot')]
    recipe_vars = calculate('Iron Ingot', 'Iron Ingot', recipes)

    if recipe_vars['Desc_IronIngot_C'] != 120:
        errors.append(f'Incorrect value for Desc_IronIngot_C: expected 120, received {recipe_vars['Desc_IronIngot_C']}')

    assert not errors, "Errors occured:\n{}".format("\n".join(errors))

def test_reinforced_plate_list():
    errors = []
    recipes = [
        get_recipe('Reinforced Iron Plate'),
        get_recipe('Iron Plate'),
        get_recipe('Screws'),
        get_recipe('Iron Ingot'),
        get_recipe('Iron Rod')
    ]
    recipe_vars = calculate('Reinforced Iron Plate', 'Reinforced Iron Plate', recipes)

    if recipe_vars['Desc_IronPlateReinforced_C'] != 10:
        errors.append(f'Incorrect value for Desc_IronPlateReinforced_C: expected 10, received {recipe_vars['Desc_IronPlateReinforced_C']}')
    if recipe_vars['Desc_IronPlate_C'] != 60:
        errors.append(f'Incorrect value for Desc_IronPlate_C: expected 60, received {recipe_vars['Desc_IronPlate_C']}')
    if recipe_vars['Desc_IronScrew_C'] != 120:
        errors.append(f'Incorrect value for Desc_IronScrew_C: expected 120, received {recipe_vars['Desc_IronScrew_C']}')
    if recipe_vars['Desc_IronIngot_C'] != 120:
        errors.append(f'Incorrect value for Desc_IronIngot_C: expected 120, received {recipe_vars['Desc_IronIngot_C']}')
    if recipe_vars['Desc_IronRod_C'] != 30:
        errors.append(f'Incorrect value for Desc_IronRod_C: expected 30, received {recipe_vars['Desc_IronRod_C']}')

    assert not errors, "Errors occured:\n{}".format("\n".join(errors))

def test_alternate_iron_ingot():
    errors = []
    recipes = [get_recipe('Basic Iron Ingot')]
    recipe_vars = calculate('Iron Ingot', 'Basic Iron Ingot', recipes)

    if recipe_vars['Desc_IronIngot_C'] != 150:
        errors.append(f'Incorrect value for Desc_IronIngot_C: expected 150, received {recipe_vars['Desc_IronIngot_C']}')

    assert not errors, "Errors occured:\n{}".format("\n".join(errors))

def test_automated_miner():
    errors = []
    recipe_vars = calculate('Portable Miner', 'Automated Miner')

    if recipe_vars['BP_ItemDescriptorPortableMiner_C'] != 10:
        errors.append(f'Incorrect value for BP_ItemDescriptorPortableMiner_C: expected 10, received {recipe_vars['BP_ItemDescriptorPortableMiner_C']}')
    if recipe_vars['Desc_SteelPipe_C'] != 40:
        errors.append(f'Incorrect value for Desc_SteelPipe_C: expected 40, received {recipe_vars['Desc_SteelPipe_C']}')
    if recipe_vars['Desc_IronPlate_C'] != 40:
        errors.append(f'Incorrect value for Desc_IronPlate_C: expected 40, received {recipe_vars['Desc_IronPlate_C']}')
    if recipe_vars['Desc_SteelIngot_C'] != 60:
        errors.append(f'Incorrect value for Desc_SteelIngot_C: expected 60, received {recipe_vars['Desc_SteelIngot_C']}')
    if recipe_vars['Desc_IronIngot_C'] != 60:
        errors.append(f'Incorrect value for Desc_IronIngot_C: expected 60, received {recipe_vars['Desc_IronIngot_C']}')

    assert not errors, "Errors occured:\n{}".format("\n".join(errors))