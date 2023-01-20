$(document).ready(function () {

  disable_coach();
  add_rmv_services();
  add_rmv_status_max_person();
  add_rmv_example_services()

  function disable_coach(){
    var status = document.querySelectorAll('[name$="-status"]');
    var coach = document.querySelectorAll('[name$="-supervise"]');
    for (var i = 0; i < coach.length; i++) {
      let status_ = status[i].options[status[i].options.selectedIndex].text.toLowerCase().trim(); 
      coach[i].disabled = (status_ == "intern")
    }
  }


  function add_rmv_status_max_person(){
    var count = $('#total_status').val();

    if(count == 0 || count == ""){
      $('#status-constraint-container').empty();
    }
    else if(count > 0){

      $('#status-constraint-container').empty();
      for(let i = 1; i <= count; i++){
        let val_input = $("#status_" + i.toString()).val();
        $("#status-constraint-container").append('<div id="status_max_number_'+ i.toString() +'" class="mb-3"><label for="exampleFormControlInput1" id="label_max_status_' + i.toString() + '" class="fw-bolder form-label label-white">Max Number of ' + val_input + ' in a team (Optional)</label><input value="" id="input_max_status_' + i.toString() + '" name="input_max_status[]" class="form-control" type="number" placeholder="Default input" aria-label="default input example"></div>');
      }
    }
    else{
      $('#status-constraint-container').empty();
    }
  }

  function add_rmv_services(){
    var count = $('#num_services').val();
    
    if(count == 0 || count == ""){
      $('#service-container').empty();
    }
    else if(count > 0){
      var label = '<label for="exampleFormControlInput1" class="form-label">Services</label>';

      $('#service-container').empty();
      $("#service-container").append(label);
      for(let i = 1; i <= count; i++){
        $("#service-container").append("<div class='form-group mb-2'><input type='text' name='services[]' value='' required class='services form-control' id='mb-4' placeholder='service" + i +  "'></div>");
      }
    }
    else{
      $('#service-container').empty();
    }

  }

  function add_rmv_example_services(){
    var count = $('#num_services').val();
    
    if(count == 0 || count == ""){
      $('#service-container-example').empty();
    }
    else if(count > 0){
      var label = '<label for="exampleFormControlInput1" class="form-label">Services</label>';

      $('#service-container-example').empty();
      $("#service-container-example").append(label);
      for(let i = 1; i <= count; i++){
        $("#service-container-example").append("<div class='form-group mb-2'><input type='text' name='services[]' value='service " + i.toString() + "' required class='services form-control' id='mb-4' placeholder='service" + i +  "'></div>");
      }
    }
    else{
      $('#service-container-example').empty();
    }

  }


  function add_rmv_status(){
    var count = $('#num_status').val();
    
    if(count == 0 || count == ""){
      $('#status-container').empty();
    }
    else if(count > 0){
      var label = '<label for="exampleFormControlInput1" class="form-label">Statuses</label>';

      $('#status-container').empty();
      $("#status-container").append(label);
      for(let i = 1; i <= count; i++){
        $("#status-container").append("<div class='form-group mb-2'><input type='text' name='statuses[]' value='' required class='services form-control' id='mb-4' placeholder='Any status name" + i +  "'></div>");
      }
    }
    else{
      $('#status-container').empty();
    }

  }

  var table = $('#example').DataTable({
      columnDefs: [
          {
              orderable: false,
              targets: [1, 2, 3],
              width: '20%', targets: 0
          },
      ],
      lengthMenu: [
        [-1],
        ['All'],
      ],
      responsive: true,
      autoWidth: false,
      scrollX:        true,
      scrollCollapse: true,
      fixedColumns: true
    
  });

  table.columns.adjust().draw();

  $(document).on('click', '[name$="-status"]', function(){
    disable_coach();
  });


  $(document).on('click', '#add-btn-pair', function(){
    var count_no = parseInt($('#total_service_pairing').val())+1;
    var new_input="<div class='form-group mb-2'><input type='text' name='service_pairing[]' id='service_pairing_"+count_no+"' required class='form-control' id='mb-4' placeholder='ex: 1 NOT 2'></div>";
    $('#service-pair-container').append(new_input);
    $('#total_service_pairing').val(count_no)
  });
  
  $(document).on('click', '#remove-btn-pair', function(){
    var count = $('#total_service_pairing').val();
    if(count>0){
      $('#service_pairing_'+count).remove();
      $('#total_service_pairing').val(count-1);
    }

  });

  $(document).on('change', '#num_services', function(){
    add_rmv_services();
    add_rmv_example_services();
  });


  $(document).on('click', '#add-btn-status', function(){
    var count_no = parseInt($('#total_status').val())+1;
    var new_input="<div id='status_"+count_no+"' class='form-group mb-2'><input value=\"\" type='text' id='status_" + count_no.toString() + "' name='statuses[]' required class='form-control' id='mb-4' placeholder='Any status name'></div>";

    var new_status_input='<div id="status_max_number_'+ count_no +'" class="mb-3"><label for="exampleFormControlInput1" id="label_max_status_' + count_no + '" class="fw-bolder form-label label-white">Max Number of .. in a team (Optional)</label><input value="" id="input_max_status_' + count_no + '" name="input_max_status[]" class="form-control" type="number" placeholder="Default input" aria-label="default input example"></div>'
    $('#status-container').append(new_input);
    $('#status-constraint-container').append(new_status_input);
    $('#total_status').val(count_no)
  });
  
  $(document).on('click', '#remove-btn-status', function(){
    var count = $('#total_status').val();
    if(count>0){
      $('#status_'+count).remove();
      $('#status_max_number_'+count).remove();
      $('#total_status').val(count-1);
    }

  });

  $(document).on('change', 'input[id^=status_]', function(){
    var input_num = this.id[this.id.length - 1];
    let val_input = $(this).val();

    $('#status_max_number_'+input_num).remove();
    $("#status-constraint-container").append('<div id="status_max_number_'+ input_num.toString() +'" class="mb-3"><label for="exampleFormControlInput1" id="label_max_status_' + input_num.toString() + '" class="fw-bolder form-label label-white">Max Number of ' + val_input + ' in a team (Optional)</label><input value="" id="input_max_status_' + input_num.toString() + ' name="input_max_status[]" class="form-control" type="number" placeholder="Default input" aria-label="default input example"></div>');
  
  });




  $(document).on('click', '#export-xls-btn', function() {
      var table = $('#team-table');
      if(table && table.length){
        $(table).table2excel({
          name: "Excel Document Name",
          filename: "Team Building" + new Date().toISOString().replace(/[\-\:\.]/g, "") + ".xls",
          fileext: ".xls",
          exclude_img: true,
          exclude_links: true,
          exclude_inputs: true,
        });
      }
  });

});
