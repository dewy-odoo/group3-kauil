{
    "name": "ge9-3363106",
    
    "summary": "Rebate for new Customers",
    
    "description": """
    Create a data file for a price list that has a value of $2,500usd
    Create a computed Boolean field called "is_new_customer" that will be true if the res.partner does not have any other sale order lines contain a motorcycle product.
    Add a button on sales orders that are still in the quotation stage is is_new_customer is true
    Create a function that applies the product.pricelist to the sale order and call that function from the button you added
    """,
    
    "version": "0.1",
    
    "category": "Kauil/Registry",
    
    "license": "OPL-1",
    
    "depends": ["sale", "motorcycle_registry"],
    
    "data": [
        'views/sale_order_inherit.xml',
        "data/discount_data.xml"
    ],
    
    "demo": [

    ],
    
    "author": "kauil-motors",
    
    "website": "www.odoo.com",
    
    "application": False,
    
}