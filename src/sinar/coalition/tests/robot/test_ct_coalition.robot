# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s sinar.coalition -t test_coalition.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src sinar.coalition.testing.SINAR_COALITION_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/sinar/coalition/tests/robot/test_coalition.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a Coalition
  Given a logged-in site administrator
    and an add Coalition form
   When I type 'My Coalition' into the title field
    and I submit the form
   Then a Coalition with the title 'My Coalition' has been created

Scenario: As a site administrator I can view a Coalition
  Given a logged-in site administrator
    and a Coalition 'My Coalition'
   When I go to the Coalition view
   Then I can see the Coalition title 'My Coalition'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Coalition form
  Go To  ${PLONE_URL}/++add++Coalition

a Coalition 'My Coalition'
  Create content  type=Coalition  id=my-coalition  title=My Coalition

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Coalition view
  Go To  ${PLONE_URL}/my-coalition
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Coalition with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Coalition title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
