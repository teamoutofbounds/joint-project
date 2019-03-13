## 7. Test

### 7.1. Development testing
The main idea is to create automatized tests, that can be executed every time someone makes a change in the code, in order to verify if the change could affect or have any unexpectedness impact in the application behavior. This tests have to be reliable and easy to run every time someone makes a change in the code.


### 7.1.1 Previous considerations

#### 7.1.1.1 What should be tested
All the aspects of the code should be tested, but not any library or functionality provided as a part of Python or Django.
• If the code in question is a built-in Python function/library, don't test it. Examples like the datetime library.
• If the code in question is built into Django, don't test it. Examples like the fields on a Model or testing how the built-in template. Node renders included tags.
• If your model has custom methods, you should test that, usually with unit tests.
• Same goes for custom views, forms, template tags, context processors, middleware, management commands, etc. If you implemented the business logic, you should test your aspects of the code.

#### 7.1.1.2.  Test structure
  app/
      /tests/
          __init__.py
          test_models.py
          test_forms.py
          test_views.py

#### 7.1.1.3.  Tools for testing

• unittest.mock: to patch third party libraries in order to more thoroughly test the code.
• Coverage: Coverage measurement is typically used to gauge the effectiveness of tests. It can show which parts of your code are being exercised by tests, and which are not.
• Selenium: is a framework to automate testing in a real browser. It allows you to simulate a real user interacting with the site, and provides a great framework for system testing your site (the next step up from integration testing.


###  7.1.2. Unit tests

The unit test must be made on a single component. The component isolation is an inexcusable requirement in this testing stage to guarantee the component behavior correctness.
We are using unit test during the production process with two main objectives:
• When we are writing code, we are going to use test to ensure the code works as we expect.
• When we are refactoring the code, we are going to use test to ensure our changes haven’t affect our application’s behavior unexpectedly.

Test frameworks to do unit tests:
• unittest (the standard library module).
• django.test.TestCase (A subclasses from django.test.TestCase, which is a subclass of unittest.TestCase that runs each test inside a Transaction to provide isolation).


### 7.1.3. Integration tests
Verify how groupings of components work when used together. Integration tests are aware of the required interactions between components, but not necessarily of the internal operations of each component. They may cover simple groupings of components through to the whole website.


### 7.1.4. System tests
System tests are the same as integration test, but this time the test is for the whole application.
To do Integration Testing you need your app to run as if it were in production. You want the HTTP server running and accepting requests. You want it to receive an actual HTTP request, execute and render a view, interact with the view in a real browser, click the button in such browser, see what happens in the browser and then back at your server, check if what you need to have it written in the DB gets written in the DB, and so on.

Test frameworks to do integration tests:
django.test.LiveServerTestCase

Tools:
Selenium


### 7.1.5. Regression tests
Tests that reproduce historic bugs. Each test is initially run to verify that the bug has been fixed, and then re-run to ensure that it has not been reintroduced following later changes to the code.
Every time a bug appears, after it is addressed, a test must be written to ensure the bug is not going to reappear later on.


### 7.2. User testing

### 7.2.1. Acceptance tests

The acceptance testing is going to be made in three steeps:

• Internal Acceptance Testing (Also known as Alpha Testing) is going to be performed by a members of the organization that developed the software but who are not directly involved in the project (Development or Testing).
• External Acceptance Testing is going to be performed by people who are not employees of the organization that developed the software:
◦ Customer Acceptance Testing is going to be performed by the customers of the organization that developed the software. They are the ones who asked the organization to develop the software.
◦ User Acceptance Testing (Also known as Beta Testing) is going to be performed by the end users of the software.

Acceptance testing types:
• Contract Acceptance Testing (developed software is tested against certain criteria and specifications which are predefined and agreed upon in a contract).
• Regulation Acceptance Testing (examines whether the software complies with the regulations. This includes governmental and legal regulations).
• Operational acceptance testing (these test cases ensure there are workflows in place to allow the software or system to be used.
This should include workflows for backup plans, user training, and various maintenance processes and security checks).


### 7.3. References

#### 7.3.1. Guides:
• Writing and running tests (Django docs)
• Writing your first Django app, part 5 > Introducing automated testing (Django docs)
• Testing tools reference (Django docs)
• Advanced testing topics (Django docs)
• A Guide to Testing in Django (Toast Driven Blog, 2011)
• Workshop: Test-Driven Web Development with Django (San Diego Python, 2014)
• Testing in Django (Part 1) - Best Practices and Examples (RealPython, 2013)

#### 7.3.2. Testing tools:
• unittest.mock (python docs)
• Coverage (Coverage.py docs)
• Selenium (mozilla docs)
