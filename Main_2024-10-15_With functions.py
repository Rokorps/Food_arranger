import pandas as pd
import PySimpleGUI as sg
import numpy as np
from scipy.optimize import lsq_linear

from tkinter import Tk 
edit = False
def objective(x):
    return np.sum(A.dot(x) - b) ** 2
def edit_cell(window, key, row, col, justify='left'):
    global textvariable, edit
    def callback(event, row, col, text, key):
        pre_text = text
        global edit
        # event.widget gives you the same entry widget we created earlier
        widget = event.widget
        if key == 'Focus_Out':
            # Get new text that has been typed into widget
            text = widget.get()
            # Print to terminal
            #print(text)
        # Destroy the entry widget
        widget.destroy()
        # Destroy all widgets
        widget.master.destroy()
        # Get the row from the table that was edited
        # table variable exists here because it was called before the callback
        values = list(table.item(row, 'values'))
        # Store new value in the appropriate row and column
        values[col] = text
        table.item(row, values=values)
        global edited_text
        if pre_text == text:
            edited_text = None
        else:
            edited_text = text
        edit = False

    if edit or row <= 0:
        return

    edit = True
    # Get the Tkinter functionality for our window
    root = window.TKroot
    # Gets the Widget object from the PySimpleGUI table - a PySimpleGUI table is really
    # what's called a TreeView widget in TKinter
    table = window[key].Widget
    #print(window,'|||', key,'|||', window[key],'|||', window[key].Widget)
    table_x = table.winfo_rootx()-root.winfo_rootx()
    table_y = table.winfo_rooty()-root.winfo_rooty()
    # Get the row as a dict using .item function and get individual value using [col]
    # Get currently selected value
    text = table.item(row, "values")[col]
    # Return x and y position of cell as well as width and height (in TreeView widget)
    x, y, width, height = table.bbox(row, col)
    #print('X:',table_x,'Y:',table_y, 'EX:', x, 'EY:', y, 'P:')
    #print(table.bbox(row, col))
    # Create a new container that acts as container for the editable text input widget
    frame = sg.tk.Frame(root)
    # put frame in same location as selected cell
    frame.place(x=x+table_x-5, y=y+table_y-5, anchor="nw", width=width, height=height)

    # textvariable represents a text value
    textvariable = sg.tk.StringVar()
    textvariable.set(text)
    # Used to acceot single line text input from user - editable text input
    # frame is the parent window, textvariable is the initial value, justify is the position
    entry = sg.tk.Entry(frame, textvariable=textvariable, justify=justify)
    # Organizes widgets into blocks before putting them into the parent
    entry.pack()
    # selects all text in the entry input widget
    entry.select_range(0, sg.tk.END)
    # Puts cursor at end of input text
    entry.icursor(sg.tk.END)
    # Forces focus on the entry widget (actually when the user clicks because this initiates all this Tkinter stuff, e
    # ending with a focus on what has been created)
    entry.focus_force()
    # When you click outside of the selected widget, everything is returned back to normal
    # lambda e generates an empty function, which is turned into an event function 
    # which corresponds to the "FocusOut" (clicking outside of the cell) event
    entry.bind("<FocusOut>", lambda e, r=row, c=col, t=text, k='Focus_Out':callback(e, r, c, t, k))
    entry.bind("<Return>", lambda e, r=row, c=col, t=text, k='Focus_Out':callback(e, r, c, t, k))
    entry.bind("<Escape>", lambda e, r=row, c=col, t=text, k='ESCAPE':callback(e, r, c, t, k))
def RightClickMenuCallback_TABLE(event, element,key):
    widget = element.Widget
    #current = widget.selection()
    #print(current)
    #if current:
    #    widget.selection_clear(current[0])
    y = int(str(event)[str(event).find('y=')+2:str(event).find('>')])
    index = widget.identify_row(y)
    widget.selection_set(index)
    element.TKRightClickMenu.tk_popup(event.x_root, event.y_root, 0)
    element.TKRightClickMenu.grab_release()
    global selected_row 
    global active_frame
    active_frame = key
    selected_row = int(index)

