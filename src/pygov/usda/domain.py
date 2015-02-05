__author__ = 'scarroll'


class Measure(object):

    @staticmethod
    def from_response_data(response_data):
        return Measure(quantity=response_data["qty"], gram_equivalent=response_data["eqv"],
                       label=response_data["label"], value=response_data["value"])

    def __init__(self, quantity, gram_equivalent, label, value):
        self.quantity = quantity
        self.gram_equivalent = gram_equivalent
        self.label = label
        self.value = value


class Nutrient(object):

    @staticmethod
    def from_response_data(response_data):
        return Nutrient(id=response_data['id'], name=response_data['name'])

    def __init__(self, id, name, group=None, unit=None, value=None, measures=None):
        self.id = id
        self.name = name
        self.group = group
        self.unit = unit
        self.value = value
        self.measures = measures

    def __str__(self):
        return "{0}".format(self.name)


class Food(object):

    @staticmethod
    def from_response_data(response_data):
        return Food(id=response_data['id'], name=response_data['name'])

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return "{0}".format(self.name)


class FoodReport(object):

    @staticmethod
    def __get_measures(raw_measures):
        measures = list()
        for raw_measure in raw_measures:
            measures.append(Measure.from_response_data(raw_measure))
        return measures

    @staticmethod
    def __get_nutrients(raw_nutrients):
        nutrients = list()
        for raw_nutrient in raw_nutrients:
            measures = FoodReport.__get_measures(raw_nutrient["measures"])
            nutrient = Nutrient(id=raw_nutrient["nutrient_id"], name=raw_nutrient["name"],
                                group=raw_nutrient["group"], unit=raw_nutrient["unit"], value=raw_nutrient["value"],
                                measures=measures)
            nutrients.append(nutrient)
        return nutrients

    @staticmethod
    def from_response_data(response_data):
        report = response_data["report"]
        food = report['food']
        return FoodReport(food=Food(id=food["ndbno"], name=food['name']),
                          nutrients=FoodReport.__get_nutrients(food["nutrients"]),
                          report_type=report["type"],
                          foot_notes=report["footnotes"],)

    def __init__(self, food, nutrients, report_type, foot_notes):
        self.food = food
        self.nutrients = nutrients
        self.report_type = report_type
        self.foot_notes = foot_notes