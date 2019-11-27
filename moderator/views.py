"""
Collect every volunteers linked to the location and sort them in :
    - validated (the volunteer is active and can open the location)
    - required_by_mod (A request has been sent from the moderator to a user)
    - required_by_vol (A request has been sent from a user to the moderator)

:param slug: Slug for the location
"""


"""
Allow moderator to validate a request from a user, or to remove a request.

:param slug: Slug for the location
:param req_pk: Primary key for the volunteering request
:param status: Status user wish to put on the volunteering_request
"""


"""
Allow moderator to request volunteership to a user.
If user does not exist in database, moderator is sent to create a user
:param slug: Slug for the location
"""


"""
Allow a moderator to create a new user.
:param slug: Slug for the location
"""