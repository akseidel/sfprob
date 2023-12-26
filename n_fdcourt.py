# akseidel 11/27/2023
import tkinter as tk
from tkinter import messagebox #as mb
from typing import NoReturn
from selenium import webdriver
from selenium.webdriver.common.by import By

# globals
party_last_name = 'Montoya'
party_first_name = 'Emaho'
firstdistrict_court_nm_caselookup_url = "https://caselookup.nmcourts.gov/caselookup/"


def go_to_nmcourts(driver_session):
    l_driver_session = driver_session
    print(f'About to navigate to {firstdistrict_court_nm_caselookup_url}')
    l_driver_session.get(firstdistrict_court_nm_caselookup_url)
    l_driver_session.implicitly_wait(0.5)
    print(f'Navigated to {l_driver_session.current_url}')

    # Setting the object to press the accept
    # New Mexico State Judiciary Case Lookup Disclaimer
    accept_button = l_driver_session.find_element(by=By.ID, value="Submit")
    print('Now attempting to accept.')
    accept_button.click()
    print(f'Now at the webpage called: {l_driver_session.title}')

    res = captcha_call()
    if res:
        # Setting the object to press the
        # Continue to Case Lookup button
        print('Now attempting to Continue to Case Lookup.')
        accept_button = l_driver_session.find_element(by=By.ID, value="Submit")
        accept_button.click()
        l_driver_session.implicitly_wait(0.5)
        print(f'Now at the webpage called: {l_driver_session.title}')
    else:
        print(f'Quit was pressed.')
        driver_session.quit()
        exit()

def new_mexico_courts_query_field_entry_and_execute(lfm_name, driver_session):
    l_driver_session = driver_session
    l_driver_session.implicitly_wait(0.5)
    print(f'Navigated to {l_driver_session.current_url}')
    l_last_first_middle_name = lfm_name
    print(f'Plugging in {l_last_first_middle_name}')
    text_lfm_name = l_driver_session.find_element(by=By.ID, value="partyName")
    # Filling in and pressing search
    print(f'Entering the party\'s name for search {l_last_first_middle_name}')
    text_lfm_name.clear()
    text_lfm_name.send_keys(l_last_first_middle_name)
    party_search = l_driver_session.find_element(by=By.ID, value="Submit")
    print(f'Issuing a party name search for {l_last_first_middle_name}')
    party_search.click()


def captcha_call():
    print(f'Asking to do the captcha and waiting for the OK to continue.')
    mb = messagebox
    res = mb.askokcancel(title='First Do The CAPTCHA',
                         message="Complete the CAPTCHA.\n\nGet the"
                                 " \"I\'m not a robot\" checkbox to be checked."
                                 "\n\nThen press this OK.\n\nIgnore the \"Continue to Case Lookup\"."
                         )
    return res


class NMCourtSession(tk.Tk):
    def party_lfm_name(self):
        return " ".join([self.search_name_var.get(), self.search_initial_var.get()])

    def do_the_case_lookup(self):
        print(f'\nStarting a new party search for {self.party_lfm_name()}')
        new_mexico_courts_query_field_entry_and_execute(self.party_lfm_name(), self.driver_session)
        self.bring_forward()

    def search_again(self) -> NoReturn:
        print(f'\nStarting a new party search for {self.party_lfm_name}')
        try:
            new_mexico_courts_query_field_entry_and_execute(self.party_lfm_name, self.driver_session)
        except Exception:
            print('')
            print('Starting a new session because the website is not')
            print('the expected one or maybe because browser was closed.')
            self.start_fresh_browser_driver()
            go_to_nmcourts(self.driver_session)
            self.do_the_case_lookup()

    def start_fresh_browser_driver(self):
        print('\nStarting a fresh browser driver session.')
        self.driver_session = webdriver.Chrome()
        print('\nStarted a fresh browser driver session.')

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
        self.title("New Mexico Case Lookup")
        w_width = 360
        w_height = 120
        pos_x = int(self.winfo_screenwidth() / 40 - w_width / 40)
        pos_y = int(self.winfo_screenheight() / 20 - w_height / 30)
        self.geometry("{}x{}+{}+{}".format(w_width, w_height, pos_x, pos_y))

        # set the Vars
        self.search_name_var = tk.StringVar(value=party_last_name)
        self.search_initial_var = tk.StringVar(value=party_first_name)

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
        go_to_nmcourts(self.driver_session)
        self.do_the_case_lookup()

# end NMCourtSession class


def mainloop(args=None):
   courtmain = NMCourtSession()


# ====================================== main ================================================
if __name__ == '__main__':
    mainloop()
