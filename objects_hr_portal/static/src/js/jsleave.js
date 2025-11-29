odoo.define('objects_hr_portal.leavejs', function (require) {
'use strict';

const publicWidget = require('web.public.widget');

publicWidget.registry.leavejs = publicWidget.Widget.extend({
    selector: '#stackedBarChart',
    events: {
    },
    
    /**
     * @override
     */
    start: function () {

        const ctx = document.getElementById('doughnutChart').getContext('2d');
        const entry_allocated_1 = document.getElementById('entry-allocated-1').innerHTML
        const entry_taken_1 = document.getElementById('entry-taken-1').innerHTML

        const taken_percent_1 = parseFloat(entry_taken_1) / parseFloat(entry_allocated_1)
        const allocated_percent_1 = 1 - taken_percent_1
        

        new Chart(ctx, {
             type: 'doughnut',
             data: {
             labels: ["Taken", "Total"],
             datasets: [{
                label: '',
                data: [taken_percent_1,allocated_percent_1],
                backgroundColor: ['#FF6384','#cccc'],
                hoverOffset: 10
             }]
             },
             options: {
             responsive: true,
             aspectRatio: 2,
             circumference: 180,
             rotation: -90,
             plugins: {
                legend: {
                   display: false,
                   position: 'bottom'
                },
                title: {
                   display: false,
                   text: ''
                }
             }}
        });


        const ctx2 = document.getElementById('doughnutChart2').getContext('2d');
        const entry_allocated_2 = document.getElementById('entry-allocated-2').innerHTML
        const entry_taken_2 = document.getElementById('entry-taken-2').innerHTML

        const taken_percent_2 = parseFloat(entry_taken_2) / parseFloat(entry_allocated_2)
        const allocated_percent_2 = 1 - taken_percent_2

        new Chart(ctx2, {
           type: 'doughnut',
           data: {
           labels: ["Taken", "Total"],
           datasets: [{
              label: '',
              data: [taken_percent_2,allocated_percent_2],
              backgroundColor: ['#FF6384','#cccc'],
              hoverOffset: 10
           }]
           },
           options: {
           responsive: true,
           aspectRatio: 2,
           circumference: 180,
           rotation: -90,
           plugins: {
              legend: {
                 display: false,
                 position: 'bottom'
              },
              title: {
                 display: false,
                 text: ''
              }
           }
           }
        });



        // const ctx3 = document.getElementById('doughnutChart3').getContext('2d');
        // const entry_allocated_3 = document.getElementById('entry-allocated-3').innerHTML
        // const entry_taken_3 = document.getElementById('entry-taken-3').innerHTML

        // const taken_percent_3 = parseFloat(entry_taken_3) / parseFloat(entry_allocated_3)
        // const allocated_percent_3 = 1 - taken_percent_3


        // new Chart(ctx3, {
        //      type: 'doughnut',
        //      data: {
        //      labels: ["Taken", "Total"],
        //      datasets: [{
        //         label: '',
        //         data: [taken_percent_3,allocated_percent_3],
        //         backgroundColor: ['#FF6384','#cccc'],
        //         hoverOffset: 10
        //      }]
        //      },
        //      options: {
        //      responsive: true,
        //      aspectRatio: 2,
        //      circumference: 180,
        //      rotation: -90,
        //      plugins: {
        //         legend: {
        //            display: false,
        //            position: 'bottom'
        //         },
        //         title: {
        //            display: false,
        //            text: ''
        //         }
        //      }
        //      }
        //   });



          // ,
          //                  {
          //                     label: 'Home',
          //                     data: parsedEntries['home'],
          //                     hidden: true,
          //                     backgroundColor: 'orange'
          //                  }

        const entriesPerMonth = document.getElementById('entries_per_month')

        const parsedEntries = JSON.parse(entriesPerMonth.value)

        const ctx4 = document.getElementById('stackedBarChart').getContext('2d');
        new Chart(ctx4, {
                        type: 'bar',
                        data: {
                        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
                        datasets: [
                           {
                              label: 'Annual',
                              data: parsedEntries['annual'],
                              hidden: false,
                              backgroundColor: 'purple'
                           },
                           {
                              label: 'Compensatory',
                              data: parsedEntries['compensatory'],
                              hidden: false,
                              backgroundColor: 'mediumseagreen'
                           }
                        ]
                        },
                        options: {
                        plugins: {
                           legend: {
                              display: true,
                              position: 'bottom'

                           }
                        },
                        responsive: true,
                        scales: {
                           x: {
                              stacked: true,
                              title: {
                              display: true,
                              text: 'Status'
                              }
                           },
                           y: {
                              stacked: true,
                              beginAtZero: true,
                              title: {
                              display: true,
                              text: 'Number of Days'
                              }
                           }
                        }
                        }
                     });
                

        return this._super.apply(this, arguments);
    },

  });
});

