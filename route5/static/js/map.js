function updateControls(addressComponents) {
    $('#form-street1').val(addressComponents.addressLine1);
    $('#form-street2').val(addressComponents.addressLine2);
    $('#form-city').val(addressComponents.city);
    $('#form-state').val(addressComponents.stateOrProvince);
    $('#form-zip').val(addressComponents.postalCode);
    $('#form-country').val(addressComponents.country);
}

$(document).ready(function () {
    $('#us6').locationpicker({
        location: {latitude: 46.15242437752303, longitude: 2.7470703125},
        radius: 300,
        inputBinding: {
            latitudeInput: $('#us6-lat'),
            longitudeInput: $('#us6-lon'),
            radiusInput: $('#us6-radius'),
            locationNameInput: $('#us6-address')
        },
        enableAutocomplete: true,
        onchanged: function (currentLocation, radius, isMarkerDropped) {
            var addressComponents = $(this).locationpicker('map').location.addressComponents;
            updateControls(addressComponents);
        }
    });
    $('#us6-dialog').on('shown.bs.modal', function () {
        $('#us6').locationpicker('autosize');
    });
    $('#address-form').on('keyup keypress', function(e) {
      var keyCode = e.keyCode || e.which;
      if (keyCode === 13) {
        e.preventDefault();
        return false;
      }
    });

});