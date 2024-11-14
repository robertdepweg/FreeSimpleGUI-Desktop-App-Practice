"""Simple Beverage Management GUI"""

# Third-party Imports
import FreeSimpleGUI as sg

# First-Party Imports
from errors import AlreadyImportedError


class BeverageListWindow:
    """Simple Beverage List"""

    def __init__(self, beverage_collection, csv_processor, path_to_csv):
        """Constructor"""
        self.beverage_collection = beverage_collection
        self.csv_processor = csv_processor
        self.path_to_csv = path_to_csv

        layout = [
            [sg.Text("Beverage List")],
            [
                sg.Listbox(
                    ["No Beverages"], 
                    key="-output-", 
                    size=(150, 34),
                    font="TkFixedFont",
                )
            ],
            [
                sg.Button("Load CSV", key="-load_csv-"),
                sg.Button("Add New Beverage", key="-open_add_new-"),
                sg.Input("", key="-search_id-"),
                sg.Button("search", key="-search_button-"),
            ],
            [sg.Button("Exit")],
        ]
        self.window = sg.Window("Beverage List", layout)

    def run(self):
        """Start the window up"""
        self._run_loop()
        self.window.close()

    def _run_loop(self):
        """Run the event loop"""
        while True:
            event, values = self.window.read()
            if event == sg.WINDOW_CLOSED or event == "Exit":
                break
            elif event == "-load_csv-":
                self._on_load_csv(event, values)
            elif event == "-open_add_new-":
                self._on_open_add_new(event, values)
            elif event == "-search_button-":
                self._on_search(event, values)

    def _on_load_csv(self, event, values):
        """Handle when load CSV button is clicked"""
        try:
            self.csv_processor.import_csv(
                self.beverage_collection, 
                self.path_to_csv,
            )
            self._update_output(event, values)
            sg.popup_ok("Beverage list has been imported successfully.")

        except AlreadyImportedError:
            sg.popup_error("The CSV file has already been imported.")
        except FileNotFoundError:
            sg.popup_error("File not found for opening.")
        except EOFError:
            sg.popup_error("The file was unchanged.")

    def _on_open_add_new(self, event, values):
        """Open a new window to allow adding a new beverage"""
        add_window = BeverageAddWindow(self.beverage_collection)
        add_window.run()
        self._update_output(event, values)

    def _on_search(self, event, values):
        """Handle when user is searching for an item"""
        search_query = values["-search_id-"]
        beverage = self.beverage_collection.find_by_id(search_query)
        if beverage:
            result_window = BeverageResultWindow(beverage)
            result_window.run()
        else:
            sg.popup_error("Cannot find a beverage with that id.")

    def _update_output(self, event, values):
        """Update then contents of the output box"""
        self.window["-output-"].update(self.beverage_collection.beverages)


class BeverageAddWindow:
    """Simple Beverage Add"""

    def __init__(self, beverage_collection):
        """Constructor"""
        self.beverage_collection = beverage_collection

        layout = [
            [sg.Text("Id", size=(8,1)), sg.Input(key="-id-")],
            [sg.Text("Name", size=(8,1)), sg.Input(key="-name-")],
            [sg.Text("Pack", size=(8,1)), sg.Input(key="-pack-")],
            [sg.Text("Price", size=(8,1)), sg.Input(key="-price-")],
            [
                sg.Radio(
                    "Active",
                    "beverage_active_group",
                    key="-beverage_active-",
                    default=True,
                )
            ],
            [sg.Radio(
                "Inactive", 
                "beverage_active_group", 
                key="-beverage_inactive-")
            ],
            [sg.Button("Add", key="-add_new-")],
            [sg.Button("Cancel", key="-cancel-")],
        ]
        self.window = sg.Window("Beverage Add", layout)

    def run(self):
        """Start the window"""
        self._run_loop()
        self.window.close()

    def _run_loop(self):
        """Run the Event loop"""
        while True:
            event, values = self.window.read()
            if event == sg.WINDOW_CLOSED or event == "-cancel-":
                break
            elif event == "-add_new-":
                self._on_add_new(event, values)
                break

    def _on_add_new(self, event, values):
        """Handle when Add button is clicked"""
        self.beverage_collection.add(
            values["-id-"],
            values["-name-"],
            values["-pack-"],
            float(values["-price-"]), # Not good practice
            bool(values["-beverage_active-"]),
        )

class BeverageResultWindow:
    """Simple Beverage Result"""

    def __init__(self, beverage):
        """Constructor"""

        active_value = beverage.active
        inactive_value = not beverage.active

        layout = [
            [
                sg.Text("Name", size=(8,1)),
                sg.Input(key="-id-", default_text=beverage.name, disabled=True)
            ],
            [
                sg.Text("Name", size=(8,1)),
                sg.Input(key="-name-", default_text=beverage.name, disabled=True)
            ],
            [
                sg.Text("Pack", size=(8,1)),
                sg.Input(key="-pack-", default_text=beverage.name, disabled=True)
            ],
            [
                sg.Text("Price", size=(8,1)),
                sg.Input(key="-price-", default_text=beverage.name, disabled=True)
            ],
            [
                sg.Radio(
                    "Active", 
                    "beverage_active_group", 
                    key="-beverage_active-"
                )
            ],
            [
                sg.Radio(
                    "Inactive", 
                    "beverage_active_group", 
                    key="-beverage_inactive-"
                )
            ],
            [
                sg.Button("Close", key="-close-"),
            ],
        ]
        self.window = sg.Window("Beverage List", layout, modal=True)

    def run(self):
        """Start the window"""
        self._run_loop()
        self.window.close()

    def _run_loop(self):
        """Run the Event loop"""
        while True:
            event, values = self.window.read()
            if event == sg.WINDOW_CLOSED or event == "-close-":
                break