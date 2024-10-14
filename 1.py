from flet import *
import sqlite3

# Database setup
conn = sqlite3.connect("dato.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS student (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        stdpart TEXT,
        stdname TEXT,
        stddepart TEXT,
        stdreteur TEXT,
        stdheur TEXT,
        stvihicule TEXT,
        stmarque TEXT,
        stmatricule TEXT,
        stnum TEXT,
        stfin TEXT,
        ststan TEXT
    )
""")
conn.commit()

# Function to update the displayed record count
def update_record_count(page):
    global row_count, row_count_text
    table_name = 'student'
    query = f'SELECT COUNT(*) FROM {table_name}'
    cursor.execute(query)
    result = cursor.fetchone()
    row_count = result[0]
    row_count_text.value = f"Nombre de rotors: {row_count}"
    page.update()

# Function to add data to the database
def add_record(e, page):
    partner = tname.value
    name = tmail.value
    departure_date = tphone.value
    return_date = taddress.value
    return_time = heur.value
    vehicle = vihicule.value
    brand = marque.value
    license_plate = matricule.value
    num_cb = num.value
    finv = fin.value
    stan_value = stan.value

    try:
        cursor.execute("""
            INSERT INTO student (stdpart, stdname, stddepart, stdreteur, stdheur, stvihicule, stmarque, stmatricule, stnum, stfin, ststan)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (partner, name, departure_date, return_date, return_time, vehicle, brand, license_plate, num_cb, finv, stan_value))
        conn.commit()
        update_record_count(page)
        clear_fields()
    except Exception as e:
        print(f"An error occurred while adding a record: {e}")

def edit_record(e, page, record_id):
    cursor.execute("SELECT * FROM student WHERE id=?", (record_id,))
    record = cursor.fetchone()
    tname.value = record[1]
    tmail.value = record[2]
    tphone.value = record[3]
    taddress.value = record[4]
    heur.value = record[5]
    vihicule.value = record[6]
    marque.value = record[7]
    matricule.value = record[8]
    num.value = record[9]
    fin.value = record[10]
    stan.value = record[11]
    add_button.text = "METTRE À JOUR"
    add_button.on_click = lambda e: update_record(e, page, record_id)
    page.update()

def update_record(e, page, record_id):
    partner = tname.value
    name = tmail.value
    departure_date = tphone.value
    return_date = taddress.value
    return_time = heur.value
    vehicle = vihicule.value
    brand = marque.value
    license_plate = matricule.value
    num_cb = num.value
    finv = fin.value
    stan_value = stan.value

    try:
        cursor.execute("""
            UPDATE student
            SET stdpart=?, stdname=?, stddepart=?, stdreteur=?, stdheur=?, stvihicule=?, stmarque=?, stmatricule=?, stnum=?, stfin=?, ststan=?
            WHERE id=?
        """, (partner, name, departure_date, return_date, return_time, vehicle, brand, license_plate, num_cb, finv, stan_value, record_id))
        conn.commit()
        update_record_count(page)
        clear_fields()
        add_button.text = "AJOUTER UN RETOUR"
        add_button.on_click = lambda e: add_record(e, page)
    except Exception as e:
        print(f"An error occurred while updating a record: {e}")

def delete_record(e, page, record_id):
    try:
        cursor.execute("DELETE FROM student WHERE id=?", (record_id,))
        conn.commit()
        update_record_count(page)
        show_records(e, page)
    except Exception as e:
        print(f"An error occurred while deleting a record: {e}")

