import mysql.connector
from datetime import datetime
import customtkinter
import os
from PIL import Image, ImageTk
import pyqrcode


from confidential import upi_id, name
# Connectting to the database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
)

mycursor = mydb.cursor()
mycursor.execute('CREATE DATABASE IF NOT EXISTS wholesale;')
mycursor.execute('USE wholesale;')
# Create the inventory table if it doesn't exist
mycursor.execute("""
CREATE TABLE IF NOT EXISTS inventory (
    orderid INT AUTO_INCREMENT PRIMARY KEY,
    item VARCHAR(50),
    qty INT,
    rate DECIMAL(10,2),
    price DECIMAL(10,2),
    date DATE
)
""")

class App(customtkinter.CTk):
    #main function
    def __init__(self):
        super().__init__()

        self.title("Wholesale Billing System :)")
        self.geometry("700x410")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(26, 26))
        self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")), size=(300, 100))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        self.chat_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))
        self.add_user_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))
        self.show_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path,"light.png")), 
                                                 dark_image=Image.open(os.path.join(image_path, "dark.png")), size=(300,200))
        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  Image Example", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Incoming",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.chat_image, anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Outgoing",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.add_user_image, anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        self.frame_4_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Inventory",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.add_user_image, anchor="w", command=self.frame_4_button_event)
        self.frame_4_button.grid(row=4, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.home_frame_large_image_label = customtkinter.CTkLabel(self.home_frame, text="", image=self.show_image)
        self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        self.home_frame_button_1 = customtkinter.CTkButton(self.home_frame, text="INCOMING",font= ('Arial Black',20), command=self.frame_2_button_event)
        self.home_frame_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.home_frame_button_2 = customtkinter.CTkButton(self.home_frame, text="OUTCOMING", font= ('Arial Black',20), command=self.frame_3_button_event)
        self.home_frame_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.home_frame_button_3 = customtkinter.CTkButton(self.home_frame, text="INVENTORY", font= ('Arial Black',20),image=self.add_user_image, command=self.frame_4_button_event)
        self.home_frame_button_3.grid(row=3, column=0, padx=20, pady=10)

        # create second frame

        
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.incoming_label = customtkinter.CTkLabel(self.second_frame, text="Incoming", font=('Arial Black', 45))
        self.incoming_label.grid(row=0, column=0, padx=20, pady=10)  # Display header in second_frame
        self.item = customtkinter.CTkEntry(self.second_frame, placeholder_text='Enter item name: ', fg_color= 'transparent', height= 40, width=250)
        self.item.grid(row=1, column=0, padx=60, pady=10)

        self.qty = customtkinter.CTkEntry(self.second_frame, placeholder_text='Enter Quantity: ', fg_color= 'transparent', height= 40, width=250)
        self.qty.grid(row=2, column=0, padx=60, pady=10)

        self.rate = customtkinter.CTkEntry(self.second_frame, placeholder_text='Enter Rate: ', fg_color= 'transparent', height= 40, width=250)
        self.rate.grid(row=3, column=0, padx=60, pady=10)


        self.second_frame_button_1 = customtkinter.CTkButton(self.second_frame, text="ADD", command= self.add_incoming)
        self.second_frame_button_1.grid(row=4, column=0, padx=20, pady=10)

        # create third frame
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.outgoing_label = customtkinter.CTkLabel(self.third_frame, text="Outgoing", font=('Arial Black', 45))
        
        self.outgoing_label.grid(row=0, column=0, padx=20, pady=10)  # Display header in third_frame
        self.orderid = customtkinter.CTkEntry(self.third_frame, placeholder_text='Enter Orderid: ', fg_color= 'transparent', height= 40, width=250)
        self.orderid.grid(row=1, column=0, padx=60, pady=10)

        self.qty2 = customtkinter.CTkEntry(self.third_frame, placeholder_text='Enter Quantity: ', fg_color= 'transparent', height= 40, width=250)
        self.qty2.grid(row=2, column=0, padx=60, pady=10)

        self.third_frame_button_1 = customtkinter.CTkButton(self.third_frame, text="REMOVE", command= self.remove_outgoing)
        self.third_frame_button_1.grid(row=3, column=0, padx=20, pady=10)
        # create fourth frame
        self.fourth_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.inventory_label = customtkinter.CTkLabel(self.fourth_frame, text="Inventory", font=('Arial Black', 45))
        self.inventory_label.grid(row=0, column=0, padx=20, pady=10)  # Display header in fourth_frame

        self.fourth_frame_button_1 = customtkinter.CTkButton(self.fourth_frame, text="SHOW TIME", command= self.check_inventory)
        self.fourth_frame_button_1.grid(row=1, column=0, padx=20, pady=10)

        # select default frame
        self.select_frame_by_name("home")
    # Function to add incoming items
    def add_incoming(self):
        
        item = self.item.get()
        qty = self.qty.get()
        rate = self.rate.get()
        price = int(qty) * int(rate)
        date = datetime.now().strftime("%Y-%m-%d")
        sql = "INSERT INTO inventory (item, qty, rate, price, date) VALUES (%s, %s, %s, %s, %s)"
        val = (item, qty, rate, price, date)
        mycursor.execute(sql, val)
        mydb.commit()
        print("Incoming item added successfully!")
        success_label = customtkinter.CTkLabel(self.second_frame, text="Incoming item added successfully!")
        success_label.grid(row=6, column=0, padx=20, pady=20)  # Use grid for placement
         # Clear entry fields
        self.item.delete(0, 'end')
        self.qty.delete(0, 'end')
        self.rate.delete(0, 'end')

        def remove_success_msg():
            success_label.destroy()  # Remove the label after 3.5 seconds

        self.after(3500, remove_success_msg)  # Schedule the removal after 3.5 seconds

    #Function to remove outgoing items
    def remove_outgoing(self):
        orderid = self.orderid.get()  # Get orderid from entry widget
        qty2 = int(self.qty2.get())  # Get quantity from entry widget

        mycursor.execute("SELECT * FROM inventory WHERE orderid = %s", (orderid,))
        result = mycursor.fetchone()
        
        if result:
            current_qty = result[2]
            if qty2 > current_qty:
                error_label = customtkinter.CTkLabel(self.third_frame, text="Quantity exceeds available stock!", fg_color="red")
                error_label.grid(row=4, column=0, padx=20, pady=10)  # Display error message in third_frame
                return

            new_qty = current_qty - qty2
            rate = result[3]
            amount = rate * qty2

            
            # Generate UPI payment string and QR code
            payload = f"upi://pay?pa={upi_id}&pn={name}&am={amount}"
            qr_code = pyqrcode.create(payload)
            qr_code.png("payment.png", scale=3)

            # Load the QR code image
            qr_image = ImageTk.PhotoImage(Image.open("payment.png"))

            # Create a label to display the image on the third frame
            qr_label = customtkinter.CTkLabel(self.third_frame, image=qr_image)
            qr_label.grid(row=3, padx=20, pady=10)
            if new_qty == 0:
                mycursor.execute("DELETE FROM inventory WHERE orderid = %s", (orderid,))
            else:
                mycursor.execute("UPDATE inventory SET qty = %s WHERE orderid = %s", (new_qty, orderid))
            mydb.commit()
            
            success_label = customtkinter.CTkLabel(self.third_frame, text="Scan the QR for Payment!!!")
            success_label.grid(row=4, column=0, padx=20, pady=10)  # Display success message in third_frame

            def remove_success_msg():

                def removed():
                    success_label.destroy()
                    qr_label.destroy()
                    continued.destroy()
                    self.third_frame_button_1.grid()

                success_label.destroy()
                continued = customtkinter.CTkButton(self.third_frame, text="CONTINUE", command= removed)
                continued.grid(row=4, column=0, padx=20, pady=10)  # Remove the label after 7 seconds

            self.after(7000, remove_success_msg)

            # Clear entry fields
            self.orderid.delete(0, 'end')
            self.qty.delete(0, 'end')
        else:
            error_label = customtkinter.CTkLabel(self.third_frame, text="Item not found in inventory!", fg_color="red")
            error_label.grid(row=3, column=0, padx=20, pady=10)  # Display error message in third_frame
    
    #Function to check inventory
    def check_inventory(self):
        mycursor.execute("SELECT orderid, item, qty FROM inventory")
        result = mycursor.fetchall()  
        if result:
            item_label1 = customtkinter.CTkLabel(self.fourth_frame, text=f"  ORDER\t\t  ITEM\t\t  QUANTUTY", font=('Arial Black', 15))
            item_label1.grid(row=1, column=0, padx=20, pady=5)
            # item_label2 = customtkinter.CTkLabel(self.fourth_frame, text=f"----------------------------------", font=('Arial Narrow', 20))
            # item_label2.grid(row=2, column=0, padx=20, pady=0)
            row_index = 3  # Start placing items from row 3

            item_labels= []
            for row in result:
                
                item_label = customtkinter.CTkLabel(self.fourth_frame, text=f"{row[0]}\t\t{row[1]}\t\t{row[2]}", font=('Arial Narrow', 20),anchor='w', justify= 'left')
                item_label.grid(row=row_index, column=0, padx=20, pady=5)  # Display each item in fourth_frame
                item_labels.append(item_label)
                row_index += 1  # Increment row index for subsequent items
                
            def refresh():
                for label in item_labels:
                    label.destroy() 
                item_label1.destroy()
                # item_label2.destroy()
                refresh.destroy()
                # only destroying last item_label i want to destrol all item_label when refresh button clicked

            refresh = customtkinter.CTkButton(self.fourth_frame, text="REFRESH", command= refresh)
            refresh.grid(row=row_index+1, column=0, padx=20, pady=10) 
        else:
            no_items_label = customtkinter.CTkLabel(self.fourth_frame, text="No items in inventory.", fg_color="gray")
            no_items_label.grid(row=0, column=0, padx=20, pady=10)  # Display message in fourth_frame

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")
        self.frame_4_button.configure(fg_color=("gray75", "gray25") if name == "frame_4" else "transparent")
        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()
        if name == "frame_4":
            self.fourth_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.fourth_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

    def frame_4_button_event(self):
        self.select_frame_by_name("frame_4")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

if __name__ == "__main__":
    app = App()
    app.mainloop()