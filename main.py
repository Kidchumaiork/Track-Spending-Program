import datetime
import json

transactions = []


def add_transaction(amount, category, transaction_type):
    # store date(yyyy/mm/dd) and time(hh:mm:ss)
    date = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    # create dictionary and store data to each var
    transaction = {
        "amount": amount,
        "category": category,
        "transaction_type": transaction_type,
        "date": date
    }

    # add dictionary to list outside function
    transactions.append(transaction)

    # auto save to file
    save_to_file()

    print(f"{transaction_type} {amount} บาท สำหรับ {category} ถูกบันทึกแล้ว!")

    if transaction_type == "รายรับ":
        print("ยอดรายรับรวมตอนนี้:", calculate_total_income())

    elif transaction_type == "รายจ่าย":
        print("ยอดรายจ่ายรวมตอนนี้:", calculate_total_expense())


def view_transactions():
    if not transactions:
        print("ยังไม่มีข้อมูลรายการบันทึก.")
        return

    user_input = input(
        "แสดงรายการ รายรับ หรือ รายจ่าย หรือ ทั้งหมด: ").strip().lower()

    # แปลงภาษาอังกฤษให้เป็นไทย (ทำให้ data consistency)
    if user_input == "income":
        user_input = "รายรับ"
    elif user_input == "expense":
        user_input = "รายจ่าย"
    elif user_input == "all":
        user_input = "ทั้งหมด"

    if user_input not in ["รายรับ", "รายจ่าย", "ทั้งหมด"]:
        print("ข้อมูลไม่ถูกต้องกรุณาลองใหม่ภายหลัง")
        return

    print("\nรายการที่แสดง:")
    for transaction in transactions:
        if user_input == "ทั้งหมด" or transaction["transaction_type"] == user_input:
            print(
                f"วันที่: {transaction['date']} | {transaction['transaction_type']} {transaction['amount']} บาท | ประเภท: {transaction['category']}")


def calculate_total_income():
    total_income = 0
    for transaction in transactions:
        if transaction['transaction_type'] == "รายรับ" or transaction['transaction_type'] == "income":
            total_income += transaction['amount']
    return total_income


def calculate_total_expense():
    total_expense = 0
    for transaction in transactions:
        if transaction["transaction_type"] == "รายจ่าย" or transaction['transaction_type'] == "expense":
            total_expense += transaction["amount"]
    return total_expense


def save_to_file():
    global transactions
    print("Saving...")

    with open(file='transactions.json', mode='w', encoding='utf-8') as jsonfile:
        json.dump(transactions, jsonfile, ensure_ascii=False, indent=4)
        print("The data is stored!")


def load_from_file():
    global transactions

    try:
        with open(file='transactions.json', mode='r', encoding='utf-8') as jsonfile:
            transactions = json.load(jsonfile)
            print("โหลดข้อมูลเรียบร้อยแล้ว!")

    except FileNotFoundError:
        print("ไม่พบไฟล์ข้อมูล เริ่มต้นรายการใหม่.")

    except PermissionError:
        print("คุณไม่มีสิทธิ์เข้าถึงไฟล์นี้.")


def calculate_balance():
    return calculate_total_income() - calculate_total_expense()


def view_transactions_by_date():
    if not transactions:
        print("ยังไม่มีข้อมูลรายการบันทึก.")
        return

    user_date = input(
        "กรุณาใส่วันที่ที่ต้องการดู (รูปแบบ: YYYY/MM/DD หรือ today): ").strip()

    if user_date == "today":
        user_date = datetime.datetime.now().strftime("%Y/%m/%d")

    found = False
    print(f"\nรายการวันที่ {user_date}:")
    for transaction in transactions:
        trans_date = transaction['date'].split()[0]  # แยกเอาแค่วันที่
        if trans_date == user_date:
            found = True
            print(
                f"เวลา: {transaction['date'].split()[1]} | {transaction['transaction_type']} {transaction['amount']} บาท | ประเภท: {transaction['category']}"
            )

    if not found:
        print("ไม่พบรายการในวันที่ระบุ.")


def main():
    load_from_file()

    while True:

        print("\n--- เมนูหลัก ---",
              "\n1. เพิ่มรายการรายรับ/รายจ่าย",
              "\n2. แสดงรายการทั้งหมด",
              "\n3. คำนวณรายรับรวม",
              "\n4. คำนวณรายจ่ายรวม",
              "\n5. แสดงรายการตามวันที่",
              "\n6. ดูยอดคงเหลือสุทธิ",
              "\n0. ออกจากโปรแกรม")

        try:
            user_pick = int(input("กรอกตัวเลือกที่ต้องการ(0-4): ").strip())

        except ValueError:
            print("กรุณากรอกตัวเลขเท่านั้น")
            continue

        match user_pick:
            case 1:
                amount = float(
                    input("กรอกจำนวนเงิน(ex. 250 หรือ 467.99): ").strip())
                while amount < 0:
                    print("จำนวนเงินต้องมากกว่า 0")
                    amount = float(input("กรอกจำนวนเงิน: ").strip())

                category = input("ค่าอะไร: ").strip().lower()
                transaction_type = input(
                    "กรอกประเภทรายรับ หรือ รายจ่าย: ").strip().lower()
                while transaction_type not in ["รายรับ", "income", "รายจ่าย", "expense"]:
                    print(
                        "กรุณาเลือกกรอกตามหัวข้อดังนี้\n 'รายรับ' หรือ 'income' หรือ 'รายจ่าย' หรือ 'expense'")
                    transaction_type = input(
                        "รายรับ หรือ รายจ่าย: ").strip().lower()

                # translate to Thai to make every data use either รายรับ or รายจ่าย
                if transaction_type == "income":
                    transaction_type = "รายรับ"
                elif transaction_type == "expense":
                    transaction_type = "รายจ่าย"

                add_transaction(amount, category, transaction_type)
            case 2:
                view_transactions()
            case 3:
                print("รายรับรวม:", calculate_total_income(), "บาท")
            case 4:
                print("รายจ่ายรวม:", calculate_total_expense(), "บาท")
            case 5:
                view_transactions_by_date()
            case 6:
                print("ยอดคงเหลือสุทธิ", calculate_balance(), "บาท")
            case 0:
                break


main()