# API alike functions
def df_filter(Food_data, List_categories, List_data_type):
    Table_Foods_unimported = Food_data[Food_data['food_category_id'].isin(values['-List_categories-'])]
    Table_Foods_unimported = Table_Foods_unimported[Table_Foods_unimported['data_type'].isin(values['-List_data_type-'])]
    Table_Foods_unimported_without_nutrients = Table_Foods_unimported[['fdc_id', 'data_type', 'description', 'food_category_id']]
    return Table_Foods_unimported_without_nutrients
def df_Move_food_in(Table_Foods_imported_without_nutrients, Table_Foods_unimported_without_nutrients, List_Table_Foods_unimported):
    if isinstance(Table_Foods_imported_without_nutrients, pd.DataFrame):
        Table_Foods_imported_without_nutrients = pd.concat([Table_Foods_imported_without_nutrients,Table_Foods_unimported_without_nutrients.iloc[List_Table_Foods_unimported]])
    else:
        Table_Foods_imported_without_nutrients = Table_Foods_unimported_without_nutrients.iloc[List_Table_Foods_unimported]
    indexes = Table_Foods_unimported_without_nutrients.index[List_Table_Foods_unimported]
    Table_Foods_unimported_without_nutrients.drop(index = indexes, inplace = True)
    Table_Foods_imported_without_nutrients = Table_Foods_imported_without_nutrients.sort_index()
    return Table_Foods_imported_without_nutrients, Table_Foods_unimported_without_nutrients
def df_Move_food_out(Table_Foods_imported_without_nutrients, Table_Foods_unimported_without_nutrients, List_Table_Foods_imported):
    Table_Foods_unimported_without_nutrients = pd.concat([Table_Foods_unimported_without_nutrients,Table_Foods_imported_without_nutrients.iloc[List_Table_Foods_imported]])
    indexes = Table_Foods_imported_without_nutrients.index[List_Table_Foods_imported]
    Table_Foods_imported_without_nutrients.drop(index = indexes, inplace = True)
    Table_Foods_unimported_without_nutrients = Table_Foods_unimported_without_nutrients.sort_index()
    return Table_Foods_imported_without_nutrients, Table_Foods_unimported_without_nutrients
def df_Move_Nutrient_in(Nutrient_data, Table_Nutrients_imported, List_Table_Nutrients):
    if isinstance(Table_Nutrients_imported, pd.DataFrame):
        Table_Nutrients_imported = pd.concat([Table_Nutrients_imported,Nutrient_data.iloc[List_Table_Nutrients].assign(address=[0]*len(Nutrient_data.iloc[List_Table_Nutrients]))])
    else:
        Table_Nutrients_imported = Nutrient_data.iloc[List_Table_Nutrients].assign(target_value=[0]*len(Nutrient_data.iloc[List_Table_Nutrients]))
    indexes = Nutrient_data.index[List_Table_Nutrients]
    Nutrient_data.drop(index = indexes, inplace = True)
    Table_Nutrients_imported = Table_Nutrients_imported.sort_index()
    return Nutrient_data, Table_Nutrients_imported
def df_Move_Nutrient_out(Nutrient_data, Table_Nutrients_imported, List_Table_Nutrients_targets):
    Nutrient_data = pd.concat([Nutrient_data,Table_Nutrients_imported[['nutrient_id', 'nutrient_name', 'nutrient_unit_name']].iloc[List_Table_Nutrients_targets]])
    indexes = Table_Nutrients_imported.index[List_Table_Nutrients_targets]
    Table_Nutrients_imported.drop(index = indexes, inplace = True)
    Nutrient_data = Nutrient_data.sort_index()
    return Nutrient_data, Table_Nutrients_imported
def Food_aranger_calculate_weights(Food_data, Table_Nutrients_imported, Table_Foods_imported_without_nutrients):
    Food_data_needed_columns = []
    for idx in Table_Nutrients_imported.index:
        Food_data_needed_columns.append(idx+4) # it is the thing if foods dataframe has additonal column for each nutrient content. Here is noted only targeted nutrient columns so that in next line the dataframe would be correctly cut.
    A = np.rot90(Food_data.iloc[Table_Foods_imported_without_nutrients.index,Food_data_needed_columns].replace(-1, 0).to_numpy())[::-1] # Create investigated nutritional values 2D matrix of chosen food
    b = Table_Nutrients_imported['target_value'].to_numpy() # create 1D matrix of a target chosen nutrients content
    bounds = (0, np.inf) # bounds so that food weights would not go below zero 
    result = lsq_linear(A,b,bounds = bounds, max_iter = 5000000000) # from scipy.optimize import lsq_linear (max iter just in case..)
    x = result.x # resulting weights of food for chosen nutritional content
    predicted_values = A.dot(x) # predicted nutrient values
    residuals = predicted_values - b # difference between predicted (calculated) and target nutrient content values (residuals)
    return x, predicted_values, residuals
