{
    "name": "Esign",
    "summary": "Digital Signature",
    "version": "0.1.0",
    "category": "Sales",
    "license": "",
    "author": "Simon Belete",
    "website": "https://simonbelete.com",
    "contributors": [
        "Simon Belete <simonbelete@gmail.com>"
    ],
    "depends": [
        "base_setup"
    ],
    "application": True,
    "data": [
        "template/assets.xml",

        "security/ir.model.access.csv",

        "views/esign_views.xml"
    ],
    "qweb": [
        "static/src/xml/esing.xml"
    ]
}