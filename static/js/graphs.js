google.charts.load('current', {'packages':['corechart']});
google.charts.load('current', {'packages':['table']});
google.charts.setOnLoadCallback(graph);
google.charts.setOnLoadCallback(pie);
google.charts.setOnLoadCallback(drawTable);



function graph() {

  var data = new google.visualization.DataTable();
  data.addColumn('string', 'Lesson no');
  data.addColumn('number', 'Amount');
  fetch('/graph')
    .then(res => res.json())
    .then((out) => {
            console.log('Output: ', out["data"]);
            data.addRows(out["data"]);

            var options = {'title':'Today lessons amount', width: '100%', height: 400};

            var chart = new google.visualization.ColumnChart(document.getElementById('graph_div'));
            chart.draw(data, options);
    })
}

function pie() {

    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Teacher');
    data.addColumn('number', 'Amount');
    fetch('/pie')
      .then(res => res.json())
      .then((out) => {
              console.log('Output: ', out["data"]);
              data.addRows(out["data"]);
  
              var options = {'title':'Today teachers load', width: '100%', height: 400};
  
              var chart = new google.visualization.PieChart(document.getElementById('pie_div'));
              chart.draw(data, options);
      })
  }


function drawTable() {
    var data = new google.visualization.DataTable();
    data.addColumn('number', 'Auditory');
    data.addColumn('number', 'Capacity');
    data.addColumn('number', 'Quality');

    fetch('/table')
      .then(res => res.json())
      .then((out) => {
              console.log('Output: ', out["data"]);

        data.addRows(out["data"]);

        var table = new google.visualization.Table(document.getElementById('table_div'));

        // table.draw(data, {showRowNumber: true, width: '100%', height: '100%'});
        table.draw(data, {showRowNumber: true, width: '100%', height: 400});
    })
}
