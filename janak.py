"""
hospital_mysql.py
Full Hospital Management System (Tkinter + MySQL)

Features:
- Full GUI with Patient Information fields
- Prescription text area
- Buttons: Prescription, Save, Update, Delete, Reset, Exit
- Bottom table showing records (Treeview)
- Uses MySQL to store/retrieve data

USAGE:
1) Install dependency:
   pip install mysql-connector-python
2) Edit DB_CONFIG with your MySQL credentials.
3) Run the script: python hospital_mysql.py

The script will attempt to create the database and table if not present.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime

# ---------------- Configuration -----------------
# Update these with your MySQL credentials
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "9391131352@",    # <-- set your MySQL password
    "database": "hospital"
}

TABLE_NAME = "patients"

# ----------------- Database helpers -----------------
def connect_db(with_database=True):
    cfg = DB_CONFIG.copy()
    if not with_database:
        cfg.pop("database", None)
    return mysql.connector.connect(**cfg)


def create_database_and_table():
    try:
        # connect without database to be able to create it if missing
        conn = connect_db(with_database=False)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        cur.close()
        conn.close()
    except mysql.connector.Error as err:
        messagebox.showerror("DB Error", f"Could not create database: {err}")
        return False

    # Now connect with the database and create table
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            ref_no VARCHAR(50),
            name_of_tablets VARCHAR(100),
            dose VARCHAR(50),
            no_of_tablets VARCHAR(50),
            lot VARCHAR(50),
            issue_date VARCHAR(50),
            exp_date VARCHAR(50),
            daily_dose VARCHAR(50),
            side_effect VARCHAR(100),
            further_info VARCHAR(200),
            blood_pressure VARCHAR(50),
            storage_advice VARCHAR(200),
            medication VARCHAR(200),
            patient_id VARCHAR(50),
            nhs_number VARCHAR(50),
            patient_name VARCHAR(100),
            dob VARCHAR(50),
            patient_address VARCHAR(300),
            prescription TEXT,
            created_at VARCHAR(50)
        ) ENGINE=InnoDB;
        """)
        conn.commit()
        cur.close()
        conn.close()
        return True
    except mysql.connector.Error as err:
        messagebox.showerror("DB Error", f"Could not create table: {err}")
        return False

