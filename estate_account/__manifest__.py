{
    "name":"Estate Account",
    "version": "18.0.1.1.0",
    "depends":["account", "real_state", "l10n_mx_edi", "sale"],
    "application": True,
    "sequence": 1,
    "license": "LGPL-3",
    "data":[
        "views/estate_property_views.xml",
        "data/addenda.xml",
        "report/report_invoice.xml",
        "report/report_sale.xml"
        ],
    
}