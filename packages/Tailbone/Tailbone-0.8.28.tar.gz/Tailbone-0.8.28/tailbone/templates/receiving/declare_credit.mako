## -*- coding: utf-8; -*-
<%inherit file="/base.mako" />

<%def name="title()">Declare Credit for Row #${row.sequence}</%def>

<%def name="context_menu_items()">
  % if master.rows_viewable and request.has_perm('{}.view'.format(permission_prefix)):
      <li>${h.link_to("View this {}".format(row_model_title), row_action_url('view', row))}</li>
  % endif
</%def>

<%def name="extra_javascript()">
  ${parent.extra_javascript()}
  <script type="text/javascript">

    function toggleFields(creditType) {
        if (creditType === undefined) {
            creditType = $('select[name="credit_type"]').val();
        }
        if (creditType == 'expired') {
            $('.field-wrapper.expiration_date').show();
        } else {
            $('.field-wrapper.expiration_date').hide();
        }
    }

    $(function() {

        toggleFields();

        $('select[name="credit_type"]').on('selectmenuchange', function(event, ui) {
            toggleFields(ui.item.value);
        });

    });
  </script>
</%def>

<div style="display: flex; justify-content: space-between;">

  <div class="form-wrapper">
    ${form.render()|n}
  </div><!-- form-wrapper -->

  <ul id="context-menu">
    ${self.context_menu_items()}
  </ul>

</div>