##
Nutrient_data = pd.read_csv('Nutrient_data.csv',sep = '|')

Food_data = pd.read_csv('Food_data.csv',sep = '|')

Food_category = pd.read_csv('food_category_EDITED.csv',sep = '|')


Food_category_ids = Food_data.food_category_id.unique()
Food_category_list = Food_category['description'].tolist()
Food_categories_available = []
for i in Food_category_ids:
	y = i-1
	Food_categories_available.append(Food_category_list[y])
	Food_data.loc[Food_data['food_category_id'] == i, 'food_category_id'] = Food_category_list[y]
Available_data_type_cols = Food_data.data_type.unique()
Table_Foods_unimported = []
Table_Foods_imported = []
Table_Food_nutrient_values = []
Nutrient_data = Nutrient_data[['nutrient_id', 'nutrient_name', 'nutrient_unit_name']]
Nutrient_names = Nutrient_data['nutrient_name'].to_list()
#print(Nutrient_names)
Table_Nutrients_list = Nutrient_data.to_numpy().tolist()
Table_Nutrients_targets = []
Table_Foods_weights = []
#print(Nutrient_data.columns)
layout = [[
			sg.Column(
			[[
					sg.Text('Kategorijos')
				],[
					sg.Listbox(Food_categories_available,
        			    select_mode=sg.TABLE_SELECT_MODE_EXTENDED,
        			    key='-List_categories-',
        			    size=(50, 12),
        			    expand_x=True,
        			    expand_y=True
        			)
        	]],
        	expand_x=True,
        	expand_y=True
        	),
			sg.Column(
			[[
					sg.Text('Duomenų tipas')
				],[
					sg.Listbox(Available_data_type_cols,
        			    select_mode=sg.TABLE_SELECT_MODE_EXTENDED,
        			    key='-List_data_type-',
        			    size=(50, 12),
        			    expand_x=True,
        			    expand_y=True
        			)
        	]],
        	expand_x=True,
        	expand_y=True
        	),
        ],[
        	sg.Button( 'Filtruoti',
        	    key = '-B_filter_categories-',
				enable_events=True
        	)
        ],[
        	sg.HorizontalSeparator(),
        ],[
        	sg.Text('Paieska'),
			sg.Input(key = '-Search_food-',
        	    size = (43, 1)
        	)
			],[
			sg.Table(values=Table_Foods_unimported, headings=['fdc_id', 'data_type', 'description', 'food_category_id'], max_col_width=15,
        	          auto_size_columns=True,
        	          justification='left',
        	          num_rows=12,
        	          key='-Table_Foods_unimported-',
        	          enable_events=True,
        	          select_mode=sg.TABLE_SELECT_MODE_EXTENDED,
        	          expand_x=True,
        	          expand_y=True,
        	          enable_click_events=True,  # Comment out to not enable header and other clicks,
        	),
        	sg.Column([[
        		sg.Button( '--->',
            	  	key = '-Move_food_in-',
					enable_events=True
            	)
            	],[
            	sg.Button( '<---',
            	  	key = '-Move_food_out-',
					enable_events=True
            	)
        	]]),
        	sg.Table(values=Table_Foods_imported, headings=['fdc_id', 'data_type', 'description', 'food_category_id'], max_col_width=15,
        	          auto_size_columns=True,
        	          justification='left',
        	          num_rows=12,
        	          key='-Table_Foods_imported-',
        	          enable_events=True,
        	          select_mode=sg.TABLE_SELECT_MODE_EXTENDED,
        	          expand_x=True,
        	          expand_y=True,
        	          enable_click_events=True,  # Comment out to not enable header and other clicks,
        	),
        	sg.VerticalSeparator(),
        	sg.Table(values=Table_Food_nutrient_values, headings=['Nutrient description', 'value'], max_col_width=15,
        	          auto_size_columns=True,
        	          justification='left',
        	          num_rows=12,
        	          key='-Table_Food_nutrient_values-',
        	          enable_events=True,
        	          select_mode=sg.TABLE_SELECT_MODE_EXTENDED,
        	          expand_x=True,
        	          expand_y=True,
        	          enable_click_events=True,  # Comment out to not enable header and other clicks,
        	)
        ],[
            sg.Text('Paieska'),
            sg.Input(key = '-Search_nutriet-',
                size = (43, 1),
                enable_events=True,
            )
            ],[
        	sg.Table(values=Table_Nutrients_list, headings=['nutrient_id','Nutrient description', 'nutrient_unit_name'], max_col_width=15,
        	          auto_size_columns=True,
        	          justification='left',
        	          num_rows=12,
        	          key='-Table_Nutrients_list-',
        	          enable_events=True,
        	          select_mode=sg.TABLE_SELECT_MODE_EXTENDED,
        	          expand_x=True,
        	          expand_y=True,
        	          enable_click_events=True,  # Comment out to not enable header and other clicks,
        	),
        	sg.Column([[
        		sg.Button( '--->',
            	  	key = '-Move_Nutrient_in-',
					enable_events=True
            	)
            	],[
            	sg.Button( '<---',
            	  	key = '-Move_Nutrient_out-',
					enable_events=True
            	)
            	]]
            ),
            sg.Table(values=Table_Nutrients_targets, headings=['nutrient_id','Nutrient description', 'nutrient_unit_name','target value'], max_col_width=15,
        	          auto_size_columns=True,
        	          justification='left',
        	          num_rows=12,
        	          key='-Table_Nutrients_targets-',
        	          enable_events=True,
        	          select_mode=sg.TABLE_SELECT_MODE_EXTENDED,
        	          expand_x=True,
        	          expand_y=True,
        	          enable_click_events=True,  # Comment out to not enable header and other clicks,
        	)
        ],[
        	sg.HorizontalSeparator(),
        ],[
        	sg.Button( 'Skaičiuoti',
              	key = '-B_GO-',
				enable_events=True
            )
        ],[
        	sg.Table(values=Table_Foods_weights, headings=['description','weight in grams'], max_col_width=15,
        	          auto_size_columns=True,
        	          justification='left',
        	          num_rows=12,
        	          key='-Table_Foods_weights-',
        	          enable_events=True,
        	          select_mode=sg.TABLE_SELECT_MODE_EXTENDED,
        	          expand_x=True,
        	          expand_y=True,
        	          enable_click_events=True,  # Comment out to not enable header and other clicks,
        	)
	]]
