e-nabavki
=========

Machine friendly e-nabavki.gov.mk. Free the data.

## Usage

`casperjs e-nabavki.gov.mk.js --page=3`

```json
{
    "links": [
        "https://e-nabavki.gov.mk/PublicAccess/Dossie/dosieNotificationForACPP.aspx?Id=c8d9ff87-d7a1-4cd2-95bf-3a56107439ae&Level=3",
        "https://e-nabavki.gov.mk/PublicAccess/Dossie/dosieNotificationForACPP.aspx?Id=18d0035d-158c-4df9-ad04-3e770c74a083&Level=3",
        "https://e-nabavki.gov.mk/PublicAccess/Dossie/dosieNotificationForACPP.aspx?Id=cb2e22be-a1e6-437d-aaf1-8367a38cd010&Level=3",
        "https://e-nabavki.gov.mk/PublicAccess/Dossie/dosieNotificationForACPP.aspx?Id=0298e840-f1b2-4dc3-b2df-5cec23dcb76a&Level=3",
        "https://e-nabavki.gov.mk/PublicAccess/Dossie/dosieNotificationForACPP.aspx?Id=6b1a4fa1-e58c-4e63-b99b-f10c14604463&Level=3",
        "https://e-nabavki.gov.mk/PublicAccess/Dossie/dosieNotificationForACPP.aspx?Id=bad812ed-e544-4edf-a9e4-b13ae65e31a2&Level=3",
        "https://e-nabavki.gov.mk/PublicAccess/Dossie/dosieNotificationForACPP.aspx?Id=e48ed97d-2357-4f8e-be41-f9a14a209e92&Level=3",
        "https://e-nabavki.gov.mk/PublicAccess/Dossie/dosieNotificationForACPP.aspx?Id=12083ff9-211a-496e-ab9f-4c2c6274b2e5&Level=3",
        "https://e-nabavki.gov.mk/PublicAccess/Dossie/dosieNotificationForACPP.aspx?Id=56dc2f87-290b-4aa9-b4f1-787c3c9faa39&Level=3",
        "https://e-nabavki.gov.mk/PublicAccess/Dossie/dosieNotificationForACPP.aspx?Id=5935ce16-dab9-42de-be6c-22fc9557b80a&Level=3"
    ],
    "page": 3,
    "length": 10
}

```

To get the actual data from a link, like one of the links above, do:

`python parse.py "https://e-nabavki.gov.mk/PublicAccess/Dossie/dosieNotificationForACPP.aspx?Id=5935ce16-dab9-42de-be6c-22fc9557b80a&Level=3"`

```json
{
    "Вид на постапка": "Постапка со преговарање без претходно објавување на оглас", 
    "Назив на договорниот орган": "Ј.П.Градски Паркинг – Скопје"
}

```
