from backend.src.solver import calculate
import pytest

def test_iron_ingot():
    errors = []
    prob_vars = calculate('Iron Ingot')

    if prob_vars['Desc_IronIngot_C'].varValue != 120:
        errors.append(f'Incorrect value for Desc_IronIngot_C: expected 120, received {prob_vars['Desc_IronIngot_C'].varValue}')
    if prob_vars['Desc_OreIron_C'].varValue != 120:
        errors.append(f'Incorrect value for Desc_OreIron_C: expected 120, received {prob_vars['Desc_OreIron_C'].varValue}')

    assert not errors, "Errors occured:\n{}".format("\n".join(errors))

def test_plastic():
    errors = []
    prob_vars = calculate('Plastic')

    if prob_vars['Desc_Plastic_C'].varValue != 160:
        errors.append(f'Incorrect value for Desc_Plastic_C: expected 160, received {prob_vars['Desc_Plastic_C'].varValue}')
    if prob_vars['Desc_LiquidOil_C'].varValue != 240:
        errors.append(f'Incorrect value for Desc_LiquidOil_C: expected 240, received {prob_vars['Desc_LiquidOil_C'].varValue}')

    assert not errors, "Errors occured:\n{}".format("\n".join(errors))

def test_reinforced_plate():
    errors = []
    prob_vars = calculate('Reinforced Iron Plate')

    if prob_vars['Desc_IronPlateReinforced_C'].varValue != 10:
        errors.append(f'Incorrect value for Desc_IronPlateReinforced_C: expected 10, received {prob_vars['Desc_IronPlateReinforced_C'].varValue}')
    if prob_vars['Desc_IronPlate_C'].varValue != 60:
        errors.append(f'Incorrect value for Desc_IronPlate_C: expected 60, received {prob_vars['Desc_IronPlate_C'].varValue}')
    if prob_vars['Desc_IronScrew_C'].varValue != 120:
        errors.append(f'Incorrect value for Desc_IronScrew_C: expected 120, received {prob_vars['Desc_IronScrew_C'].varValue}')
    if prob_vars['Desc_IronIngot_C'].varValue != 120:
        errors.append(f'Incorrect value for Desc_IronIngot_C: expected 120, received {prob_vars['Desc_IronIngot_C'].varValue}')
    if prob_vars['Desc_IronRod_C'].varValue != 30:
        errors.append(f'Incorrect value for Desc_IronRod_C: expected 30, received {prob_vars['Desc_IronRod_C'].varValue}')
    if prob_vars['Desc_OreIron_C'].varValue != 120:
        errors.append(f'Incorrect value for Desc_OreIron_C: expected 120, received {prob_vars['Desc_OreIron_C'].varValue}')

    assert not errors, "Errors occured:\n{}".format("\n".join(errors))

def test_ai_limiter():
    errors = []
    prob_vars = calculate('AI Limiter')

    if prob_vars['Desc_CircuitBoardHighSpeed_C'].varValue != 10:
        errors.append(f'Incorrect value for Desc_CircuitBoardHighSpeed_C: expected 10, received {prob_vars['Desc_CircuitBoardHighSpeed_C'].varValue}')
    if prob_vars['Desc_CopperSheet_C'].varValue != 50:
        errors.append(f'Incorrect value for Desc_CopperSheet_C: expected 50, received {prob_vars['Desc_CopperSheet_C'].varValue}')
    if prob_vars['Desc_HighSpeedWire_C'].varValue != 200:
        errors.append(f'Incorrect value for Desc_HighSpeedWire_C: expected 200, received {prob_vars['Desc_HighSpeedWire_C'].varValue}')
    if prob_vars['Desc_CopperIngot_C'].varValue != 100:
        errors.append(f'Incorrect value for Desc_CopperIngot_C: expected 100, received {prob_vars['Desc_CopperIngot_C'].varValue}')
    if prob_vars['Desc_GoldIngot_C'].varValue != 40:
        errors.append(f'Incorrect value for Desc_GoldIngot_C: expected 40, received {prob_vars['Desc_GoldIngot_C'].varValue}')
    if prob_vars['Desc_OreCopper_C'].varValue != 100:
        errors.append(f'Incorrect value for Desc_OreCopper_C: expected 100, received {prob_vars['Desc_OreCopper_C'].varValue}')
    if prob_vars['Desc_OreGold_C'].varValue != 120:
        errors.append(f'Incorrect value for Desc_OreGold_C: expected 120, received {prob_vars['Desc_OreGold_C'].varValue}')

    assert not errors, "Errors occured:\n{}".format("\n".join(errors))

