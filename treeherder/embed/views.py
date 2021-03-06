from django.http import Http404
from django.views.generic.base import TemplateView

from treeherder.model.derived import JobsModel


class ResultsetStatusView(TemplateView):

    template_name = "embed/resultset_status.html"

    def get_context_data(self, **kwargs):
        assert "repository" in kwargs and "revision" in kwargs
        context = super(ResultsetStatusView, self).get_context_data(**kwargs)
        with JobsModel(kwargs['repository']) as jm:
            resultset_list = jm.get_revision_resultset_lookup(
                [kwargs['revision']])
            if not resultset_list:
                raise Http404("No resultset found for revision {0}".format(
                    kwargs['revision']))
            result_set_id = resultset_list[kwargs['revision']]['id']
            resultset_status_dict = jm.get_resultset_status(result_set_id)
            update_needed = (('pending' in resultset_status_dict) or
                             ('running' in resultset_status_dict) or
                             not resultset_status_dict)
            context['update_needed'] = update_needed
            context['resultset_status_dict'] = resultset_status_dict
            return context