window = sg.Window('Food_aranger beta', 
                    layout,
                    resizable = True,
                    return_keyboard_events=True,
                    finalize = True)

window["-Table_Foods_unimported-"].Widget.bind('<Button-3>', '_YY')
last_event = False
event = False
edited_text = None
Table_Foods_unimported_values = None
Table_Foods_imported_without_nutrients = False
Table_Nutrients_imported = False
# Multiplication leap value
Leap = 1.01
# defining preset
arr_addresses = [63,3,4,5,6,110,111,107,163,166,167,168,171,176,177,178,179,184,88,90,91,93,94,104,96,99,101,102,103,211,212,213,214,215,216,217,218,219,220]
arr_goals = [11000,9,56,80,400,15,700,900,90,1.2,1.3,16,5,1.3,30,400,2.4,120,100,8,410,700,3400,2300,55,11,0.9,150,2.3,45,0.28,1.05,0.14,2.73,2.1,0.72,0.297,1.75,1.9]
rarr_addresses = []
rarr_goals = []
Choices_dict = {}
for i in range(len(arr_addresses)):
    Choices_dict[arr_addresses[i]] = arr_goals[i]
Choices_dict = dict(sorted(Choices_dict.items()))
#print(Choices_dict)
Table_Nutrients_imported = Nutrient_data.iloc[list(Choices_dict.keys())].assign(target_value=list(Choices_dict.values()))
indexes = Nutrient_data.index[list(Choices_dict.keys())]
Nutrient_data.drop(index = indexes, inplace = True)
window['-Table_Nutrients_list-'].update(values = Nutrient_data.to_numpy().tolist())
Table_Nutrients_imported = Table_Nutrients_imported.sort_index()
window['-Table_Nutrients_targets-'].update(values = Table_Nutrients_imported.to_numpy().tolist())
while True:
    print(event)
    if edited_text != None:
        Table_Nutrients_imported.at[Table_Nutrients_imported.index[row],'target_value'] = float(edited_text)
        print(Table_Nutrients_imported)
        print('EDITED: ',edited_text, row+1)
        edited_text = None
    if event:
        if isinstance(event, tuple):
            last_event = event
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event == '-B_filter_categories-':
        Table_Foods_unimported_without_nutrients = df_filter(Food_data, values['-List_categories-'], values['-List_data_type-'])
        window['-Table_Foods_unimported-'].update(values = Table_Foods_unimported_without_nutrients.to_numpy().tolist())
    if event == '-Search_food-':
        pass
    if event == 'Return:36':
        if last_event:
            if 'Table' in last_event[0]:
                row, col = last_event[2]
                edit_cell(window, '-Table_Nutrients_targets-', row+1, 3, justify='left')
    if event == '-Move_food_in-':
        try:
            Table_Foods_imported_without_nutrients, Table_Foods_unimported_without_nutrients = df_Move_food_in(Table_Foods_imported_without_nutrients, Table_Foods_unimported_without_nutrients, values['-Table_Foods_unimported-'])
            window['-Table_Foods_unimported-'].update(values = Table_Foods_unimported_without_nutrients.to_numpy().tolist())
            window['-Table_Foods_imported-'].update(values = Table_Foods_imported_without_nutrients.to_numpy().tolist())
        except:
            pass
    if event == '-Move_food_out-':
        try:
            Table_Foods_imported_without_nutrients, Table_Foods_unimported_without_nutrients = df_Move_food_out(Table_Foods_imported_without_nutrients, Table_Foods_unimported_without_nutrients, values['-Table_Foods_imported-'])
            window['-Table_Foods_unimported-'].update(values = Table_Foods_unimported_without_nutrients.to_numpy().tolist())
            window['-Table_Foods_imported-'].update(values = Table_Foods_imported_without_nutrients.to_numpy().tolist())
        except:
            pass
    if isinstance(event, tuple):
        try:
            if event[0] == '-Table_Foods_imported-':
                index_of_food = Table_Foods_imported_without_nutrients.index[[event[2][0]]]
                #np.rot90(Food_data.loc[index_of_food].to_numpy()).tolist()[1:]
                Displayed_food_Nutrients_npArray = np.rot90([Food_data.loc[index_of_food].values[0][4:479],Nutrient_names], k = 3)[Table_Nutrients_imported.index,:]
                window['-Table_Food_nutrient_values-'].update(values = Displayed_food_Nutrients_npArray.tolist())
        except:
            pass
    if event == '-Search_nutriet-':
        pass
    if event == '-Move_Nutrient_in-':
        try:
            Nutrient_data, Table_Nutrients_imported = df_Move_Nutrient_in(Nutrient_data, Table_Nutrients_imported, values['-Table_Nutrients_list-'])
            window['-Table_Nutrients_list-'].update(values = Nutrient_data.to_numpy().tolist())
            window['-Table_Nutrients_targets-'].update(values = Table_Nutrients_imported.to_numpy().tolist())
        except:
            pass
    if event == '-Move_Nutrient_out-':
        try:
            Nutrient_data, Table_Nutrients_imported = df_Move_Nutrient_out(Nutrient_data, Table_Nutrients_imported, values['-Table_Nutrients_targets-'])
            window['-Table_Nutrients_list-'].update(values = Nutrient_data.to_numpy().tolist())
            window['-Table_Nutrients_targets-'].update(values = Table_Nutrients_imported.to_numpy().tolist())
        except:
            pass
    if event == '-B_GO-':
        try:
            x, predicted_values, residuals = Food_aranger_calculate_weights(Food_data, Table_Nutrients_imported, Table_Foods_imported_without_nutrients)
            window['-Table_Foods_weights-'].update(values = np.rot90([x,Table_Foods_imported_without_nutrients['description'].values], k = 3).tolist(), visible = True)
        except:
            pass
window.close()