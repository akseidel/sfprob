# akseidel 11/27/2023
import tkinter as tk
from typing import NoReturn
from selenium import webdriver
from selenium.webdriver.common.by import By

# globals
query_last_name = 'Montoya Emaho'
query_first_name = 'Emaho'
firstdistrict_court_nm_caselookup_url = "https://caselookup.nmcourts.gov/caselookup/"
#santa_fe_county_url = "https://clerktrackweb.santafecountynm.gov/ctweb/login.aspx"
#santa_fe_county_probate_url = "https://clerktrackweb.santafecountynm.gov/ctweb/prosearch.aspx"


def login_the_session(driver_session):
    l_driver_session = driver_session
    l_driver_session.get(firstdistrict_court_nm_caselookup_url)
    l_driver_session.implicitly_wait(0.5)
    print(f'Navigated to {l_driver_session.current_url}')
    # Setting the object to fill in or press
    accept_button = l_driver_session.find_element(by=By.ID, value="Submit")
    # Filling in and pressing login
    #print('Now attempting to accept.')
    accept_button.click()
    print(f'Now at the webpage called: {l_driver_session.title}')
    # successfully navigated to post login webpage
    # successfully entered URL_2


def probate_query_field_entry_and_execute(lastname, firstname, driver_session):
    l_driver_session = driver_session
    l_lastname = lastname
    l_firstname = firstname
    print('Attempting to navigating to the probate search webpage.')
    l_driver_session.get(santa_fe_county_probate_url)
    l_driver_session.implicitly_wait(0.5)
    print('Navigated to', l_driver_session.current_url)
    text_lastname = l_driver_session.find_element(by=By.ID, value="txtName")
    text_firstname = l_driver_session.find_element(by=By.ID, value="txtInitial")
    login_search = l_driver_session.find_element(by=By.ID, value="btnSearch")
    # Filling in and pressing search
    print(f'Issuing a probate search for {l_lastname}, {l_firstname}')
    text_lastname.clear()
    text_lastname.send_keys(l_lastname)
    text_firstname.clear()
    text_firstname.send_keys(l_firstname)
    login_search.click()


class ProbeMain(tk.Tk):

    def do_search(self):
        l_lastname = self.search_name_var.get()
        l_firstname = self.search_initial_var.get()
        probate_query_field_entry_and_execute(l_lastname, l_firstname, self.driver_session)
        self.bring_forward()

    def search_again(self) -> NoReturn:
        l_lastname = self.search_name_var.get()
        l_firstname = self.search_initial_var.get()
        print(f'\nStarting a new probate search for {l_lastname}, {l_firstname}')
        try:
            probate_query_field_entry_and_execute(l_lastname, l_firstname, self.driver_session)
        except Exception:
            print('')
            print('Probate probe is starting a new session because the website is not')
            print('the expected one or maybe because browser was closed.')
            self.start_fresh_browser_driver()
            login_the_session(self.driver_session)
            self.do_search()

    def start_fresh_browser_driver(self):
        print('\nStarting a fresh browser driver session.')
        self.driver_session = webdriver.Chrome()

    def bring_forward(self) -> NoReturn:
        self.attributes('-topmost', True)
        self.update()
        self.attributes('-topmost', False)

    def do_quit(self) -> NoReturn:
        print('... Goodby ...')
        self.driver_session.quit()
        self.destroy()

    def __init__(self):
        super().__init__()
        self.title("Santa Fe County Probate Records Probe")
        w_width = 360
        w_height = 120
        pos_x = int(self.winfo_screenwidth() / 40 - w_width / 40)
        pos_y = int(self.winfo_screenheight() / 20 - w_height / 30)
        self.geometry("{}x{}+{}+{}".format(w_width, w_height, pos_x, pos_y))

        # set the Vars
        self.search_name_var = tk.StringVar(value=query_last_name)
        self.search_initial_var = tk.StringVar(value=query_first_name)

        # search frame
        self.search_lastname_frame = tk.Frame(self,
                                              borderwidth=0
                                              )
        self.search_lastname_frame.pack(fill=tk.X, padx=8, pady=0)

        self.lbl_name = tk.Label(self.search_lastname_frame,
                                 text="Last Name:")
        self.lbl_name.pack(side='left', padx=0, pady=1)

        self.name_txt_entry = tk.Entry(self.search_lastname_frame,
                                       textvariable=self.search_name_var,
                                       width=20)
        self.name_txt_entry.pack(side='left', padx=4, pady=1)

        self.search_firstname_frame = tk.Frame(self,
                                               borderwidth=0
                                               )
        self.search_firstname_frame.pack(fill=tk.X, padx=8, pady=0)

        self.lbl_initial = tk.Label(self.search_firstname_frame,
                                    text="First Name:")
        self.lbl_initial.pack(side='left', padx=0, pady=1)

        self.firstname_txt_entry = tk.Entry(self.search_firstname_frame,
                                            textvariable=self.search_initial_var,
                                            width=20)
        self.firstname_txt_entry.pack(side='left', padx=4, pady=1)

        # controls
        self.bts_frame = tk.Frame(self,
                                  borderwidth=0
                                  )
        self.bts_frame.pack(fill=tk.X, padx=0, pady=2)

        self.button_search = tk.Button(self.bts_frame, text="Search Again",
                                       width=80,
                                       command=self.search_again
                                       )
        self.button_search.pack(padx=8, pady=0)

        self.button_quit = tk.Button(self.bts_frame, text="Quit",
                                     width=80,
                                     command=self.do_quit)
        self.button_quit.pack(padx=8, pady=0)
        self.protocol("WM_DELETE_WINDOW", self.do_quit)  # assign to closing button [X]

        self.start_fresh_browser_driver()
        login_the_session(self.driver_session)
        self.do_search()


# end GrpsDrillingMain class


def mainloop(args=None):
    sfprobe_n: ProbeMain = ProbeMain()
    sfprobe_n.mainloop()


# ====================================== main ================================================
if __name__ == '__main__':
    mainloop()
