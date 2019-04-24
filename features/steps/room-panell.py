from behave import *

use_step_matcher("parse")


@step('Exists a user "user2" with password "password"')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: And Exists a user "user2" with password "password"')