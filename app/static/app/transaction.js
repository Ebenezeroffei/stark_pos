let transactionsInit = () => {
    let transactions = $('#active').parents('ul').find('li').eq(0).find('a');
    // Make the transactions section be active
    $('#active').removeAttr('id');
    transactions.attr('id','active');
}
// transactionsInit();



