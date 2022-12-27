$(document).ready(function () {

  disable_coach();
  add_rmv_services();


  function disable_coach(){
    var status = document.querySelectorAll('[name$="-status"]');
    var coach = document.querySelectorAll('[name$="-supervise"]');
    for (var i = 0; i < coach.length; i++) {
      coach[i].disabled = (status[i].options.selectedIndex == 0)
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
        $("#service-container").append("<div class='form-group mb-2'><input type='text' name='services[]' value='service" + i +  "' required class='services form-control' id='mb-4' placeholder='service" + i +  "'></div>");
      }
    }
    else{
      $('#service-container').empty();
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
          },
      ],
      lengthMenu: [
        [-1],
        ['All'],
      ],
    
  });

  $(document).on('click', '[name$="-status"]', function(){
    disable_coach();
  });


  $(document).on('click', '#add-btn-pair', function(){
    var count_no = parseInt($('#total_service_pairing').val())+1;
    var new_input="<div class='form-group mb-2'><input type='text' name='service_pairing[]' id='service_pairing_"+count_no+"' required class='form-control' id='mb-4' placeholder='ex: A NOT B'></div>";
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
  });


  $(document).on('click', '#add-btn-status', function(){
    var count_no = parseInt($('#total_status').val())+1;
    var new_input="<div class='form-group mb-2'><input type='text' name='statuses[]' id='status_"+count_no+"' required class='form-control' id='mb-4' placeholder='Any status name'></div>";
    $('#status-container').append(new_input);
    $('#total_status').val(count_no)
  });
  
  $(document).on('click', '#remove-btn-status', function(){
    var count = $('#total_status').val();
    if(count>0){
      $('#status_'+count).remove();
      $('#total_status').val(count-1);
    }

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
