const staffssInit = () => {
    let staff = $('#active').parents('ul').find('li').eq(2).find('a');
    // Make the staff section be active
    $('#active').removeAttr('id');
    staff.attr('id','active');
}
staffssInit();

const addNewStaff = () => {
    $('#add-new-staff').click(function(){
        // Start load
        $(this).html(
            `<div class='spinner-border spinner-border-sm'>
            </div>`
        ).addClass('disabled');
        // Get values
        let firstName = $('#id_first_name').val();
        let lastName = $('#id_last_name').val();
        let password = $('#id_password').val();
        let csrfmiddlewaretoken = $('input[name = csrfmiddlewaretoken]').val();
        let url = $(this).data('addNewStaffUrl');
        if(firstName && lastName && password){
            firstName = firstName[0].toUpperCase() + firstName.substring(1,);
            lastName = lastName[0].toUpperCase() + lastName.substring(1,);
            for(let i of ['#id_first_name','#id_last_name','#id_password']){
                $(i).removeClass('border-danger');
            }
            $.post(
                url,
                {
                    firstName,
                    lastName,
                    password,
                    csrfmiddlewaretoken
                },
                function(res){
                    // End load
                    $('#add-new-staff').html('Save').removeClass('disabled');
                    if(res.status == 'success'){
                        // Close the modal
                        $('#cancel-add-staff').click();
                        // First staff
                        if($('#staffs > .row').length == 0){
                            $("#staffs").empty();
                            $('#staffs').append(
                                `<div class='row'>
                                    <div class="col-6 col-md-4 col-lg-3 col-xl-2">
                                        <div class="card shadow-sm h-100">
                                            <div class='card-body'>
                                                <!-- Name -->
                                                <p class="small text-muted m-0">Name</p>
                                                <p class="lead"><strong>${firstName}</strong></p>
                                                <!-- Username -->
                                                <p class="small text-muted m-0">Username</p>
                                                <p class="lead"><strong>${res.username}</strong></p>
                                                <!-- Password -->
                                                <p class="small text-muted m-0">Password</p>
                                                <p class="lead"><strong>**********</strong></p>
                                                <!-- Options -->
                                                <button style="width: 100%;" class="btn btn-danger delete-staff-attempt" data-toggle="modal" data-target="#deleteStaffModal" id="staff-${res.staffId}">Delete</button>
                                            </div>
                                        </div>
                                    </div>
                                </div>`
                            );
                        }
                        else{
                            // Add the staff to the frontend
                            $('#staffs > .row').append(
                                `<div class="col-6 col-md-4 col-lg-3 col-xl-2">
                                    <div class="card shadow-sm h-100">
                                        <div class='card-body'>
                                            <!-- Name -->
                                            <p class="small text-muted m-0">Name</p>
                                            <p class="lead"><strong>${firstName}</strong></p>
                                            <!-- Username -->
                                            <p class="small text-muted m-0">Username</p>
                                            <p class="lead"><strong>${res.username}</strong></p>
                                            <!-- Password -->
                                            <p class="small text-muted m-0">Password</p>
                                            <p class="lead"><strong>**********</strong></p>
                                            <!-- Options -->
                                            <button style="width: 100%;" class="btn btn-danger delete-staff-attempt" data-toggle="modal" data-target="#deleteStaffModal" id="staff-${res.staffId}">Delete</button>
                                        </div>
                                    </div>
                                </div>`
                            );
                        }
                        // Turn off click event
                        $('#delete-staff-attempt').off('click');
                        deleteStaffAttempt();
                        // Clean input fields
                        $('#id_first_name, #id_last_name, #id_password').val('');
                    }
                },
                'json'
            )
        }
        else{
            for(let i of ['#id_first_name','#id_last_name','#id_password']){
                if(!$(i).val()){
                    $(i).addClass('border-danger');
                }
            }
        }
    });
}
addNewStaff();

const deleteStaffAttempt = () => {
    $('.delete-staff-attempt').click(function(){
        let staffId = Number($(this).attr('id').split('-')[1]);
        $('#delete-staff').data('staffId',staffId);
    });
}

deleteStaffAttempt();


const deleteStaff = () => {
    $('#delete-staff').click(function(){
        let staffId = $(this).data('staffId');
        let csrfmiddlewaretoken = $('input[name = csrfmiddlewaretoken]').val();
        let url = $(this).data('staffDeleteUrl')
        $.post(
            url,
            {
                staffId,
                csrfmiddlewaretoken
            },
            function(res){
                if(res.status == 'success'){
                    // Close modal
                    $('#cancel-staff-delete').click();
                    // Delete staff from frontend
                    $(`#staff-${staffId}`).parents('.col-6').hide(function(){
                        let staffsWrapper = $('#staffs > .row');
                        // Last staff
                        if(staffsWrapper.children().length - 1 == 0){
                            $(staffsWrapper).before(
                                `<div>
                                    <h3 class="text-muted text-center">You haven't added any staff.</h3>
                                    <a href="#" data-toggle="modal" data-target="#addStaffModal" style="width: 300px;margin: 20px auto;display: block;" class="btn btn-primary">New Staff</a>
                                </div>`
                            );
                            $(staffsWrapper).remove(); // Remove staffs parent
                        }
                        // Remove staff
                        $(this).remove();
                    });
                }
            },
            'json'
        );
    });
}
deleteStaff();