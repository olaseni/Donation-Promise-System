from django.template import Context, Template

from dps_main.tests import DpsTestCase


class TemplateTagTestCase(DpsTestCase):

    @staticmethod
    def _render_template(string, context=None):
        context = context or {}
        context = Context(context)
        return Template(string).render(context)

    def test_tag(self):
        """
        GIVEN a view
        WHEN said view contains string with a custom template tag
        THEN tag executes as expected
        """
        rendered = self._render_template(
            '{% load dps_tags %}'
            '{% action_helper_ping %}'
        )
        self.assertEqual(rendered, 'pong')

    def test_context_processor(self):
        """
        GIVEN a view
        WHEN said view contains string with a custom context processor
        THEN processor executes as expected
        """
        pass
