# def upgrade():
#     op.create_check_constraint(
#         'lossy_xor_lossless',
#         table_name='qualities',
#         schema='metadata',
#         condition='(settings_lossy_id IS NULL) <> '\
#                 '(settings_lossless_id IS NULL)'
#     )
#
#
# def downgrade():
#     op.drop_constraint('lossy_xor_lossless')
