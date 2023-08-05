# -*- coding: utf-8 -*-
"""	
    oy.models.mixins.publishable
    ~~~~~~~~~~

    Provides a mixin classe for publishable content 

    :copyright: (c) 2018 by Musharraf Omer.
    :license: MIT, see LICENSE for more details.
"""

from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from oy.boot.sqla import db
from oy.babel import lazy_gettext
from .time_stampped import TimeStampped


class Published(TimeStampped):
    """Add fields to track the publish status of the content """

    STATUS_CHOICES = [
        ("published", lazy_gettext("Published")),
        ("draft", lazy_gettext("Draft")),
    ]
    status = db.Column(
        db.Enum(*[value for value, label in STATUS_CHOICES], name="status"),
        default=STATUS_CHOICES[0][0],
        info=dict(
            choices=STATUS_CHOICES,
            label="Status",
            description="The status of this item. Draft items will not be shown for end users until they are published.",
        ),
    )
    publish_date = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
        info=dict(
            label="Publish Date",
            description="This item will not be publish until this date.",
        ),
    )
    expire_date = db.Column(
        db.DateTime,
        info=dict(
            label="Expiration Date",
            description="This item will not be publish After this date.",
        ),
    )

    @hybrid_property
    def is_published(self):
        rv = (
            self.status == self.STATUS_CHOICES[0][0]
            and self.publish_date <= datetime.now()
        )
        if self.expire_date is not None:
            rv = rv and self.expire_date >= datetime.now()
        return rv
