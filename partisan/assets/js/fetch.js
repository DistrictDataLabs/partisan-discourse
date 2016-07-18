/*
 * fetch.js
 * Javascript for the web page fetch and lookup.
 *
 * Author:  Benjamin Bengfort <bbengfort@districtdatalabs.com>
 * Created: Mon Jul 18 13:01:45 2016 -0400
 *
 * Dependencies:
 *  - jquery
 */

(function($) {
  $(document).ready(function() {
    $('[data-toggle="tooltip"]').tooltip()

    var urlForm = $("#urlForm");

    // Handle urlForm submission
    urlForm.submit(function(e) {
      e.preventDefault();

      // Remove form errors if any
      removeErrors(urlForm);

      // Get form data
      var data = {
        'long_url': $('#long_url').val()
      }

      // POST the form to the endpoint
      var endpoint = urlForm.attr('action');
      var method   = urlForm.attr('method');

      // Disable the form and show spinner
      toggleURLForm();


      $.ajax({
          "url": endpoint,
          "method": method,
          "data": JSON.stringify(data),
          "contentType": "application/json"
      }).done(function(data) {
          toggleURLForm();
          if (data.detail) {
            window.location = data.detail;
          } else {
            alert("No detail was provided for some reason?");
          }

      }).fail(function(xhr) {
          data = xhr.responseJSON;
          console.log(data)

          // Set the error for particular fields.
          $.each(data, function(key, val) {
              var field = $("#"+key);
              if (field.length == 0) {
                field = $("#long_url");
              }

              field.closest('.form-group').addClass("has-error");
              field.closest('.form-group').find('.help-block').text(val);
          });

          toggleURLForm();
      });

      return false;
    });

    // Toggle Form Disabled
    function toggleURLForm() {
      $("#urlFormSpinner").toggleClass("hidden");
      $("#urlFormIcon").toggleClass("hidden");
      $('#long_url').prop('disabled', function(i, v) { return !v; });
      $('#submitUrlBtn').prop('disabled', function(i, v) { return !v; });
    }

    // Remove Errors Form
    function removeErrors(form) {
      $.each(form.find('.has-error'), function(idx, elem) {
        elem = $(elem);
        elem.removeClass("has-error");
        elem.find('.help-block').text("");
      });
    }

  });
})(jQuery);
