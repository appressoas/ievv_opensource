#########################################
`utils.testhelpers` --- Testing utilities
#########################################


.. _utils.testhelpers.testmigrations:

*************************
Testing Django migrations
*************************

.. warning:: You can not test migrations if you have a ``MIGRATION_MODULES`` setting that
    disabled migrations. So make sure you remove that setting if you have it in your
    test settings.


Guide
=====

Lets say you have the following model::

    class Node(models.Model):
        name = models.CharField(max_length=255)


You have an initial migration, and you have created a migration named ``0002_suffix_name_with_stuff``
which looks like this::

    suffix = ' STUFF'

    def add_stuff_to_all_node_names(apps, schema_editor):
        Node = apps.get_model('myapp', 'Node')
        for node in Node.objects.all():
            node.name = '{}{}'.format(node.name, suffix)
            node.save()

    def reverse_add_stuff_to_all_node_names(apps, schema_editor):
        Node = apps.get_model('myapp', 'Node')
        for node in Node.objects.all():
            if node.name.endswith(suffix):
                node.name = node.name[:-len(suffix)]
                node.save()

    class Migration(migrations.Migration):
        dependencies = [
            ('myapp', '0001_initial'),
        ]

        operations = [
            migrations.RunPython(add_stuff_to_all_node_names, reverse_code=reverse_add_stuff_to_all_node_names),
        ]

.. note:: You can not test migrations that can not be reversed, so you **MUST** write reversible migrations
    if you want to be able to test them. Think of this as a good thing - it forces you to write reversible
    migrations.

To test this, you can write a test case like this::

    from ievv_opensource.utils.testhelpers import testmigrations

    class TestSomeMigrations(testmigrations.MigrationTestCase):
        app_label = 'myapp'
        migrate_from = '0001_initial'
        migrate_to = '0002_suffix_name_with_stuff'

        def test_migrate_works(self):

            # Add some data to the model using the ``apps_before`` model state
            Node = self.apps_before.get_model('myapp', 'Node')
            node1_id = Node.objects.create(
                name='Node1'
            ).id
            node2_id = Node.objects.create(
                name='Node2'
            ).id

            # Migrate (run the 0002_suffix_name_with_stuff migration)
            self.migrate()

            # Test using the ``apps_after`` model state.
            Node = self.apps_after.get_model('myapp', 'Node')
            self.assertEqual(Node.objects.get(id=node1_id).name, 'Node1 STUFF')
            self.assertEqual(Node.objects.get(id=node2_id).name, 'Node2 STUFF')

        def test_reverse_migrate_works(self):

            # First, we migrate to get to a state where we can reverse the migration
            self.migrate()

            # Add some data to the model using the ``apps_after`` model state
            Node = self.apps_after.get_model('myapp', 'Node')
            node1_id = Node.objects.create(
                name='Node1 STUFF'
            ).id
            node2_id = Node.objects.create(
                name='Node2 STUFF'
            ).id

            # Reverse the migration
            self.reverse_migrate()

            # Test using the ``apps_before`` model state.
            Node = self.apps_before.get_model('myapp', 'Node')
            self.assertEqual(Node.objects.get(id=node1_id).name, 'Node1')
            self.assertEqual(Node.objects.get(id=node2_id).name, 'Node2')


The MigrationTestCase class
===========================

.. currentmodule:: ievv_opensource.utils.testhelpers.testmigrations
.. automodule:: ievv_opensource.utils.testhelpers.testmigrations
