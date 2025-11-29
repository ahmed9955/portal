odoo.define('objects_hr_portal.attendancejs', function (require) {
'use strict';

const publicWidget = require('web.public.widget');

publicWidget.registry.attendancejs = publicWidget.Widget.extend({
    selector: '#onelinechart',
    events: {
    },
    /**
     * @override
     */
    start: function () {





          const ctxh = document.getElementById('doughnutChart').getContext('2d');
          const entry_allocated_1 = document.getElementById('entry-allocated-1').innerHTML
          const entry_taken_1 = document.getElementById('entry-taken-1').innerHTML

          const taken_percent_1 = parseFloat(entry_taken_1) / parseFloat(entry_allocated_1)
          const allocated_percent_1 = 1 - taken_percent_1
          

          new Chart(ctxh, {
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


          // const ctx2h = document.getElementById('doughnutChart2').getContext('2d');
          // const entry_allocated_2 = document.getElementById('entry-allocated-2').innerHTML
          // const entry_taken_2 = document.getElementById('entry-taken-2').innerHTML

          // const taken_percent_2 = parseFloat(entry_taken_2) / parseFloat(entry_allocated_2)
          // const allocated_percent_2 = 1 - taken_percent_2

          // new Chart(ctx2h, {
          //   type: 'doughnut',
          //   data: {
          //   labels: ["Taken", "Total"],
          //   datasets: [{
          //       label: '',
          //       data: [taken_percent_2,allocated_percent_2],
          //       backgroundColor: ['#FF6384','#cccc'],
          //       hoverOffset: 10
          //   }]
          //   },
          //   options: {
          //   responsive: true,
          //   aspectRatio: 2,
          //   circumference: 180,
          //   rotation: -90,
          //   plugins: {
          //       legend: {
          //         display: false,
          //         position: 'bottom'
          //       },
          //       title: {
          //         display: false,
          //         text: ''
          //       }
          //   }
          //   }
          // });



          // const ctx3 = document.getElementById('doughnutChart3').getContext('2d');
          // const entry_allocated_3 = document.getElementById('entry-allocated-3').innerHTML
          // const entry_taken_3 = document.getElementById('entry-taken-3').innerHTML

          // const taken_percent_3 = parseFloat(entry_taken_3) / parseFloat(entry_allocated_3)
          // const allocated_percent_3 = 1 - taken_percent_3


          // new Chart(ctx3, {
          //     type: 'doughnut',
          //     data: {
          //     labels: ["Taken", "Total"],
          //     datasets: [{
          //         label: '',
          //         data: [taken_percent_3,allocated_percent_3],
          //         backgroundColor: ['#FF6384','#cccc'],
          //         hoverOffset: 10
          //     }]
          //     },
          //     options: {
          //     responsive: true,
          //     aspectRatio: 2,
          //     circumference: 180,
          //     rotation: -90,
          //     plugins: {
          //         legend: {
          //           display: false,
          //           position: 'bottom'
          //         },
          //         title: {
          //           display: false,
          //           text: ''
          //         }
          //     }
          //     }
          //   });











        const home_hours_float = document.getElementById('home_hours_float')
        const office_hours_float = document.getElementById('office_hours_float')
        const total = (parseFloat(home_hours_float.innerHTML) + parseFloat(office_hours_float.innerHTML))
        const home_precent = ((parseFloat(home_hours_float.innerHTML))/total) * 100
        const office_precent = 100 - home_precent
        const ctx = document.getElementById('onelinechart').getContext('2d');
        new Chart(ctx, {
          type: 'bar',
          data: {
            labels: ['Progress'],
            datasets: [
              {
                label: 'Completed',
                data: [home_precent],
                backgroundColor: 'rgb(99, 102, 241)', // Indigo color similar to image
                barPercentage: 1.0,
                categoryPercentage: 1.0,
                borderRadius: {
                  topLeft: 4,
                  bottomLeft: 4,
                },
              },
              {
                label: 'Remaining',
                data: [office_precent],
                backgroundColor: 'rgb(16, 185, 129)', // Green color similar to image
                barPercentage: 1.0,
                categoryPercentage: 1.0,
                borderRadius: {
                  topRight: 4,
                  bottomRight: 4,
                },
              }
            ]
          },
          options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              x: {
                stacked: true,
                display: false,
                grid: {
                  display: false
                }
              },
              y: {
                stacked: true,
                display: false,
                grid: {
                  display: false
                }
              }
            },
            plugins: {
              legend: {
                display: false
              },
              tooltip: {
                enabled: false
              }
            }
          }
        });


        // const worked_hours_float = document.getElementById('worked_hours_float').innerHTML
        // const required_hours_float = document.getElementById('required_hours_float').innerHTML
        // const total_hours_float = document.getElementById('total_hours_float').innerHTML
        // const worked = parseFloat(worked_hours_float)
        // const required =  parseFloat(required_hours_float)
        // const total_hours = parseFloat(total_hours_float)
        // const sum = worked + required + total_hours
        // const ctx2 = document.getElementById('onelinecharthours').getContext('2d');                        

        // new Chart(ctx2, {
        //   type: 'bar',
        //   data: {
        //     labels: ['Progress'],
        //     datasets: [
        //       {
        //         label: 'Worked',
        //         // data: [worked/sum],
        //         data: [worked/total_hours],
        //         backgroundColor: 'rgb(99, 102, 241)', // Indigo color similar to image
        //         barPercentage: 1.0,
        //         categoryPercentage: 1.0,
        //         borderRadius: {
        //           topLeft: 4,
        //           bottomLeft: 4,
        //         },
        //       },
        //       {
        //         label: 'Required',
        //         // data: [Math.abs(required/sum - worked/sum)],
        //         data: [Math.abs((required - worked)/total_hours)],
        //         backgroundColor: 'rgba(234, 179, 8, 1)', // Green color similar to image
        //         barPercentage: 1.0,
        //         categoryPercentage: 1.0,
        //         borderRadius: {
        //           topRight: 4,
        //           bottomRight: 4,
        //         },
        //       },
        //       {
        //         label: 'Total',
        //         // data: [1-(worked/sum + (Math.abs(required/sum - worked/sum)))],
        //         data: [1-((worked/total_hours) + (Math.abs((required - worked)/total_hours)) )],
        //         backgroundColor: 'rgb(209,213,219)',
        //         barPercentage: 1.0,
        //         categoryPercentage: 1.0,
        //         borderRadius: {
        //           topRight: 4,
        //           bottomRight: 4,
        //         },
        //       }
        //     ]
        //   },
        //   options: {
        //     indexAxis: 'y',
        //     responsive: true,
        //     maintainAspectRatio: false,
        //     scales: {
        //       x: {
        //         stacked: true,
        //         display: false,
        //         grid: {
        //           display: false
        //         }
        //       },
        //       y: {
        //         stacked: true,
        //         display: false,
        //         grid: {
        //           display: false
        //         }
        //       }
        //     },
        //     plugins: {
        //       legend: {
        //         display: false
        //       },
        //       tooltip: {
        //         enabled: false
        //       }
        //     }
        //   }
        // });








        const dropdownBtn = document.getElementById('dropdownBtn');
        const dropdownList = document.getElementById('dropdownList');
        const selectedLabel = document.getElementById('selectedLabel');

        const now = new Date();
        const months = [];

        for (let i = 0; i < 12; i++) {
          const date = new Date(now.getFullYear(), i, 1);
          const label = date.toLocaleString('default', { month: 'long', year: 'numeric' });
          // const value = `${date.getMonth() + 1}-${date.getFullYear()}`;
          const value = `${date.getMonth() + 1 > 9?date.getMonth() + 1: '0' + (date.getMonth() + 1).toString()}-${date.getFullYear()}`;
          months.push({ label, value });

          // Create dropdown item
          const item = document.createElement('a');
          item.className = 'dropdown-item';
          item.textContent = label;
          item.dataset.value = value;
          item.href = `/objects/hr/attendance?start=${date.getMonth()==0?date.getFullYear()-1:date.getFullYear()}-${date.getMonth()==0?12:date.getMonth()}-26&&end=${date.getFullYear()}-${date.getMonth() + 1}-25`
          

          item.addEventListener('click', () => {
            selectedLabel.textContent = label;
            dropdownList.classList.remove('show');
            console.log('Selected month value:', value); // You can use this value
          });

          dropdownList.appendChild(item);
        }

        // Auto-select current month
        const currentFilter = document.getElementById('current_filter')
        if(currentFilter){
            const currentMonthValue = currentFilter.innerHTML;
            const currentMonth = months.find(m => m.value === currentMonthValue);
            if (currentMonth) {
              selectedLabel.textContent = currentMonth.label;
            }
        }

        // Toggle dropdown
        dropdownBtn.addEventListener('click', () => {
          dropdownList.classList.toggle('show');
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', (e) => {
          if (!document.getElementById('monthDropdown').contains(e.target)) {
            dropdownList.classList.remove('show');
          }
        });
        

      }
});

});

