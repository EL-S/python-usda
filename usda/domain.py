#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from six import with_metaclass
from abc import ABCMeta, abstractstaticmethod


class UsdaObject(with_metaclass(ABCMeta)):
    """Describes any kind of USDA API result."""

    def __init__(self):
        pass

    @abstractstaticmethod
    def from_response_data(response_data):
        """Generate an object from JSON response data."""


class Measure(UsdaObject):

    @staticmethod
    def from_response_data(response_data):
        return Measure(
            quantity=response_data["qty"],
            gram_equivalent=response_data["eqv"],
            label=response_data["label"], value=response_data["value"])

    def __init__(self, quantity, gram_equivalent, label, value):
        super(Measure, self).__init__()
        self.quantity = float(quantity)
        self.gram_equivalent = float(gram_equivalent)
        self.label = str(label)
        self.value = float(value)

    def __repr__(self):
        return "Measure '{0}': {1} {2}".format(
            self.label, self.value, self.quantity)

    def __str__(self):
        return self.label


class Nutrient(UsdaObject):
    """Describes a USDA nutrient.
    In reports, can hold associated measurement data."""

    @staticmethod
    def from_response_data(response_data):
        return Nutrient(id=response_data['id'], name=response_data['name'])

    def __init__(self, id, name,
                 group=None, unit=None, value=None, measures=None):
        super(Nutrient, self).__init__()
        self.id = int(id)
        self.name = str(name)
        self.group = str(group) if group is not None else None
        self.unit = str(unit) if unit is not None else None
        self.value = float(value) if value is not None else None
        self.measures = measures

    def __str__(self):
        return self.name

    def __repr__(self):
        return "Nutrient ID {0} '{1}'".format(self.id, self.name)


class Food(UsdaObject):
    """Describes a USDA food item."""

    @staticmethod
    def from_response_data(response_data):
        return Food(id=response_data['id'], name=response_data['name'])

    def __init__(self, id, name):
        super(Food, self).__init__()
        self.id = int(id)
        self.name = str(name)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "Food ID {0} '{1}'".format(self.id, self.name)


class FoodReport(UsdaObject):
    """Describes a USDA food report."""

    @staticmethod
    def _get_measures(raw_measures):
        """Get measurements from JSON data."""
        measures = list()
        for raw_measure in raw_measures:
            measures.append(Measure.from_response_data(raw_measure))
        return measures

    @staticmethod
    def _get_nutrients(raw_nutrients):
        """Get nutrients from JSON data with their associated measurements."""
        nutrients = list()
        for raw_nutrient in raw_nutrients:
            measures = FoodReport._get_measures(raw_nutrient["measures"])
            nutrient = Nutrient(
                id=raw_nutrient["nutrient_id"], name=raw_nutrient["name"],
                group=raw_nutrient["group"], unit=raw_nutrient["unit"],
                value=raw_nutrient["value"], measures=measures)
            nutrients.append(nutrient)
        return nutrients

    @staticmethod
    def from_response_data(response_data):
        report = response_data["report"]
        type = report["type"]
        food = report['food']
        food_group = None if type == "Basic" or type == "Statistics" \
            else food["fg"]
        return FoodReport(
            food=Food(id=food["ndbno"], name=food['name']),
            nutrients=FoodReport._get_nutrients(food["nutrients"]),
            report_type=report["type"],
            foot_notes=report["footnotes"], food_group=food_group)

    def __init__(self, food, nutrients, report_type, foot_notes, food_group):
        super(FoodReport, self).__init__()
        assert isinstance(food, Food)
        self.food = food
        self.nutrients = nutrients
        self.report_type = str(report_type)
        self.foot_notes = foot_notes
        self.food_group = str(food_group) if food_group is not None else None

    def __repr__(self):
        return "Food Report for '{0}'".format(repr(self.food))
