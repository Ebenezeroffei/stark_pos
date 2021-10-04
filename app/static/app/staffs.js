const staffssInit = () => {
    let transactions = $('#active').parents('ul').find('li').eq(2).find('a');
    // Make the transactions section be active
    $('#active').removeAttr('id');
    transactions.attr('id','active');
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
                    // Close the modal
                    $('#cancel-add-staff').click();
                    // Add the staff to the frontend
                    $('#staffs > .row').append(
                        `<div class="col-6 col-md-4 col-lg-3 col-xl-2">
                            <div class="card shadow-sm p-2">
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
                                <button class="btn btn-danger" data-toggle="modal" data-target="#deleteStaffModal">Delete</button>
                            </div>
                        </div>`
                    );
                    console.log(res);
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
        let studentId = Number($(this).attr('id').split('-')[1]);
        console.log(studentId);
        $('#delete-staff').data('studentId',studentId);
    });
}

deleteStaffAttempt();


const deleteStaff = () => {
    $('#delete-staff').click(function(){
        let studentId = $(this).data('studentId');
        let csrfmiddlewaretoken = $('input[name = csrfmiddlewaretoken]').val();
        let url = $(this).data('staffDeleteUrl')
        console.log(studentId);
        $.post(
            url,
            {
                studentId,
                csrfmiddlewaretoken
            },
            function(res){
                console.log(res);
                // Close modal
                $('#cancel-staff-delete').click();
            },
            'json'
        );
    });
}
deleteStaff();