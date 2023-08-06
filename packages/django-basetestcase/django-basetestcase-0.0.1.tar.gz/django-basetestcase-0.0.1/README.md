============
BaseTestCase
============

BaseTestCase is a collection of cheater methods for the Django TestCase.
These came about as a result of learning and using TDD.

There are four different classes:

    1. ModelTestCase
    2. FormTestCase
    3. ViewTestCase
    4. FunctionalTest
        - For use with Selenium.
        - Origins and some methods from "Obey The Testing Goat".


Quick start
-----------

1. Add "django-BaseTestCase" to your INSTALLED_APPS setting like this:

    INSTALLED_APPS = [
        ...
        'django-BaseTestCase',
    ]

2. Import into test and use:

    from django-BaseTestCase import ModelTestCase
    
    class ModelTest(ModelTestCase):
    
    ...