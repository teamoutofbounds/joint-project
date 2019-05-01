from behave import *

use_step_matcher("re")


@step("There is a product assigned to a room")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: And There is a product assigned to a room')