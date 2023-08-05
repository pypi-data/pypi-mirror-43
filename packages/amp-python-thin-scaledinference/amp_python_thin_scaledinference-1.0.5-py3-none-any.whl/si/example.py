"""
Example code to illustrate how to use the Scaled Inference python api.
To run this code (assuming the amp_agents addresses are correct and the project key is valid) use:
    python example.py --amp_agents 'amp2-dev-clientsim-0,amp2-dev-clientsim-1' --key '1622f1831b45819b'
"""
import argparse
import logging
import src.si.amp as amp


def example_code(amp_agents, key):
    """
    Example code that illustrates use of the SI python library.
    """
    # First step: create one "amp" object for each project key.
    #   Since there is only one project, there will only be one amp object.
    #   key and amp_agents are required in the options dictionary
    # If there is a problem with the key, or any of the amp_agents, it doesn't make sense to create an amp object,
    # and an exception will be thrown.
    amp_object = amp.Amp(key=key, amp_agents=amp_agents, logger=logging.getLogger(__name__))
    # Now session objects associated with this project can be created.
    #    For illustration, one session are created here.
    #    The amp_object does not keep a reference to this object.
    #    It is the client's responsibility to manage it.
    first_session = amp_object.session()
    # Once a session exists, observe and decision events can be sent.
    # Typical usage is to send all the pre decision observes and the decide event via a single decide_with_context call,
    # and to send post decide events, for metric evaluation, via observe calls
    choices_dict = {"color": ["red", "green", "blue"], "count": [10, 100]}  # 6 candidates via cross product
    properties_dict = {"isAuthenticated": False, "version": "mobile", "browser_height": 1740, "browser_width": 360}
    print("first session is in its pre decision phase. making a call to decide_with_context,"
          " after which first session will be in its post decision phase")
    result = first_session.decide_with_context(context_name="AmpSession",
                                               properties=properties_dict,
                                               decision_name="Decide",
                                               candidates=choices_dict)
    print("returned value is", result)
    print("returned decision is", result["decision"])
    # After the decision is made, send a few more observes if possible: this helps improve future decisions.
    print("first_session is now in its post decision phase. making an observe call")
    result = first_session.observe(name="btnClick",
                                   properties={"btnName": "SignUp"})
    print("returned value is", result)


def get_command_line_options():
    """
    Gets the appropriate command line options and returns them as a dictionary.
    """
    parser = argparse.ArgumentParser(description='This is a program that uses the SI python thin client')
    parser.add_argument('--amp_agents', help='amp_agents addresses e.g. localhost:8100,amp2-dev-clientsim-0', required=True)
    parser.add_argument('--key', help='project key e.g. d0e13d2357ffa507', required=True)
    args = vars(parser.parse_args())
    return args


def main():
    options = get_command_line_options()
    print('Command line arguments are %s' % options)
    amp_agents = options["amp_agents"].split(',')
    example_code(amp_agents=amp_agents, key=options["key"])


if __name__ == "__main__":
    main()
