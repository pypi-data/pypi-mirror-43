# -*- coding: utf-8 -*-

# Copyright (c) 2017, Camptocamp SA
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# The views and conclusions contained in the software and documentation are those
# of the authors and should not be interpreted as representing official policies,
# either expressed or implied, of the FreeBSD Project.

"""Change mapserver URL for Docker

Revision ID: d48a63b348f1
Revises: 9268a1dffac0
Create Date: 2017-08-24 08:05:46.012191
"""

from alembic import op
from c2c.template.config import config

# revision identifiers, used by Alembic.
revision = 'd48a63b348f1'
down_revision = '94db7e7e5b21'
branch_labels = None
depends_on = None


def upgrade():
    schema = config['schema']

    # Instructions
    op.execute("""
        UPDATE "{schema}".ogc_server
        SET url = 'config://mapserver'
        WHERE url = 'config://internal/mapserv'
    """.format(schema=schema))


def downgrade():
    schema = config['schema']

    # Instructions
    op.execute("""
        UPDATE "{schema}".ogc_server
        SET url = 'config://internal/mapserv'
        WHERE url = 'config://mapserver'
    """.format(schema=schema))
