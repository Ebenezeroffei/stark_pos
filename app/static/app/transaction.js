let transactionsInit = () => {
    let transactions = $('#active').parents('ul').find('li').eq(2).find('a');
    // Make the transactions section be active
    $('#active').removeAttr('id');
    transactions.attr('id','active');
}
transactionsInit();

// A function that calcultes the profit of a product
let calculateProfit = () => {
    let cost = Number($('#cost').text().substring(4,).trim());
    let revenue = Number($('#revenue').text().substring(4,).trim());
    let profit = String(revenue - cost);
    let profitLst = profit.split('.');
    profitLst.length > 1 ? profitLst[1] = profitLst[1].slice(0,2).padEnd(2,'0') : profitLst[1] = '00';
    $('#profit').html(`GH&#8373; ${profitLst.join('.')}`)
}


