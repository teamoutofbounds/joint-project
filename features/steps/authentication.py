from behave import *

use_step_matcher("parse")


@given('Exists a user "{user_name}" with password "{password}"')
def step_impl(context, user_name, password):
    from django.contrib.auth.models import User
    User.objects.create_user(username=user_name, email='user@exaple.com', password=password)


@given('Exists a role "{role_name}"')
def step_impl(context, role_name):
    from django.contrib.auth.models import Group
    Group.objects.get_or_create(name=role_name)


@step('I\'m a user "{user_name}" with role is "{role_name}"')
def step_impl(context, user_name, role_name):
    from django.contrib.auth.models import Group
    role = Group.objects.get(name=role_name)
    from django.contrib.auth.models import User
    user = User.objects.get(username=user_name)
    user.groups.add(role)


@when('I login as user "{user_name}" with password "{password}"')
def step_impl(context, user_name, password):
    # context.browser.visit(context.get_url('/login'))
    # form = context.browser.find_by_tag('form').first
    # context.browser.fill('username', user_name)
    # context.browser.fill('password', password)
    # form.find_by_value('login').first.click()
    pass


@then('As a user "{user_name}" I\'m viewing the Gestor landing page')
def step_impl(context, user_name):
    # assert context.browser.is_text_present(user_name)
    pass
