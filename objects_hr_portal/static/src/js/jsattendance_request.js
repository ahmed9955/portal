odoo.define('objects_hr_portal.attendancereqeustjs', function (require) {
'use strict';

const publicWidget = require('web.public.widget');

publicWidget.registry.attendancerequestjs = publicWidget.Widget.extend({
    selector: '#attendance_request_main',
    events: {
    },
    /**
     * @override
     */
    start: function () {
        
        const addAttendance = document.querySelector('#add_attendance')
        const hrRequest = document.querySelector('#hr_request')
        const checkOut = document.querySelector('#check_out')
        const checkOutLabel = document.querySelector('#check_out_label')
        const checkInLabel = document.querySelector('#check_in_label')
        const locationLabel = document.querySelector('#location_label')
        const location = document.querySelector('#location')

        if(addAttendance){
          addAttendance.addEventListener('change',(e) => {
            if (e.target.checked && checkOut && checkOutLabel && checkInLabel && locationLabel && location) {
                  checkOut.setAttribute('required','1');
                  checkOut.setAttribute('type','datetime-local');
                  checkOutLabel.classList.remove('hidden');
                  checkInLabel.innerHTML = 'Check In';
                  locationLabel.classList.remove('hidden')
                  location.setAttribute('required','1')

                  location.disabled = false;
                  location.style.display = 'block';

            }
          })
        }

        if (hrRequest){
          hrRequest.addEventListener('change',(e) => {
            if (e.target.checked && checkOut && checkOutLabel && checkInLabel && locationLabel && location) {
                  checkOut.setAttribute('required','0');
                  checkOut.setAttribute('type','hidden');
                  checkOutLabel.classList.add('hidden');
                  checkInLabel.innerHTML = 'Date';
                  locationLabel.classList.add('hidden')
                  location.setAttribute('required','0')

                  location.disabled = true;
                  location.style.display = 'none';

            }
          })

        }


      }
});

});

