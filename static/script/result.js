$(document).ready(function () {

  function exportReportToExcel() {
    let tables = document.getElementById("team-table-all"); // you can use document.getElementById('tableId') as well by providing id to the table tag
    var todaydate = new Date();  //pass val varible in Date(val)
    var dd = todaydate .getDate();
    var mm = todaydate .getMonth()+1; //January is 0!
    var yyyy = todaydate .getFullYear();
    if(dd<10){  dd='0'+dd } 
    if(mm<10){  mm='0'+mm } 
    var datestring = dd+'-'+mm+'-'+yyyy;
    TableToExcel.convert(tables, { // html code may contain multiple tables so here we are refering to 1st table tag
      name: `export_team_table_` + datestring + `.xlsx`, // fileName you could use any name
      sheet: {
        name: 'Sheet 1' // sheetName
      }
    });
  }

  function updateTeamResult() {
    s_idx = $('#solution-select').val();
    num_of_soln = $('#sum-soln').val();
    for (let i = 0; i < parseInt(num_of_soln); i++) {
      if (i == s_idx) {
        $('#container-result-' + i.toString()).show();
      }
      else {
        $('#container-result-' + i.toString()).hide();
      }
    }
  }


  function exportCSVFile() {
    var todaydate = new Date();  //pass val varible in Date(val)
    var dd = todaydate .getDate();
    var mm = todaydate .getMonth()+1; //January is 0!
    var yyyy = todaydate .getFullYear();
    if(dd<10){  dd='0'+dd } 
    if(mm<10){  mm='0'+mm } 
    var datestring = dd+'-'+mm+'-'+yyyy;

    $("#team-table-all").tableHTMLExport({
      // csv, txt, json, pdf
      type: 'csv',

      // default file name
      filename: `export_team_table_` + datestring + `.csv`,

      // for csv
      separator: ',',
      newline: '\r\n',
      trimContent: true,
      quoteFields: true,

      // CSS selector(s)
      ignoreColumns: '',
      ignoreRows: '',

      // your html table has html content?
      htmlContent: false,

      // debug
      consoleLog: false,
    })


  }


  $(document).on('click', '#export-xls-btn', exportReportToExcel);
  $(document).on('click', '#export-csv-btn', exportCSVFile);
  $(document).on('change', '#solution-select', updateTeamResult);


  updateTeamResult();
});


// function exportPDFFile() {
//   var todaydate = new Date();  //pass val varible in Date(val)
//   var dd = todaydate .getDate();
//   var mm = todaydate .getMonth()+1; //January is 0!
//   var yyyy = todaydate .getFullYear();
//   if(dd<10){  dd='0'+dd } 
//   if(mm<10){  mm='0'+mm } 
//   var datestring = dd+'-'+mm+'-'+yyyy;

//   $("#team-table-all").tableHTMLExport({
//     type: 'pdf',
//     orientation: 'p',
//     filename: `export_team_table_` + datestring + `.pdf`,

//   })
// }