# ----------------- App -----------------
class HospitalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Management System - MySQL")
        self.root.geometry("1540x800+0+0")
        self.root.resizable(False, False)

        # ===== Variables =====
        self.var_ref = tk.StringVar()
        self.var_name_of_tablets = tk.StringVar()
        self.var_dose = tk.StringVar()
        self.var_no_of_tablets = tk.StringVar()
        self.var_lot = tk.StringVar()
        self.var_issue_date = tk.StringVar()
        self.var_exp_date = tk.StringVar()
        self.var_daily_dose = tk.StringVar()
        self.var_side_effect = tk.StringVar()

        self.var_further_info = tk.StringVar()
        self.var_blood_pressure = tk.StringVar()
        self.var_storage_advice = tk.StringVar()
        self.var_medication = tk.StringVar()
        self.var_patient_id = tk.StringVar()
        self.var_nhs = tk.StringVar()
        self.var_patient_name = tk.StringVar()
        self.var_dob = tk.StringVar()
        self.var_patient_address = tk.StringVar()

        # ===== UI Layout =====
        title = tk.Label(self.root, text="+ SADAR HOSPITAL BHABUA BIHAR", font=("Arial", 60, "bold"), bg="#f0f0f0", fg="red")
        title.pack(side=tk.TOP, fill=tk.X)

        main_frame = tk.Frame(self.root, bd=4, relief=tk.RIDGE, padx=0, pady=0)
        main_frame.place(x=0, y=130, width=1470, height=400)

        # Left frame - Patient Information
        left_frame = tk.LabelFrame(main_frame, text="Patient Information", font=("Arial", 12, "bold"))
        left_frame.place(x=0, y=5, width=980, height=450)

        # Right frame - Prescription
        right_frame = tk.LabelFrame(main_frame, text="Prescription", font=("Arial", 12, "bold"))
        right_frame.place(x=990, y=5, width=460, height=380)


        # Left grid entries
        lbls = [
            ("Name Of Tablets:", self.var_name_of_tablets),
            ("Ref No:", self.var_ref),
            ("Dose:", self.var_dose),
            ("No Of Tablets:", self.var_no_of_tablets),
            ("Lot:", self.var_lot),
            ("Issue Date:", self.var_issue_date),
            ("Exp Date:", self.var_exp_date),
            ("Daily Dose:", self.var_daily_dose),
            ("Side Effect:", self.var_side_effect),
        ]
        r = 0
        for text, var in lbls:
            tk.Label(left_frame, text=text, font=("Arial", 12)).grid(row=r, column=0, sticky=tk.W, padx=2, pady=6)
            tk.Entry(left_frame, textvariable=var, width=35).grid(row=r, column=1, padx=2, pady=6)
            r += 1

        # Additional fields on the right side of left_frame
        addlbls = [
            ("Further Information:", self.var_further_info),
            ("Blood Pressure:", self.var_blood_pressure),
            ("Storage Advice:", self.var_storage_advice),
            ("Medication:", self.var_medication),
            ("Patient Id:", self.var_patient_id),
            ("NHS Number:", self.var_nhs),
            ("Patient Name:", self.var_patient_name),
            ("Date Of Birth:", self.var_dob),
            ("Patient Address:", self.var_patient_address),
        ]
        r = 0
        for text, var in addlbls:
            tk.Label(left_frame, text=text, font=("Arial", 10)).grid(row=r, column=2, sticky=tk.W, padx=1, pady=4)
            tk.Entry(left_frame, textvariable=var, width=30).grid(row=r, column=3, padx=0, pady=1)
            r += 1

        # Prescription text box
        self.txt_prescription = tk.Text(right_frame, width=200, height=30)
        self.txt_prescription.pack(padx=6, pady=6)

        # Buttons frame
        btn_frame = tk.Frame(self.root, bd=4, relief=tk.RIDGE)
        btn_frame.place(x=0, y=530, width=1470, height=70)

        btn_prescription = tk.Button(btn_frame, text="Prescription", width=22, command=self.generate_prescription, bg="#0b9d00", fg="black")
        btn_prescription.grid(row=0, column=0, padx=6, pady=6)

        btn_save = tk.Button(btn_frame, text="Save Data", width=22, command=self.save_data, bg="#0b9d00", fg="black")
        btn_save.grid(row=0, column=1, padx=6, pady=6)

        btn_update = tk.Button(btn_frame, text="Update", width=22, command=self.update_data, bg="#0b9d00", fg="black")
        btn_update.grid(row=0, column=2, padx=6, pady=6)

        btn_delete = tk.Button(btn_frame, text="Delete", width=22, command=self.delete_data, bg="#0b9d00", fg="black")
        btn_delete.grid(row=0, column=3, padx=6, pady=6)

        btn_reset = tk.Button(btn_frame, text="Reset", width=22, command=self.reset_fields, bg="#0b9d00", fg="black")
        btn_reset.grid(row=0, column=4, padx=6, pady=6)

        btn_exit = tk.Button(btn_frame, text="Exit", width=22, command=self.root.quit, bg="#0b9d00", fg="black")
        btn_exit.grid(row=0, column=5, padx=6, pady=6)

        # Table frame
        table_frame = tk.Frame(self.root, bd=4, relief=tk.RIDGE)
        table_frame.place(x=0, y=600, width=1470, height=190)

        scroll_x = tk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        scroll_y = tk.Scrollbar(table_frame, orient=tk.VERTICAL)
        self.patient_table = ttk.Treeview(table_frame, columns=(
            "id","ref_no","name_of_tablets","dose","no_of_tablets","lot","issue_date","exp_date",
            "daily_dose","side_effect","further_info","blood_pressure","storage_advice","medication",
            "patient_id","nhs","patient_name","dob","patient_address","prescription","created_at"
        ), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.config(command=self.patient_table.xview)
        scroll_y.config(command=self.patient_table.yview)

        # Headings
        self.patient_table.heading("id", text="ID")
        self.patient_table.heading("ref_no", text="Ref No")
        self.patient_table.heading("name_of_tablets", text="Tablet")
        self.patient_table.heading("dose", text="Dose")
        self.patient_table.heading("no_of_tablets", text="No")
        self.patient_table.heading("lot", text="Lot")
        self.patient_table.heading("issue_date", text="Issue Date")
        self.patient_table.heading("exp_date", text="Exp Date")
        self.patient_table.heading("daily_dose", text="Daily")
        self.patient_table.heading("side_effect", text="Side Effect")
        self.patient_table.heading("further_info", text="Further Info")
        self.patient_table.heading("blood_pressure", text="BP")
        self.patient_table.heading("storage_advice", text="Storage")
        self.patient_table.heading("medication", text="Medication")
        self.patient_table.heading("patient_id", text="Patient Id")
        self.patient_table.heading("nhs", text="NHS No")
        self.patient_table.heading("patient_name", text="Patient Name")
        self.patient_table.heading("dob", text="DOB")
        self.patient_table.heading("patient_address", text="Address")
        self.patient_table.heading("prescription", text="Prescription")
        self.patient_table.heading("created_at", text="Created At")

        self.patient_table["show"] = "headings"
        # set column widths
        for col in self.patient_table["columns"]:
            self.patient_table.column(col, width=140, anchor=tk.W)
        self.patient_table.column("id", width=60)
        self.patient_table.pack(fill=tk.BOTH, expand=1)
        self.patient_table.bind("<ButtonRelease-1>", self.get_cursor)

        # Initialize DB and fetch rows
        ok = create_database_and_table()
        if not ok:
            messagebox.showerror("Fatal", "Database not ready. Check credentials and restart.")
            self.root.destroy()
            return

        self.fetch_data()

    # ----------------- Functions -----------------
    def generate_prescription(self):
        # Simple prescription generator based on current fields
        prescription_text = f"""Prescription

Patient Name: {self.var_patient_name.get()}
Patient ID: {self.var_patient_id.get()}
Medicine: {self.var_name_of_tablets.get()}
Dose: {self.var_dose.get()}
No Of Tablets: {self.var_no_of_tablets.get()}
Daily Dose: {self.var_daily_dose.get()}
Side Effects: {self.var_side_effect.get()}
Further Info: {self.var_further_info.get()}

Issued On: {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
        self.txt_prescription.delete("1.0", tk.END)
        self.txt_prescription.insert(tk.END, prescription_text)

    def save_data(self):
        if self.var_ref.get() == "":
            messagebox.showerror("Error", "Reference No is required")
            return
        try:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute(f"""
                INSERT INTO {TABLE_NAME} (
                    ref_no, name_of_tablets, dose, no_of_tablets, lot, issue_date,
                    exp_date, daily_dose, side_effect, further_info, blood_pressure,
                    storage_advice, medication, patient_id, nhs_number, patient_name,
                    dob, patient_address, prescription, created_at
                ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                self.var_ref.get(),
                self.var_name_of_tablets.get(),
                self.var_dose.get(),
                self.var_no_of_tablets.get(),
                self.var_lot.get(),
                self.var_issue_date.get(),
                self.var_exp_date.get(),
                self.var_daily_dose.get(),
                self.var_side_effect.get(),
                self.var_further_info.get(),
                self.var_blood_pressure.get(),
                self.var_storage_advice.get(),
                self.var_medication.get(),
                self.var_patient_id.get(),
                self.var_nhs.get(),
                self.var_patient_name.get(),
                self.var_dob.get(),
                self.var_patient_address.get(),
                self.txt_prescription.get("1.0", tk.END).strip(),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))
            conn.commit()
            cur.close()
            conn.close()
            messagebox.showinfo("Saved", "Record saved successfully")
            self.fetch_data()
            self.reset_fields()
        except mysql.connector.Error as err:
            messagebox.showerror("DB Error", str(err))

    def fetch_data(self):
        for row in self.patient_table.get_children():
            self.patient_table.delete(row)
        try:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM {TABLE_NAME}")
            rows = cur.fetchall()
            cur.close()
            conn.close()
            for r in rows:
                self.patient_table.insert("", tk.END, values=r)
        except mysql.connector.Error as err:
            messagebox.showerror("DB Error", str(err))

    def get_cursor(self, event=""):
        cursor_row = self.patient_table.focus()
        contents = self.patient_table.item(cursor_row)
        row = contents.get("values")
        if not row:
            return
        try:
            self.selected_id = row[0]
            self.var_ref.set(row[1])
            self.var_name_of_tablets.set(row[2])
            self.var_dose.set(row[3])
            self.var_no_of_tablets.set(row[4])
            self.var_lot.set(row[5])
            self.var_issue_date.set(row[6])
            self.var_exp_date.set(row[7])
            self.var_daily_dose.set(row[8])
            self.var_side_effect.set(row[9])
            self.var_further_info.set(row[10])
            self.var_blood_pressure.set(row[11])
            self.var_storage_advice.set(row[12])
            self.var_medication.set(row[13])
            self.var_patient_id.set(row[14])
            self.var_nhs.set(row[15])
            self.var_patient_name.set(row[16])
            self.var_dob.set(row[17])
            self.var_patient_address.set(row[18])
            self.txt_prescription.delete("1.0", tk.END)
            self.txt_prescription.insert(tk.END, row[19] if row[19] else "")
        except Exception as e:
            print("Get cursor error:", e)

    def update_data(self):
        try:
            id_ = getattr(self, "selected_id", None)
        except:
            id_ = None
        if not id_:
            messagebox.showerror("Error", "Please select a record to update")
            return
        try:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute(f"""
                UPDATE {TABLE_NAME} SET
                    ref_no=%s, name_of_tablets=%s, dose=%s, no_of_tablets=%s, lot=%s, issue_date=%s,
                    exp_date=%s, daily_dose=%s, side_effect=%s, further_info=%s, blood_pressure=%s,
                    storage_advice=%s, medication=%s, patient_id=%s, nhs_number=%s, patient_name=%s,
                    dob=%s, patient_address=%s, prescription=%s
                WHERE id=%s
            """, (
                self.var_ref.get(),
                self.var_name_of_tablets.get(),
                self.var_dose.get(),
                self.var_no_of_tablets.get(),
                self.var_lot.get(),
                self.var_issue_date.get(),
                self.var_exp_date.get(),
                self.var_daily_dose.get(),
                self.var_side_effect.get(),
                self.var_further_info.get(),
                self.var_blood_pressure.get(),
                self.var_storage_advice.get(),
                self.var_medication.get(),
                self.var_patient_id.get(),
                self.var_nhs.get(),
                self.var_patient_name.get(),
                self.var_dob.get(),
                self.var_patient_address.get(),
                self.txt_prescription.get("1.0", tk.END).strip(),
                id_
            ))
            conn.commit()
            cur.close()
            conn.close()
            messagebox.showinfo("Updated", "Record updated successfully")
            self.fetch_data()
            self.reset_fields()
        except mysql.connector.Error as err:
            messagebox.showerror("DB Error", str(err))

    def delete_data(self):
        try:
            id_ = getattr(self, "selected_id", None)
        except:
            id_ = None
        if not id_:
            messagebox.showerror("Error", "Please select a record to delete")
            return
        confirm = messagebox.askyesno("Confirm", "Do you really want to delete this record?")
        if confirm:
            try:
                conn = connect_db()
                cur = conn.cursor()
                cur.execute(f"DELETE FROM {TABLE_NAME} WHERE id=%s", (id_,))
                conn.commit()
                cur.close()
                conn.close()
                messagebox.showinfo("Deleted", "Record deleted")
                self.fetch_data()
                self.reset_fields()
            except mysql.connector.Error as err:
                messagebox.showerror("DB Error", str(err))

    def reset_fields(self):
        self.var_ref.set("")
        self.var_name_of_tablets.set("")
        self.var_dose.set("")
        self.var_no_of_tablets.set("")
        self.var_lot.set("")
        self.var_issue_date.set("")
        self.var_exp_date.set("")
        self.var_daily_dose.set("")
        self.var_side_effect.set("")
        self.var_further_info.set("")
        self.var_blood_pressure.set("")
        self.var_storage_advice.set("")
        self.var_medication.set("")
        self.var_patient_id.set("")
        self.var_nhs.set("")
        self.var_patient_name.set("")
        self.var_dob.set("")
        self.var_patient_address.set("")
        self.txt_prescription.delete("1.0", tk.END)
        self.selected_id = None


# ----------------- Run -----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = HospitalApp(root)
    root.mainloop()
