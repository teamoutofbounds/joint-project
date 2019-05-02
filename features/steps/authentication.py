from behave import *

use_step_matcher("parse")


@given('Exists a user "{username}" with password "{password}"')
def step_impl(context, username, password):
    pass
    ''''
    from django.contrib.auth.models import User
    User.objects.create_user(username=username, email='user@example.com', password=password)
    '''


@given('I login as user "{username}" with password "{password}"')
def step_impl(context, username, password):
    pass
    '''
    context.browser.visit(context.get_url('/users/'))
    form = context.browser.find_by_tag('form').first
    context.browser.fill('username', username)
    context.browser.fill('password', password)
    form.find_by_value('login').first.click()
    assert context.browser.is_text_present('User: ' + username)
    '''


@step('I am not logged in')
def step_impl(context):
    pass
    '''
    context.browser.visit(context.get_url('logout')+'?next=/magatzem/')
    assert context.browser.is_text_present('login')
    '''


@then("I'm redirected to the login form")
def step_impl(context):
    pass
    '''
    assert context.browser.url.startswith(context.get_url('login'))
    '''


@then('There is "{link_text}" link available')
def step_impl(context, link_text):
    pass
    '''
    assert context.browser.is_element_present_by_xpath('//a[text()="'+link_text+'"]')
    '''


@then('There is no "{link_text}" link available')
def step_impl(context, link_text):
    pass
    '''
    assert context.browser.is_element_not_present_by_xpath('//a[text()="'+link_text+'"]')
    '''


@then('Server responds with page containing "{message}"')
def step_impl(context, message):
    pass
    '''
    assert context.browser.is_text_present(message)
    '''