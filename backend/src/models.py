from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(server_default=sa.func.now())
    updated_at: Mapped[datetime] = mapped_column(
        default=sa.func.now(),
        onupdate=sa.func.now(),
        server_default=sa.func.now(),
    )
