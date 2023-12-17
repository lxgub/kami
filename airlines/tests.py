from django.test import SimpleTestCase
from unittest.mock import patch, MagicMock
from decimal import Decimal
from airlines.models import Airplane
from airlines.schemas import ApiResponseInfo
from airlines.v1.calculations import BaseAircraftCalculator
from airlines.v1.get_aircraft import GetAircraftUseCase


class AirplaneTestCase(SimpleTestCase):

    def test_airplane_str_method(self) -> None:
        airplane = Airplane(airplane_identifier=2, passenger_capacity=100)
        self.assertEqual(
            str(airplane),
            '2 | 100 | None'
        )


class BaseAircraftCalculatorTestCase(SimpleTestCase):
    def test_base_aircraft_calculator_1(self) -> None:
        calculator = BaseAircraftCalculator(
            airplane_identifier=2,
            passenger_capacity=100
        )
        calculator._calculate_real_tank_capacity = MagicMock(return_value=None)  # type: ignore
        calculator._calculate_real_consumption = MagicMock(return_value=None)  # type: ignore
        result = calculator.get_result()
        self.assertIsInstance(result, dict)
        self.assertIn('fuel_consumption', result)
        self.assertIn('flight_minutes', result)

    def test_base_aircraft_calculator_2(self) -> None:
        """
        The logarithm of 1 to any base is equal to 0. Therefore, the aircraft ID cannot be 1.
        """
        calculator = BaseAircraftCalculator(
            airplane_identifier=1,
            passenger_capacity=100
        )
        result = calculator._get_base_consumption()
        self.assertEqual(result, Decimal('0.0'))


class GetAircraftUseCaseTestCase(SimpleTestCase):

    def test_get_aircraft_use_case(self) -> None:
        airplane_identifier = 2
        passenger_capacity = 100
        mock_airplane = Airplane(airplane_identifier=airplane_identifier, passenger_capacity=passenger_capacity)
        with patch('airlines.v1.get_aircraft.GetAircraftUseCase._get_aircraft', return_value=mock_airplane):
            response = GetAircraftUseCase()(airplane_identifier)
        self.assertIsInstance(response[1], ApiResponseInfo)
        self.assertEqual(response[0], 200)
        self.assertIsInstance(response[1].results, dict)
        self.assertIn('fuel_consumption', response[1].results)
        self.assertIn('flight_minutes', response[1].results)
        self.assertEqual(response[1].results['fuel_consumption'],
                         Decimal('0.7545177444479562289814111864'))
