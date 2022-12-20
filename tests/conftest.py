from pytest_factoryboy import register

from tests.factories import AdFactory, CategoriesFactory, UserFactory

pytest_plugins = "tests.fixtures"

register(CategoriesFactory)
register(UserFactory)
register(AdFactory)

