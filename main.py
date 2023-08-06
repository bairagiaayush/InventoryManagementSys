import json, sys
records ={}
with open("records.json") as data_file:
  records = json.load(data_file)
print(records)
print("NOTE------>>>")
print("product keys range from: 1000 - ", int(max(records.keys())))

# FOLLOWING CODE IS TO ADD A NEW PRODUCT TO OUR INVENTORY
maximum = -1
new_product = input("enter 1 if new product to be added to inventory, else enter any other character")
if new_product == "1":
    try:
        for i in records.keys():
            i = int(i)
            maximum = max(maximum,i)
        
        UID = str(maximum + 1)
        print("UID for this product is", UID)
        name = input("product name")
        value = int(input("unit price of product"))
        inventory = int(input("enter quantity of the product available in storage"))
        size = int(input("enter size of product"))
        make = input("enter make of product in CAPITALS")
        warranty = input("any warranty? enter Yes or No only")
        if warranty == "Yes" or "No":
            records[UID] = { "product" : name , "value" : value , "inventory" : inventory , "size" : size , "make" : make , "warranty" : warranty}
        else:
            print("INVALID INPUTS")
            sys.exit()
    except:
        print("INVALID INPUTS")
        sys.exit()  
        
js = json.dumps(records)

fd = open("records.json",'w')
fd.write(js)
fd.close()

# FOLLOWING CODE IS TO CHECK THE INVENTORY FOR A PARTICULAR PRODUCT
x = input("enter 1 if you want to check stock of a product. Else enter any other character")
if x =="1":
    stock = input("enter UID of product to check its inventory: ")
    if stock not in records.keys():
        print("product not existing. Please enter a vaild ID or add a new product")
        sys.exit()
    stock_value = records[stock]["inventory"]
    print("Existing stock : ", stock_value)

# FOLLOWING CODE IS TO ADD STOCK TO OUR EXISTING INVENTORY
x = input("enter 1 if you want to add stock to inventory. Else enter any other character")
if x =="1":
    prod = input("enter UID of product whose stock has to be refilled")
    if prod not in records.keys():
        print("product not existing. Please enter a vaild ID or add a new product")
        sys.exit()
    
    add = input("enter the number of stock to be added to inventory")
    try:
        add = int(add)
    except:
        print("enter numerical value")
        sys.exit()
    records[prod]["inventory"] = records[prod]["inventory"] + add
    
    js = json.dumps(records)
    
    fd = open("records.json",'w')
    fd.write(js)
    fd.close()


# CHECKING WHICH PRODUCTS HAVE WARRANTY AND ADDING THEM TO A LIST
warranty_products = []
for i in records.keys():
    if records[i]["warranty"] == "Yes":
        warranty_products.append(records[i]["product"])

# USER GIVING HOW MANY PRODUCTS ARE TO BE BOUGHT BY CUSTOMER
x = input("enter 1 if a sale is being made. Else enter any other character")
if x =="1":
    number = input("enter total number of products to be bought")
    try:
        number = int(number)
    except:
        print("enter valid number")
        sys.exit()
    if number > len(records.keys()) or number < 1:
        print("cant process these many products")
        sys.exit()
    
    # USER GIVING PRODUCT ID AND QUANTITY OF PRODUCT AS INPUT
    total_payment = 0
    sale = {}
    for i in range(number):
        product = input("enter product ID")
        if product not in records.keys():
            print("enter valid product ID")
            sys.exit()
          
        print("the accessed product is: ", records[product])
        
        quantity = input("enter quantity to be purchased")
        try:
            quantity = int(quantity)
        except:
            print("enter valid quantity")
            sys.exit()
        if int(quantity) < 1:
            print("enter valid quantity")
            sys.exit()
          
        if quantity > records[product]["inventory"]:
            print("not enough inventory")
            sys.exit()
        
        records[product]["inventory"] = records[product]["inventory"] - quantity
        unit_price = records[product]["value"]
        total = records[product]["value"]*quantity
        total_payment = total_payment + records[product]["value"]*quantity
        
        sale[records[product]["product"]] = [unit_price , quantity , total]
    
    
    # PRINTING THE SALE RECIEPT FOR THE CUSTOMER
    from datetime import date
    from datetime import datetime
    today = date.today()
    d = today.strftime("%d/%m/%Y")
    now = datetime.now()
    curr_time = now.strftime("%H:%M:%S")
    print("sale reciept is as follows")
    print("--------------------------")
    
    for i in sale.keys():
        print("product: ", i ,"||  unit price: ", sale[i][0], "||   quantity ", sale[i][1] ,"||   total ", sale[i][2])
        if i in warranty_products:
            print("warranty for this product for 1 year duration.\n")
        print("--------------------------")
    print("TOTAL AMOUNT PAYABLE : ", total_payment)
    print("DATE: ", d , "  TIME: ", curr_time)
        
    # MAKING SALES JSON FILE ASSIGNMENTS
    from datetime import date
    from datetime import datetime
    today = date.today()
    d1 = today.strftime("%d/%m/%Y")
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    profit = 0.1*total_payment
    key = str(d1) + " " + str(current_time)
    SALE =str(sale)
    PROFIT = "PROFIT: " + str(profit)
    LIST = ["unit price", "quantity purchased", "total cost"]
    sales_record = [LIST,SALE,PROFIT]
    SALES_RECORD = {}
    SALES_RECORD[key] = sales_record

    # APPENDING SALE RECIEPT IN JSON FILE
    filename = "sales.json"
    entry = SALES_RECORD
    
    with open(filename,'r') as file:
        data = json.load(file)
        
    data.append(entry)
    
    with open(filename,'w') as file:
        json.dump(data,file)

# UPDATING INVENTORY RECORDS
js = json.dumps(records)

fd = open("records.json",'w')
fd.write(js)
fd.close()
