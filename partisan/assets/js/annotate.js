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

(function() {

  // AnnotateView wraps a form with annotation buttons to provide interactive
  // functionality with the API to select or deselect annotations in the DOM.
  AnnotateView = function(selector, options) {

    this.form       = null;
    this.options    = {};
    this.buttons    = [];
    this.labelInput = null;

    // Initializes the view
    this.init = function(selector, options) {

      // Set default options
      options = options || {};
      this.options = _.defaults(options, this.options);

      // Get the required jQuery elements
      this.form = $(selector);
      this.buttons = this.form.find("button[type=submit]");
      this.labelInput = this.form.find("input[name=label]");

      // Bind the required event handlers
      var self = this;
      this.buttons.click(function(e) { return self.onClick(this, e); });
      this.form.submit(function(e) { return self.onSubmit(this, e); });

      // Return this for chaining
      return this;

    }

    // When one of the buttons is clicked
    this.onClick = function(caller, event) {
      var button = $(caller);

      if (!button.data('selected')) {
        // Label the annotation with the slug of the button
        var label = button.data('label-slug');
        this.labelInput.val(label);
      } else {
        // Null the label on the annotation (to "deselect" the annotation)
        this.labelInput.val("");
      }
    }

    // When the form is submitted
    this.onSubmit = function(caller, event) {
      var self = this;
      event.preventDefault();

      // Get the action and method from the form
      var method = this.form.attr('method');
      var action = this.form.attr('action');

      // Get the data from the form
      var data = {
        'label': this.labelInput.val()
      }

      // Now make the AJAX request to the endpoint
      $.ajax({
        "url": action,
        "method": method,
        "data": JSON.stringify(data),
        "contentType": "application/json"
      }).done(function(data) {

        // On successful post of the annotation reset the buttons.
        console.log("Setting annotation to", data.label);

        // Go through each button and set the data as required.
        $.each(self.buttons, function(idx, btn) {
          btn = $(btn);

          if (btn.data('label-slug') == data.label) {
            // Ok this is the newly selected button
            // Set the selected attribute to true and the class to primary.
            btn.data('selected', true);
            btn.removeClass('btn-default');
            btn.find("i").addClass('icon-white');
            btn.addClass('btn-' + data.label);

          } else {
            // This is not the newly selected button
            btn.data('selected', false);
            btn.removeClass('btn-democratic');
            btn.removeClass('btn-republican');
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
    }

    return this.init(selector, options)
  };

  // When the document is ready bind all annotation views
  $(document).ready(function() {
    annotators = _.map($(".annotate-form"), AnnotateView);
  });

})();
