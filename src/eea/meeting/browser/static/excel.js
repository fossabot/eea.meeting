window.saveFile = function saveFile (selector, title, json_opts) {
    var table = $(selector).tableToJSON(json_opts);


    if(selector == '#subscribers'){
        table.forEach(function(item){
            delete item['Address'];
            delete item['Reimbursed'];
            delete item['State'];
            delete item['User Name'];
            delete item['Visa'];
            delete item['Role'];
        });
    }

    var opts = [{sheetid:'Sheet 1',header:true}];
    var res = alasql('SELECT * INTO XLSX("Export_'+title+'.xls",?) FROM ?',
                     [opts,[table]]);
}
