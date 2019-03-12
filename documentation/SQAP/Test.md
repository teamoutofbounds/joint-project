## 7. Test

### 7.1. Development testing
The main idea is to create automatized tests, that can be executed every time someone makes a change in the code, in order to verify if the change could affect or have any unexpectedness impact in the application behavior. This tests have to be reliable and easy to run every time someone makes a change in the code.

### 7.1.1 What should be tested
All the aspects of the code should be tested, but not any library or functionality provided as a part of Python or Django.
• If the code in question is a built-in Python function/library, don't test it. Examples like the datetime library.
• If the code in question is built into Django, don't test it. Examples like the fields on a Model or testing how the built-in template. Node renders included tags.
• If your model has custom methods, you should test that, usually with unit tests.
• Same goes for custom views, forms, template tags, context processors, middleware, management commands, etc. If you implemented the business logic, you should test your aspects of the code.

#### 7.1.2.  Test structure
  app/
      /tests/
          __init__.py
          test_models.py
          test_forms.py
          test_views.py


### 7.1.3.  Tools for testing

• unittest.mock: to patch third party libraries in order to more thoroughly test the code.
• Coverage: Coverage measurement is typically used to gauge the effectiveness of tests. It can show which parts of your code are being exercised by tests, and which are not.
• Selenium: is a framework to automate testing in a real browser. It allows you to simulate a real user interacting with the site, and provides a great framework for system testing your site (the next step up from integration testing.
