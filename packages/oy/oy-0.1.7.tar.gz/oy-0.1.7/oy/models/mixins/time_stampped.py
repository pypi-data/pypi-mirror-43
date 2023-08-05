# -*- coding: utf-8 -*-
"""	
    oy.models.mixins.time_stampped
    ~~~~~~~~~~

    Provides a mixin classe for models that need to track time 

    :copyright: (c) 2018 by Musharraf Omer.
    :license: MIT, see LICENSE for more details.
"""

from datetime import datetime
from flask import _request_ctx_stack
from oy.boot.sqla import db
from ._sqlaevent import SQLAEvent


class TimeStampped(SQLAEvent):
    """Add created and updated fields"""

    created = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
        info=dict(label="Creation Date"),
    )
    updated = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)

    def before_update(self, mapper, connection):
        if _request_ctx_stack.top is not None:
            self.updated = datetime.utcnow()
