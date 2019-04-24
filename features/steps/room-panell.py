from behave import *

use_step_matcher("parse")


@given('Exists a user "{user2}" with password "{password}"')
def step_impl(context, user2, password):
    """
    :param user2:
    :param password:
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: And Exists a user "user2" with password "password"')
