/*
 * annotate.js
 * Javascript for annotating documents.
 *
 * Author:  Benjamin Bengfort <bbengfort@districtdatalabs.com>
 * Created: Mon Jul 18 22:25:07 2016 -0400
 *
 * Dependencies:
 *  - jquery
 */

(function($) {
  $(document).ready(function() {
    var annotateForm = $("#annotateForm");

    annotateForm.find("button[type=submit]").click(function(e) {
      // When the annotate button is clicked, set the val of the form.
      var target = $(e.target);

      if (!target.data('selected')) {
        // Label the annotation with the slug of the button
        var label = target.data('label-slug');
        annotateForm.find("#label").val(label);
      } else {
        // Null the label on the annotation
        annotateForm.find("#label").val("");
      }

    });

    annotateForm.submit(function(e) {
      e.preventDefault();

      // Get the action and method from the form
      var method = annotateForm.attr('method');
      var action = annotateForm.attr('action');

      // Get the data from the form
      var data = {
        'label': annotateForm.find('#label').val()
      }

      // Now make the AJAX request to the endpoint
      $.ajax({
        "url": action,
        "method": method,
        "data": JSON.stringify(data),
        "contentType": "application/json"
      }).done(function(data) {

        // On successful post of the annotation reset the buttons.
        var labelSlug = data.label
        console.log("Setting toggle to", labelSlug);

        // Go through each button and set the data as required.
        $.each(annotateForm.find("button[type=submit]"), function(idx, btn) {
          btn = $(btn);

          if (btn.data('label-slug') == labelSlug) {
            // Ok this is the newly selected button
            // Set the selected attribute to true and the class to primary.
            btn.data('selected', true);
            btn.removeClass('btn-default');
            btn.find("i").addClass('icon-white');
            btn.addClass('btn-danger');

          } else {
            // This is not the newly selected button
            btn.data('selected', false);
            btn.removeClass('btn-danger');
            btn.find("i").removeClass('icon-white');
            btn.addClass('btn-default');
          }

        });

      }).fail(function(xhr) {
        data = xhr.responseJSON;
        console.log(data)

        alert("There was a problem annotating this document!");
      });

      return false;
    });

  });
})(jQuery);
