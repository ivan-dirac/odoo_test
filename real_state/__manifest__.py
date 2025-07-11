{
    "name":"Real State",
    "version": "18.0.1.1.0",
    "depends":["base", "purchase"],
    "application": True,
    "sequence": 1,
    "license": "LGPL-3",
    "data":[
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/res_partner_views.xml",
        "views/purchase_order_views.xml"
    ],
    "demo":[
        "demo/estate_property_demo.xml"
    ]
}