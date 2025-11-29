odoo.define('objects_hr_portal.homejs', function (require) {
'use strict';

const publicWidget = require('web.public.widget');

publicWidget.registry.Homejs = publicWidget.Widget.extend({
      selector: '#wrap',
      events: {
      },

          /**
     * @override
     */
      init: function() {
        //gray background

        const el = document.getElementById('wrap');
        if (el) {
            el.classList.add('bg-gray-50');
        }              


        const el2 = document.querySelector('.o_portal .align-items-center');

        if (el2) {
            el2.classList.remove('bg-white');        
            el2.classList.remove('border');        
            el2.classList.remove('rounded');        
            el2.classList.add('bg-gray-50');        

            el2.parentElement.parentElement.classList.remove('bg-white');        
            el2.parentElement.parentElement.classList.remove('border');        
            el2.parentElement.parentElement.classList.remove('rounded');        
            el2.parentElement.parentElement.classList.add('bg-gray-50');        
    
        }
        this._super.apply(this, arguments);
      },


      /**
       * @override
       */
      start: function () {

        const checkInButtonAction = document.querySelector('#check-in-now')
        if (checkInButtonAction){
          checkInButtonAction.addEventListener('click',(e) => {
              e.target.style.display = 'none';
          })
        }

        const homeCheckBox = document.querySelector('#home');
        const officeCheckBox = document.querySelector('#office');

        if(homeCheckBox){
            homeCheckBox.addEventListener('change',(e) => {
                if (e.target.checked) {
                  const checkInButton = document.querySelector('#check-in-now')
                  
                  if(checkInButton){
                      checkInButton.disabled = false
                  }
                }
            })
        }

        if(officeCheckBox){
          officeCheckBox.addEventListener('change',(e) => {
              if (e.target.checked) {
                  const checkInButton = document.querySelector('#check-in-now')
                  
                  if(checkInButton){
                      checkInButton.disabled = false
                  }
              }
          })
        }

        const changepassword = document.getElementById('changepass')

        if (changepassword) {
            changepassword.addEventListener('click', (e) => {

                  const changepasswordclose = document.getElementById('changepassmodel');
                  const modalPassword = document.getElementById('changepasswordform');

                  if(modalPassword){
                      modalPassword.classList.remove('hidden')
                  }

                  if(changepasswordclose){
                    changepasswordclose.addEventListener('click', () => {
                      modalPassword.classList.add('hidden')                    
                    });
                  }
            })
        }

        //modal of logout confirmation show/hide 
        const openBtn = document.getElementById('showcheckoutdialog');
        const closeBtn = document.getElementById('checkoutmodal');
        const modal = document.getElementById('checkoutconfirmation');
        if(openBtn){
          openBtn.addEventListener('click', () => {
            modal.classList.remove('hidden')
          });
        }
        if(closeBtn){
          closeBtn.addEventListener('click', () => {
            modal.classList.add('hidden')                    
          });
        }

        //set timer time
        const hours_today = document.getElementById('hours_today_val');
        let seconds = Number(hours_today?.value);
        const display = document.getElementById('timer-display');
        if (!display) return;
        function updateTimer() {
            seconds++;
            const hrs = String(Math.floor(seconds / 3600)).padStart(2, '0');
            const mins = String(Math.floor((seconds % 3600) / 60)).padStart(2, '0');
            const secs = String(parseInt(seconds % 60)).padStart(2, '0');
            display.textContent = `${hrs}:${mins}:${secs}`;
        }
        setInterval(updateTimer, 1000);

        return this._super.apply(this, arguments);
      }

  });
});

