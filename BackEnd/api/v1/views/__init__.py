#!/usr/bin/env python3
"""create nre view app_views"""

from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")


from api.v1.views.index import *
from api.v1.views.authentication import *
from api.v1.views.user import *
from api.v1.views.store import *
from api.v1.views.category import *
from api.v1.views.product import *
from api.v1.views.cartItem import *
from api.v1.views.review import *
