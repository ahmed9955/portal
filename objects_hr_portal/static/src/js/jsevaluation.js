odoo.define('objects_hr_portal.evaluationjs', function (require) {
'use strict';

const publicWidget = require('web.public.widget');
const {deleteCookie} = require('web.utils.cookies');

publicWidget.registry.Evaluationjs = publicWidget.Widget.extend({
      selector: '#evaluation',
      events: {
      },

          /**
     * @override
     */
      init: function() {
        
        document.querySelectorAll('.list-item-click').forEach(el => {

          el.addEventListener('click',(e) => {
            e.stopPropagation();
            const header = document.getElementById('header_name')
            const position = document.getElementById('header_position')
            const middleFrame = document.getElementById('middle-frame')
            const symbol = document.getElementById('middle-symbol')
            const iframe = document.getElementById("iframe_container")
            const ifr = document.getElementById("ifr")
            header.innerHTML = e.target.dataset.attr
            position.innerHTML = el.dataset.type
            symbol.innerHTML = e.target.dataset.attr.toString().substring(0, 2).toUpperCase()
            middleFrame.classList.remove('hidden')
            // iframe.classList.remove('hidden')
            // iframe.setAttribute('src',`https://surveys.objects.ws/${el.dataset.sid}?token=${el.dataset.token}`)
            if(iframe){

                // deleteCookie('PHPSESSID')
                // deleteCookie('YII_CSRF_TOKEN')

                if(ifr){
                  ifr.remove()
                }
                const innerFrame = document.createElement('iframe');
                innerFrame.id = 'ifr';
                innerFrame.sandbox = "allow-scripts allow-forms allow-same-origin"
                innerFrame.src = `https://surveys.objects.ws/${el.dataset.sid}?token=${el.dataset.token}&newtest=Y&cb=${new Date().getTime()}`;
                innerFrame.className = 'w-full h-full border-0';
                iframe.appendChild(innerFrame);
            }
          })
        })
        

        this._super.apply(this, arguments);
      },


      /**
       * @override
       */
      start: function () {

        return this._super.apply(this, arguments);
      }

  });
});

