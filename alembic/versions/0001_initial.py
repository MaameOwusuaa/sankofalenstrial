from alembic import op
import sqlalchemy as sa
revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    role = sa.Enum('user', 'admin', 'superuser', name='role')
    role.create(op.get_bind(), checkfirst=True)
    op.create_table('users', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('first_name', sa.String(80), nullable=False), sa.Column('last_name', sa.String(80), nullable=False), sa.Column('email', sa.String(255), nullable=False), sa.Column('hashed_password', sa.String(255), nullable=False), sa.Column('role', role, nullable=False), sa.Column('is_active', sa.Boolean(), nullable=False), sa.Column('created_at', sa.DateTime(), nullable=False))
    op.create_index('ix_users_email', 'users', ['email'], unique=True)
    op.create_index('ix_users_role', 'users', ['role'])
    op.create_table('heritage_sites', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('name', sa.String(180), nullable=False), sa.Column('region', sa.String(120), nullable=False), sa.Column('country', sa.String(120), nullable=False), sa.Column('category', sa.String(100), nullable=False), sa.Column('short_description', sa.String(500), nullable=False), sa.Column('story', sa.Text(), nullable=False), sa.Column('audio_url', sa.String(500)), sa.Column('image_url', sa.String(500)), sa.Column('latitude', sa.Float()), sa.Column('longitude', sa.Float()), sa.Column('qr_code', sa.String(120), nullable=False), sa.Column('is_published', sa.Boolean(), nullable=False), sa.Column('created_at', sa.DateTime(), nullable=False), sa.Column('updated_at', sa.DateTime(), nullable=False))
    for c in [('ix_heritage_sites_name', 'name'), ('ix_heritage_sites_region', 'region'), ('ix_heritage_sites_category', 'category'), ('ix_heritage_sites_qr_code', 'qr_code')]:
        op.create_index(c[0], 'heritage_sites', [c[1]], unique=c[1] == 'qr_code')
    op.create_table('passports', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), unique=True), sa.Column('points', sa.Integer(), nullable=False))
    op.create_table('badges', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False), sa.Column('name', sa.String(120), nullable=False), sa.Column('description', sa.String(400), nullable=False), sa.Column('awarded_at', sa.DateTime(), nullable=False))
    op.create_index('ix_badges_user_id', 'badges', ['user_id'])
    op.create_table('scans', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id')), sa.Column('site_id', sa.Integer(), sa.ForeignKey('heritage_sites.id'), nullable=False), sa.Column('scanned_at', sa.DateTime(), nullable=False))
    op.create_index('ix_scans_site_id', 'scans', ['site_id'])
    op.create_table('audit_logs', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id')), sa.Column('action', sa.String(160), nullable=False), sa.Column('details', sa.Text()), sa.Column('created_at', sa.DateTime(), nullable=False))

def downgrade():
    for t in ['audit_logs', 'scans', 'badges', 'passports', 'heritage_sites', 'users']:
        op.drop_table(t)
    sa.Enum('user', 'admin', 'superuser', name='role').drop(op.get_bind(), checkfirst=True)
