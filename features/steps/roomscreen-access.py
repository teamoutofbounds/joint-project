from behave import *
# from magatzem.models import Room

use_step_matcher("re")


@when("I access the rooms screen")
def step_impl(context):
    pass
    '''
    context.browser.visit(context.get_url('magatzem:list-room'))
    '''


@step("There are no rooms")
def step_impl(context):
    pass
    '''
    assert Room.objects.count() == 0
    '''


@step("There is at least one room")
def step_impl(context):
    pass
    '''
    assert Room.objects.count() >= 1
    '''