def show_records(e, page):
    records = cursor.execute("SELECT * FROM student").fetchall()
    record_list.controls.clear()
    for record in records:
        record_card = Card(
            content=Column([
                Row([Icon(icons.PEOPLE, size=24), Text(f"Partenaire: {record[1]}", weight='bold', size=16)], alignment='start'),
                Row([Icon(icons.PERSON, size=24), Text(f"Nom Prénom: {record[2]}")], alignment='start'),
                Row([Icon(icons.DATE_RANGE, size=24), Text(f"Date Départ: {record[3]}")], alignment='start'),
                Row([Icon(icons.DATE_RANGE, size=24), Text(f"Date Retour: {record[4]}")], alignment='start'),
                Row([Icon(icons.TIME_TO_LEAVE, size=24), Text(f"Heur Retour: {record[5]}")], alignment='start'),
                Row([Icon(icons.DRIVE_ETA, size=24), Text(f"Vihicule: {record[6]}")], alignment='start'),
                Row([Icon(icons.BRANDING_WATERMARK, size=24), Text(f"Marque: {record[7]}")], alignment='start'),
                Row([Icon(icons.LOCATION_ON, size=24), Text(f"Matricule: {record[8]}")], alignment='start'),
                Row([Icon(icons.KEYBOARD, size=24), Text(f"N°CB: {record[9]}")], alignment='start'),
                Row([Icon(icons.MONEY, size=24), Text(f"FinV: {record[10]}")], alignment='start'),
                Row([Icon(icons.STORAGE, size=24), Text(f"STAN: {record[11]}")], alignment='start'),
                Row([
                    ElevatedButton("Modifier", on_click=lambda e, id=record[0]: edit_record(e, page, id)),
                    ElevatedButton("Supprimer", on_click=lambda e, id=record[0]: delete_record(e, page, id))
                ], alignment='center')
            ], alignment='start'),
            elevation=2,
            width=320,
            margin=5
        )
        record_list.controls.append(record_card)
    page.update()

def clear_fields():
    tname.value = ""
    tmail.value = ""
    tphone.value = ""
    taddress.value = ""
    heur.value = ""
    vihicule.value = ""
    marque.value = ""
    matricule.value = ""
    num.value = ""
    fin.value = ""
    stan.value = ""

def main(page: Page):
    global tname, tmail, tphone, taddress, heur, vihicule, marque, matricule, num, fin, stan, row_count_text, record_list, add_button

    page.title = 'SOURIZA CAR (FOX CAR)'
    page.scroll = 'auto'
    page.window.top = 1 
    page.window.left = 960
    page.window.width = 390
    page.window.height = 740
    page.bgcolor = 'white'
    page.theme_mode = ThemeMode.LIGHT

    global row_count
    row_count = 0
    row_count_text = Text(f"Nombre de rotors: {row_count}", size=20, font_family="Bernard MT Condensed", color='blue')

    # Menu bar with PopupMenuButton
    menu_bar = Row(
        [
            PopupMenuButton(
                icon=icons.MENU,
                items=[
                    PopupMenuItem(text="Accueil", on_click=lambda e: print("Accueil clicked")),
                    PopupMenuItem(text="Ajouter un Retour", on_click=lambda e: add_record(e, page)),
                    PopupMenuItem(text="Afficher les Retours", on_click=lambda e: show_records(e, page)),
                    PopupMenuItem(text="Quitter", on_click=lambda e: page.window_close())
                ]
            )
        ],
        alignment=MainAxisAlignment.START
    )

    add_button = ElevatedButton(
        "AJOUTER UN RETOUR",
        width=170,
        style=ButtonStyle(bgcolor='blue', color='white', padding=15),
        on_click=lambda e: add_record(e, page)
    )
    show_button = ElevatedButton(
        "AFFICHER LES RETOUR",
        width=170,
        style=ButtonStyle(bgcolor='blue', color='white', padding=15),
        on_click=lambda e: show_records(e, page)
    )

    tname = TextField(label='Partenaire', icon=icons.PEOPLE, height=38)
    tmail = TextField(label='Nom Prénom', icon=icons.PERSON, height=38)
    tphone = TextField(label='Date Départ', icon=icons.DATE_RANGE, height=38)
    taddress = TextField(label='Date Retour', icon=icons.DATE_RANGE, height=38)
    heur = TextField(label='Heur Retour', icon=icons.TIME_TO_LEAVE, height=38)
    vihicule = TextField(label='Vihicule', icon=icons.DRIVE_ETA, height=38)
    marque = TextField(label='Marque', icon=icons.BRANDING_WATERMARK, height=38)
    matricule = TextField(label='Matricule', icon=icons.LOCATION_ON, height=38)
    num = TextField(label='N°CB', icon=icons.KEYBOARD, height=38)
    fin = TextField(label='FinV', icon=icons.MONEY, height=38)
    stan = TextField(label='STAN', icon=icons.STORAGE, height=38)

    record_list = Column()
    
    page.add(
        Column([
            menu_bar,  # Add the menu bar here
            row_count_text,
            tname,
            tmail,
            tphone,
            taddress,
            heur,
            vihicule,
            marque,
            matricule,
            num,
            fin,
            stan,
            Row([add_button, show_button], alignment='center'),
            record_list,
        ], horizontal_alignment='center')
    )

    update_record_count(page)

app(target=main)
