function onOpen(e){
    var menu = SpreadsheetApp.getUi().createMenu('COVID DATA')
    menu.addItem('Home', 'covidHome')
        .addSeparator()
        .addSubMenu(SpreadsheetApp.getUi().createMenu('State or County')
                    .additem("State", "state")
                    .additem("County", "county")
                    .addSeparator()
                    .addToUI()
}

function fetchStateData(state, intervention) {
    var baseUrl = "https://data.covidactnow.org/latest";
    var url = baseUrl + "/us/states/CA.WEAK_INTERVENTION.json";

    var response = UrlFetchApp.fetch(url, {'muteHttpExceptions': true});

    var json = response.getContentText();
    var data = JSON.parse(json);

    Logger.log(data)

}