def test_stator():
    errors = []
    prob_vars = calculate('Stator')

    if prob_vars['Desc_Stator_C'].varValue != pytest.approx(26.6667, abs=1e-3):
        errors.append(f'Incorrect value for Desc_Stator_C: expected 26.6667, received {prob_vars['Desc_Stator_C'].varValue}')
    if prob_vars['Desc_SteelPipe_C'].varValue != 80:
        errors.append(f'Incorrect value for Desc_SteelPipe_C: expected 80, received {prob_vars['Desc_SteelPipe_C'].varValue}')
    if prob_vars['Desc_Wire_C'].varValue != pytest.approx(213.3333, abs=1e-3):
        errors.append(f'Incorrect value for Desc_Wire_C: expected 213.3333, received {prob_vars['Desc_Wire_C'].varValue}')
    if prob_vars['Desc_SteelIngot_C'].varValue != 120:
        errors.append(f'Incorrect value for Desc_SteelIngot_C: expected 120, received {prob_vars['Desc_SteelIngot_C'].varValue}')
    if prob_vars['Desc_CopperIngot_C'].varValue != pytest.approx(106.6667, abs=1e-3):
        errors.append(f'Incorrect value for Desc_CopperIngot_C: expected 106.6667, received {prob_vars['Desc_CopperIngot_C'].varValue}')
    if prob_vars['Desc_OreIron_C'].varValue != 120:
        errors.append(f'Incorrect value for Desc_OreIron_C: expected 120, received {prob_vars['Desc_OreIron_C'].varValue}')
    if prob_vars['Desc_Coal_C'].varValue != 120:
        errors.append(f'Incorrect value for Desc_Coal_C: expected 120, received {prob_vars['Desc_Coal_C'].varValue}')
    if prob_vars['Desc_OreCopper_C'].varValue != pytest.approx(106.6667, abs=1e-3):
        errors.append(f'Incorrect value for Desc_OreCopper_C: expected 106.6667, received {prob_vars['Desc_OreCopper_C'].varValue}')

    assert not errors, "Errors occured:\n{}".format("\n".join(errors))

def test_computer():
    errors = []
    prob_vars = calculate('Computer')

    if prob_vars['Desc_Computer_C'].varValue != 5:
        errors.append(f'Incorrect value for Desc_Computer_C: expected 5, received {prob_vars['Desc_Computer_C'].varValue}')
    if prob_vars['Desc_CircuitBoard_C'].varValue != 20:
        errors.append(f'Incorrect value for Desc_CircuitBoard_C: expected 20, received {prob_vars['Desc_CircuitBoard_C'].varValue}')
    if prob_vars['Desc_Cable_C'].varValue != 40:
        errors.append(f'Incorrect value for Desc_Cable_C: expected 40, received {prob_vars['Desc_Cable_C'].varValue}')
    if prob_vars['Desc_Plastic_C'].varValue != 160:
        errors.append(f'Incorrect value for Desc_Plastic_C: expected 160, received {prob_vars['Desc_Plastic_C'].varValue}')
    if prob_vars['Desc_CopperSheet_C'].varValue != 40:
        errors.append(f'Incorrect value for Desc_CopperSheet_C: expected 40, received {prob_vars['Desc_CopperSheet_C'].varValue}')
    if prob_vars['Desc_Wire_C'].varValue != 80:
        errors.append(f'Incorrect value for Desc_Wire_C: expected 80, received {prob_vars['Desc_Wire_C'].varValue}')
    if prob_vars['Desc_LiquidOil_C'].varValue != 240:
        errors.append(f'Incorrect value for Desc_LiquidOil_C: expected 240, received {prob_vars['Desc_LiquidOil_C'].varValue}')
    if prob_vars['Desc_CopperIngot_C'].varValue != 120:
        errors.append(f'Incorrect value for Desc_CopperIngot_C: expected 120, received {prob_vars['Desc_CopperIngot_C'].varValue}')
    if prob_vars['Desc_OreCopper_C'].varValue != 120:
        errors.append(f'Incorrect value for Desc_OreCopper_C: expected 120, received {prob_vars['Desc_OreCopper_C'].varValue}')

    assert not errors, "Errors occured:\n{}".format("\n".join(errors))